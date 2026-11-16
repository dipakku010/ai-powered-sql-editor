# LLM Schema Prompt Generator for Oracle Database Schemas

# This module provides a function to generate a text prompt suitable for LLMs
# from an Oracle database schema dictionary.


# Generates an LLM-friendly schema prompt from the extracted Oracle schema.
def generate_llm_schema_prompt(schema: dict) -> str:
    """Converts structured schema dict into an LLM-friendly DDL text string.

    Args:
        schema (dict): A dictionary representing the Oracle database schema.

    Returns:
        str: A string containing the LLM-friendly DDL text for the schema.
    """
    # Initialize a list to hold the lines of the prompt.
    prompt_lines = ["Database Dialect: Oracle SQL\n"]
    # Iterate over each table and its columns to generate the DDL statements.
    for table_name, columns in schema.items():
        # Add a comment indicating the start of a new table's DDL.
        prompt_lines.append(f"-- Table: {table_name}")
        # Add an empty line for readability between tables.
        prompt_lines.append("")
        # Start the CREATE TABLE statement for the current table.
        prompt_lines.append(f"CREATE TABLE {table_name} (")
        # Initialize a list to hold the column definitions for the current table.
        col_definitions = []
        # Iterate over each column to generate its definition within the CREATE TABLE statement.
        for col in columns:
            parts = [f"  {col['column_name']} {col['data_type']}"]
            # Add column constraints based on the column properties.
            if col["is_pk"]:
                parts.append("PRIMARY KEY")
            if not col["nullable"] and not col["is_pk"]:
                parts.append("NOT NULL")
            if col["fk_ref"]:
                parts.append(f"REFERENCES {col['fk_ref']}")
            # Join the parts to form the column definition string.
            col_str = " ".join(parts)
            # Combine the column parts into a single string.
            # Append column comment if exists
            if col["comment"]:
                col_str += f" -- {col['comment']}"
            col_definitions.append(col_str)

        # Append the column definitions to the prompt, separated by commas.
        prompt_lines.append(",\n".join(col_definitions))
        # Close the CREATE TABLE statement for the current table.
        prompt_lines.append(");\n")
        # Add an empty line for readability between tables.
        prompt_lines.append("")
    # Join all the prompt lines into a single string and return it.
    return "\n".join(prompt_lines)
