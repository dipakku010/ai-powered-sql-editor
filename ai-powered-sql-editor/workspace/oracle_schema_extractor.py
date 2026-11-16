# Oracle database schema extractor.
#
# The module intentionally reads metadata from Oracle's USER_* views. Those views
# describe objects owned by the authenticated user, so the result is scoped to
# the schema associated with ORACLE_USER rather than to every schema in the
# database.

import oracledb
import os

# The database uses a password verifier that thin mode cannot authenticate.
# Allow deployments to override the local Oracle Instant Client location.
oracledb.init_oracle_client(
    lib_dir=os.environ.get("ORACLE_CLIENT_LIB_DIR", "/opt/oracle")
)


# Returns a connection to the Oracle database using environment variables for credentials.
def get_db_connection():
    """Create an Oracle connection from the process environment.

    Keeping credentials outside the source file makes the extractor suitable for
    local development and deployment environments without embedding passwords in
    code. ``ORACLE_DSN`` may be a connect descriptor such as
    ``localhost:1521/XEPDB1`` or a configured TNS alias.

    The connection object is returned to the caller so the caller can manage its
    lifetime with a context manager.
    """
    # ``os.environ.get`` returns ``None`` when a setting is absent. The Oracle
    # driver then reports the missing connection value when ``connect`` is
    # called, keeping configuration lookup in one place.
    return oracledb.connect(
        user=os.environ.get("ORACLE_USER"),
        password=os.environ.get("ORACLE_PASSWORD"),
        dsn=os.environ.get("ORACLE_DSN"),
    )


# Fetch the Oracle schema as a table-to-column mapping.
def fetch_oracle_schema():
    """Return the owned Oracle schema as a table-to-column mapping.

    Each table name maps to a list of column dictionaries. Each dictionary
    contains the normalized data type, nullability, column comment, primary-key
    flag, and an optional foreign-key target in ``TABLE(COLUMN)`` form.

    The database connection and cursor are context-managed so both are closed
    when metadata extraction finishes, including when query execution or row
    processing raises an exception.
    """
    query = """
   -- USER_TAB_COLS supplies one row for each visible column in the current
   -- user's schema, including the type attributes needed for formatting below.
   SELECT
   tc.table_name,
   tc.column_name,
   tc.data_type,
   tc.data_length,
   tc.data_precision,
   tc.data_scale,
   tc.nullable,
   cc.comments AS column_comment,
   pk.is_primary_key,
   fk.r_table_name AS fk_ref_table,
   fk.r_column_name AS fk_ref_column
FROM user_tab_cols tc
-- Join Column Comments
LEFT JOIN user_col_comments cc
   ON tc.table_name = cc.table_name
  AND tc.column_name = cc.column_name
-- Join Primary Keys
LEFT JOIN (
   SELECT cons.table_name, cols.column_name, 1 AS is_primary_key
   FROM user_constraints cons
   JOIN user_cons_columns cols ON cons.constraint_name = cols.constraint_name
   WHERE cons.constraint_type = 'P'
) pk
   ON tc.table_name = pk.table_name
  AND tc.column_name = pk.column_name
-- Join Foreign Keys
LEFT JOIN (
   SELECT
       src_cols.table_name,
       src_cols.column_name,
       ref_cols.table_name AS r_table_name,
       ref_cols.column_name AS r_column_name
   FROM user_constraints cons
   JOIN user_cons_columns src_cols ON cons.constraint_name = src_cols.constraint_name
   JOIN user_constraints ref_cons ON cons.r_constraint_name = ref_cons.constraint_name
   JOIN user_cons_columns ref_cols ON ref_cons.constraint_name = ref_cols.constraint_name
   WHERE cons.constraint_type = 'R'
) fk
   ON tc.table_name = fk.table_name
  AND tc.column_name = fk.column_name
-- Exclude Oracle Recycle Bin tables
WHERE tc.table_name NOT LIKE 'BIN$%'
ORDER BY tc.table_name, tc.column_id;
   """

    # The outer dictionary groups the flat query result into the structure used
    # by callers: {table_name: [column_metadata, ...]}.
    schema = {}
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Fetch all metadata before closing the cursor. The result set is
            # normally small enough for this utility and keeps row processing
            # independent from the live cursor.
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                (
                    table_name,
                    col_name,
                    data_type,
                    data_len,
                    precision,
                    scale,
                    nullable,
                    comment,
                    is_pk,
                    fk_table,
                    fk_col,
                ) = row

                # A table appears once per column in the query. Initialize its
                # list on the first row, then append each column in the ORDER BY
                # order returned by Oracle.
                if table_name not in schema:
                    schema[table_name] = []

                # Preserve length information for character and RAW columns.
                # Oracle reports these attributes separately from DATA_TYPE.
                if data_type in ("VARCHAR2", "CHAR", "RAW"):
                    type_str = f"{data_type}({data_len})"

                # NUMBER precision and scale are also separate metadata fields.
                # A missing scale represents an integer-like NUMBER, so expose it
                # consistently as scale zero in the normalized type string.
                elif data_type == "NUMBER" and precision is not None:
                    type_str = f"NUMBER({precision},{scale or 0})"
                else:
                    # Types without a length or precision, such as DATE and
                    # TIMESTAMP, are already complete in DATA_TYPE.
                    type_str = data_type

                # Convert Oracle's Y/N flags into Python booleans and represent
                # absent foreign-key metadata as None rather than a malformed
                # string. The original column comment is retained as returned by
                # Oracle, including None when no comment exists.
                schema[table_name].append(
                    {
                        "column_name": col_name,
                        "data_type": type_str,
                        "nullable": nullable == "Y",
                        "comment": comment,
                        "is_pk": bool(is_pk),
                        "fk_ref": f"{fk_table}({fk_col})" if fk_table else None,
                    }
                )
    return schema
