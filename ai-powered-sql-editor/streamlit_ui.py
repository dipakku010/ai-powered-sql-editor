"""Streamlit UI for AI SQL Editor API

This Streamlit app provides a user-friendly interface to interact with the AI SQL Editor Flask API.
It enables users to:
1. Generate SQL queries from natural language instructions
2. Auto-complete SQL snippets

Run with:
    streamlit run streamlit_ui.py
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Configure the Streamlit app
st.set_page_config(
    page_title="AI SQL Editor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 4px;
        margin-top: 10px;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 4px;
        margin-top: 10px;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 12px;
        border-radius: 4px;
        margin-top: 10px;
    }
    .code-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 12px;
        border-radius: 4px;
        margin-top: 10px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== SIDEBAR CONFIGURATION ====================
st.sidebar.title("⚙️ Configuration")

# API Configuration
api_host = st.sidebar.text_input(
    "API Host", value="127.0.0.1", help="The host where the Flask API is running"
)
api_port = st.sidebar.number_input(
    "API Port",
    value=5002,
    min_value=1024,
    max_value=65535,
    help="The port number for the Flask API",
)
api_timeout = st.sidebar.slider(
    "API Timeout (seconds)", min_value=5, max_value=120, value=30
)

# Build API base URL
api_base_url = f"http://{api_host}:{api_port}/api/sql"

# Display connection status
st.sidebar.markdown("---")
st.sidebar.subheader("📡 Connection Status")

try:
    response = requests.get(f"http://{api_host}:{api_port}/hello", timeout=2)
    if response.status_code == 200:
        st.sidebar.markdown(
            '<div class="success-box">✅ Connected to API</div>',
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.warning("⚠️ API returned unexpected status")
except requests.exceptions.ConnectionError:
    st.sidebar.error("❌ Cannot connect to API. Make sure Flask app is running!")
except requests.exceptions.Timeout:
    st.sidebar.error("❌ API connection timeout")
except Exception as e:
    st.sidebar.error(f"❌ Error: {str(e)}")

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This app demonstrates AI-powered SQL query generation using LangChain and Groq LLM. "
    "It features two modes:\n"
    "1. **Generate**: Convert natural language to Oracle SQL\n"
    "2. **Autocomplete**: Complete SQL snippets intelligently"
)

# ==================== MAIN INTERFACE ====================
st.title("🚀 AI SQL Editor")
st.markdown(
    "**Transform natural language into Oracle SQL queries using AI** | Powered by LangChain + Groq LLM"
)

# Create tabs for different features
tab1, tab2, tab3 = st.tabs(["🔨 Generate SQL", "✨ Auto-Complete", "📚 Documentation"])

# ==================== TAB 1: GENERATE SQL ====================
with tab1:
    st.header("Generate SQL from Natural Language")
    st.markdown(
        "Describe what you want in plain English, and let AI generate the Oracle SQL for you."
    )

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.subheader("📝 Natural Language Instruction")

        # Example instructions
        example_instructions = {
            "Get top 10 customers": "Fetch the top 10 customers by total purchase amount",
            "Active users this month": "Get all active users who logged in during this month",
            "Sales by region": "Show total sales grouped by region for the current year",
            "Employee details": "List all employees with their department and salary",
            "Product inventory": "Display all products with low inventory (less than 10 units)",
        }

        instruction = st.text_area(
            "Enter your SQL requirement:",
            height=120,
            placeholder="e.g., Fetch all users who registered in the last 7 days and sort by registration date",
            help="Describe what SQL query you need in natural language",
        )

        # Quick example buttons
        st.markdown("**Quick Examples:**")
        example_col1, example_col2, example_col3 = st.columns(3)
        with example_col1:
            if st.button("👥 Get top 10 customers"):
                instruction = example_instructions["Get top 10 customers"]
                st.session_state.instruction = instruction
        with example_col2:
            if st.button("📊 Active users this month"):
                instruction = example_instructions["Active users this month"]
                st.session_state.instruction = instruction
        with example_col3:
            if st.button("💰 Sales by region"):
                instruction = example_instructions["Sales by region"]
                st.session_state.instruction = instruction

    with col2:
        st.subheader("⚡ Actions")

        # Generate button
        generate_button = st.button(
            "🚀 Generate SQL",
            use_container_width=True,
            type="primary",
            help="Click to generate SQL from your instruction",
        )

        st.markdown("---")

        # Display latest results
        st.markdown("**Status:** Ready")
        st.markdown("**Mode:** SQL Generation")

    # Execute generation
    if generate_button or (instruction and "generate_clicked" in st.session_state):
        if not instruction.strip():
            st.error("❌ Please enter a natural language instruction!")
        else:
            st.session_state.generate_clicked = True

            with st.spinner("🤖 AI is generating SQL... Please wait..."):
                try:
                    response = requests.post(
                        f"{api_base_url}/generate",
                        json={"instruction": instruction},
                        timeout=api_timeout,
                    )

                    if response.status_code == 200:
                        result = response.json()
                        generated_sql = result.get("sql", "")

                        # Display success
                        st.markdown(
                            '<div class="success-box">✅ SQL Generated Successfully!</div>',
                            unsafe_allow_html=True,
                        )

                        # Display the generated SQL
                        st.subheader("📋 Generated SQL Query")
                        st.code(generated_sql, language="sql")

                        # Additional actions
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📋 Copy to Clipboard", key="copy_gen"):
                                st.write(
                                    "SQL copied to clipboard! (Note: Use external clipboard for actual copy)"
                                )
                        with col2:
                            if st.button("🔄 New Query", key="new_gen"):
                                st.rerun()
                        with col3:
                            st.download_button(
                                label="⬇️ Download SQL",
                                data=generated_sql,
                                file_name=f"generated_query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql",
                                mime="text/sql",
                                key="download_gen",
                            )

                        # Show metadata
                        with st.expander("📊 Query Metadata"):
                            st.json(
                                {
                                    "instruction": instruction,
                                    "timestamp": datetime.now().isoformat(),
                                    "api_endpoint": f"{api_base_url}/generate",
                                }
                            )

                    else:
                        error_data = response.json()
                        error_message = error_data.get("error", "Unknown error")
                        st.markdown(
                            f'<div class="error-box">❌ Error: {error_message}</div>',
                            unsafe_allow_html=True,
                        )
                        st.error(f"API Error: {error_message}")

                except requests.exceptions.Timeout:
                    st.error(
                        f"❌ Request timed out after {api_timeout} seconds. Try increasing timeout in settings."
                    )
                except requests.exceptions.ConnectionError:
                    st.error(
                        "❌ Failed to connect to API. Make sure the Flask app is running on "
                        f"{api_host}:{api_port}"
                    )
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

# ==================== TAB 2: AUTO-COMPLETE ====================
with tab2:
    st.header("Auto-Complete SQL Snippets")
    st.markdown("Start typing a SQL query, and let AI complete it for you.")

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.subheader("📝 SQL Snippet")

        # Example snippets
        example_snippets = {
            "SELECT basic": "SELECT * FROM",
            "SELECT with WHERE": "SELECT id, name, email FROM users WHERE",
            "JOIN query": "SELECT u.id, u.name, o.order_id FROM users u JOIN orders o ON",
            "GROUP BY": "SELECT department, COUNT(*) FROM employees GROUP BY",
            "ORDER BY": "SELECT * FROM products WHERE price >",
        }

        sql_snippet = st.text_area(
            "Enter SQL snippet to complete:",
            height=120,
            placeholder="e.g., SELECT * FROM users WHERE",
            help="Provide the beginning of a SQL query and AI will complete it",
        )

        # Quick example buttons
        st.markdown("**Quick Examples:**")
        example_col1, example_col2, example_col3 = st.columns(3)
        with example_col1:
            if st.button("SELECT basic"):
                sql_snippet = example_snippets["SELECT basic"]
                st.session_state.sql_snippet = sql_snippet
        with example_col2:
            if st.button("JOIN query"):
                sql_snippet = example_snippets["JOIN query"]
                st.session_state.sql_snippet = sql_snippet
        with example_col3:
            if st.button("GROUP BY"):
                sql_snippet = example_snippets["GROUP BY"]
                st.session_state.sql_snippet = sql_snippet

    with col2:
        st.subheader("⚡ Actions")

        # Autocomplete button
        autocomplete_button = st.button(
            "✨ Auto-Complete",
            use_container_width=True,
            type="primary",
            help="Click to auto-complete your SQL snippet",
        )

        st.markdown("---")

        st.markdown("**Status:** Ready")
        st.markdown("**Mode:** SQL Auto-Complete")

    # Execute autocomplete
    if autocomplete_button or (
        sql_snippet and "autocomplete_clicked" in st.session_state
    ):
        if not sql_snippet.strip():
            st.error("❌ Please enter a SQL snippet!")
        else:
            st.session_state.autocomplete_clicked = True

            with st.spinner("🤖 AI is auto-completing SQL... Please wait..."):
                try:
                    response = requests.post(
                        f"{api_base_url}/autocomplete",
                        json={"prompt": sql_snippet},
                        timeout=api_timeout,
                    )

                    if response.status_code == 200:
                        result = response.json()
                        completion = result.get("completion", "")

                        # Display success
                        st.markdown(
                            '<div class="success-box">✅ Auto-Complete Successful!</div>',
                            unsafe_allow_html=True,
                        )

                        # Display the input and completion
                        st.subheader("📋 Completed SQL Query")

                        # Show before and after
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Input:**")
                            st.code(sql_snippet, language="sql")
                        with col2:
                            st.write("**Completion:**")
                            st.code(completion, language="sql")

                        # Show full query
                        st.write("**Full Query:**")
                        full_query = sql_snippet + "\n" + completion
                        st.code(full_query, language="sql")

                        # Additional actions
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📋 Copy to Clipboard", key="copy_auto"):
                                st.write(
                                    "SQL copied to clipboard! (Note: Use external clipboard for actual copy)"
                                )
                        with col2:
                            if st.button("🔄 New Snippet", key="new_auto"):
                                st.rerun()
                        with col3:
                            st.download_button(
                                label="⬇️ Download SQL",
                                data=full_query,
                                file_name=f"autocomplete_query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql",
                                mime="text/sql",
                                key="download_auto",
                            )

                        # Show metadata
                        with st.expander("📊 Query Metadata"):
                            st.json(
                                {
                                    "input_snippet": sql_snippet,
                                    "completion": completion,
                                    "timestamp": datetime.now().isoformat(),
                                    "api_endpoint": f"{api_base_url}/autocomplete",
                                }
                            )

                    else:
                        error_data = response.json()
                        error_message = error_data.get("error", "Unknown error")
                        st.markdown(
                            f'<div class="error-box">❌ Error: {error_message}</div>',
                            unsafe_allow_html=True,
                        )
                        st.error(f"API Error: {error_message}")

                except requests.exceptions.Timeout:
                    st.error(
                        f"❌ Request timed out after {api_timeout} seconds. Try increasing timeout in settings."
                    )
                except requests.exceptions.ConnectionError:
                    st.error(
                        "❌ Failed to connect to API. Make sure the Flask app is running on "
                        f"{api_host}:{api_port}"
                    )
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

# ==================== TAB 3: DOCUMENTATION ====================
with tab3:
    st.header("📚 Documentation")

    st.markdown("## About This Application")
    st.markdown("""
    The AI SQL Editor is a demonstration of how modern AI can automate SQL query generation
    and completion. It leverages:
    - **LangChain**: For building LLM chains and prompt management
    - **Groq LLM**: For fast and accurate SQL generation
    - **Flask**: Backend API for processing requests
    - **Streamlit**: User-friendly web interface
    
    ### Key Features
    
    **1. SQL Generation from Natural Language**
    - Convert plain English descriptions to Oracle SQL queries
    - Automatically extracts database schema context
    - Optimized for Oracle-specific SQL syntax
    
    **2. SQL Auto-Completion**
    - Start typing SQL and let AI complete it
    - Context-aware completions based on schema
    - Supports complex queries and joins
    
    ### API Endpoints
    
    **Generate SQL**
    - **Endpoint:** `POST /api/sql/generate`
    - **Input:** `{"instruction": "natural language instruction"}`
    - **Output:** `{"sql": "generated Oracle SQL"}`
    - **Example:** "Get all active users" → `SELECT * FROM users WHERE status = 'active'`
    
    **Auto-Complete SQL**
    - **Endpoint:** `POST /api/sql/autocomplete`
    - **Input:** `{"prompt": "SELECT * FROM"}`
    - **Output:** `{"completion": "rest of the SQL"}`
    - **Example:** "SELECT * FROM" → Completes with appropriate columns and conditions
    
    ### How It Works
    
    1. **User Input**: You provide either a natural language instruction or a SQL snippet
    2. **Schema Context**: The API retrieves and caches the Oracle database schema
    3. **AI Processing**: LangChain chains your input with the schema context and sends it to Groq LLM
    4. **SQL Generation**: The model generates valid Oracle SQL based on your request
    5. **Result Display**: The generated SQL is cleaned and returned to the UI
    
    ### Supported SQL Features
    
    - **Oracle Pagination**: FETCH FIRST N ROWS ONLY or ROWNUM
    - **Date Functions**: SYSDATE for current timestamps
    - **String Operations**: || for concatenation
    - **Complex Queries**: JOINs, GROUP BY, ORDER BY, subqueries
    - **Filtering**: WHERE clauses with multiple conditions
    
    ### Tips for Best Results
    
    ✅ **Do:**
    - Be specific in your natural language instructions
    - Use clear column and table names
    - Mention sorting and filtering requirements
    - Specify the number of rows you want (e.g., "top 10")
    
    ❌ **Avoid:**
    - Ambiguous or vague descriptions
    - Non-existent table or column names
    - Unclear sorting preferences
    
    ### Example Queries
    """)

    # Create example queries table
    example_queries = {
        "Natural Language": [
            "Get the top 5 products by sales this month",
            "Find all customers who haven't made a purchase in 90 days",
            "List employees in the IT department with salary above 100k",
            "Show monthly revenue trends for the current year",
        ],
        "SQL Snippet": [
            "SELECT * FROM orders WHERE order_date >",
            "SELECT department, COUNT(*) FROM employees GROUP BY",
            "SELECT u.name, o.order_id FROM users u LEFT JOIN",
        ],
    }

    st.markdown("#### Example Queries You Can Try")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Natural Language Examples:**")
        for i, query in enumerate(example_queries["Natural Language"], 1):
            st.markdown(f"{i}. {query}")

    with col2:
        st.markdown("**SQL Snippet Examples:**")
        for i, snippet in enumerate(example_queries["SQL Snippet"], 1):
            st.markdown(f"{i}. `{snippet}`...")

    st.markdown("---")

    st.markdown("### Troubleshooting")

    with st.expander("❌ Connection Error"):
        st.markdown("""
        **Problem:** "Cannot connect to API"
        
        **Solutions:**
        1. Ensure Flask app is running: `python flask_app.py`
        2. Check API host and port in sidebar settings
        3. Make sure Flask is listening on the correct port (default: 5002)
        4. Check if firewall is blocking the connection
        """)

    with st.expander("⏱️ Timeout Error"):
        st.markdown("""
        **Problem:** "Request timed out"
        
        **Solutions:**
        1. Increase timeout value in sidebar settings
        2. Check if the LLM service is responding
        3. Verify internet connection (Groq API requires connectivity)
        4. Try a simpler query first
        """)

    with st.expander("❌ SQL Generation Error"):
        st.markdown("""
        **Problem:** "Error generating SQL"
        
        **Solutions:**
        1. Check the error message returned by API
        2. Verify database schema is accessible
        3. Try a more specific natural language instruction
        4. Check server logs for detailed error information
        """)

    st.markdown("---")
    st.markdown(
        "Built with ❤️ using LangChain, Groq, Flask, and Streamlit | "
        "[View Source Code](https://github.com)"
    )
