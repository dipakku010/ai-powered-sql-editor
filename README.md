# 🚀 AI SQL Editor - Intelligent Oracle SQL Generation with LLM

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask 2.0+](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2.0%2B-orange.svg)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.52%2B-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)

**Transform natural language into production-ready Oracle SQL queries using AI-powered LLM**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API](#-api-reference) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [API Reference](#-api-reference)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Advanced Usage](#-advanced-usage)
- [Performance Optimization](#-performance-optimization)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## Overview

**AI SQL Editor** is an intelligent SQL generation platform that leverages state-of-the-art Large Language Models (LLM) to automatically generate and complete Oracle SQL queries from natural language instructions. It combines the power of **LangChain**, **Groq LLM**, and a user-friendly **Streamlit** web interface with a production-grade **Flask API** backend.

### Why AI SQL Editor?

- 🤖 **No Manual Query Writing**: Describe what you need in plain English
- ⚡ **Lightning Fast**: Powered by Groq's fastest open-source LLM models
- 🎯 **Oracle Optimized**: Generates Oracle-specific SQL syntax automatically
- 🔄 **Smart Completion**: Auto-complete SQL snippets with context awareness
- 🛡️ **Production Ready**: Fully tested API with comprehensive error handling
- 🎨 **Beautiful UI**: Intuitive Streamlit interface for seamless interaction
- 📊 **Schema-Aware**: Understands your database schema for accurate queries
- ✅ **Battle-Tested**: Built with industry-standard frameworks and libraries

---

## ✨ Features

### Core Features

✅ **SQL Generation from Natural Language**

- Convert English descriptions to Oracle SQL queries
- Context-aware query generation using database schema
- Support for complex queries: JOINs, aggregations, filtering, sorting
- Automatic Oracle dialect optimization

✅ **SQL Auto-Completion**

- Intelligent SQL snippet completion
- Context and schema-aware suggestions
- Supports all SQL query types
- Instant feedback and previews

✅ **REST API**

- Production-grade Flask API
- Two well-documented endpoints
- JSON request/response format
- Comprehensive error handling
- Built-in caching for performance

✅ **Web Interface (Streamlit)**

- Beautiful, responsive UI
- Real-time SQL generation
- Query export (SQL, JSON)
- Connection status monitoring
- Integrated documentation
- Quick example buttons
- Query history and metadata

✅ **Database Integration**

- Automatic Oracle schema extraction
- Intelligent schema caching (1-hour default)
- Support for complex database structures
- Multiple table and view handling

✅ **Performance Features**

- Schema caching with configurable timeout
- Request timeout management
- Optimized LLM prompts
- Batch processing ready
- In-memory caching

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Layer                               │
├─────────────────────────────────────────────────────────────┤
│  Streamlit Web Interface (streamlit_ui.py)                 │
│  ├─ SQL Generation Tab                                     │
│  ├─ SQL Auto-Complete Tab                                  │
│  └─ Documentation & Help                                   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    API Layer                                │
├─────────────────────────────────────────────────────────────┤
│  Flask Application (flask_app.py)                          │
│  ├─ /api/sql/generate      (POST)                          │
│  ├─ /api/sql/autocomplete  (POST)                          │
│  └─ /hello                 (GET - Health Check)            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 Processing Layer                            │
├─────────────────────────────────────────────────────────────┤
│  AI SQL Editor (ai_sql_editor.py)                          │
│  ├─ LLM Chain Construction                                 │
│  ├─ Prompt Engineering                                     │
│  ├─ Response Parsing                                       │
│  └─ Schema Context Management                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 LLM & Database Layer                        │
├─────────────────────────────────────────────────────────────┤
│  LangChain (Prompt Templates, Output Parsing)             │
│  Groq LLM API (openai/gpt-oss-120b model)                 │
│  Oracle Database (Schema Extraction)                       │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Input (Natural Language or SQL Snippet)
         ↓
  Streamlit UI / HTTP Request
         ↓
  Flask API Validation
         ↓
  LangChain Chain Construction
         ↓
  Schema Context Retrieval (from cache or DB)
         ↓
  Groq LLM API Call
         ↓
  Response Parsing & Cleaning
         ↓
  JSON Response to Client
         ↓
  Display in UI / Return to Caller
```

---

## 📋 Prerequisites

### System Requirements

- **OS**: macOS, Linux, or Windows (with WSL2)
- **Python**: 3.8 or higher
- **Memory**: Minimum 2GB RAM (4GB recommended)
- **Internet**: Required for Groq API connectivity

### Required Accounts & Credentials

- **Groq API Key**: Get it from [Groq Console](https://console.groq.com)
- **Oracle Database**: Access to Oracle 11g or later (for schema extraction)

### Dependencies

- Python 3.8+
- Flask 2.0+
- LangChain 1.2+
- Streamlit 1.52+
- Groq SDK

---

## 🛠️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-sql-editor.git
cd ai-sql-editor
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Groq API Configuration
GROQ_API_KEY=your-groq-api-key-here

# Oracle Database Configuration (optional, if using Oracle)
ORACLE_HOST=your-oracle-host
ORACLE_PORT=1521
ORACLE_USER=your-oracle-user
ORACLE_PASSWORD=your-oracle-password
ORACLE_SID=your-oracle-sid

# Flask Configuration (optional)
FLASK_DEBUG=False
FLASK_ENV=production
```

**Security Note**: Never commit `.env` file. Add it to `.gitignore`.

### Step 5: Verify Installation

```bash
python3 -c "import streamlit, flask, langchain_groq, requests; print('✅ All dependencies installed successfully!')"
```

---

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)

```bash
# Make the script executable
chmod +x quickstart.sh

# Run the script (starts both Flask and Streamlit)
./quickstart.sh
```

### Option 2: Manual Startup (Two Terminals)

**Terminal 1 - Start Flask API:**

```bash
cd workspace
python3 flask_app.py
```

You should see:

```
 * Serving Flask app 'flask_app'
 * Running on http://0.0.0.0:5002
 * Debug mode: on
```

**Terminal 2 - Start Streamlit UI:**

```bash
streamlit run streamlit_ui.py
```

Streamlit will automatically open in your browser at `http://localhost:8501`

### Option 3: Using Docker (Coming Soon)

```bash
docker build -t ai-sql-editor .
docker run -p 5002:5002 -p 8501:8501 -e GROQ_API_KEY=$GROQ_API_KEY ai-sql-editor
```

---

## 📖 Usage Guide

### 🔨 Generate SQL from Natural Language

1. **Open the Streamlit UI** at `http://localhost:8501`
2. **Navigate to "🔨 Generate SQL" tab**
3. **Enter your requirement** in natural English:
   ```
   Get the top 10 customers by total purchase amount in the last year
   ```
4. **Click "🚀 Generate SQL" button**
5. **Review the generated query** in the code display
6. **Export**: Download SQL file or copy to clipboard

#### Example Queries

```
"Fetch all active users registered in the last 30 days sorted by registration date"
↓
SELECT user_id, username, email, registration_date
FROM users
WHERE status = 'active'
  AND registration_date >= TRUNC(SYSDATE) - 30
ORDER BY registration_date DESC
```

```
"Show total sales revenue grouped by region for the current year"
↓
SELECT region, SUM(order_amount) as total_revenue, COUNT(*) as order_count
FROM orders
WHERE YEAR(order_date) = YEAR(SYSDATE)
GROUP BY region
ORDER BY total_revenue DESC
```

---

### ✨ Auto-Complete SQL Snippets

1. **Navigate to "✨ Auto-Complete" tab**
2. **Enter a SQL snippet**:
   ```sql
   SELECT * FROM customers WHERE
   ```
3. **Click "✨ Auto-Complete" button**
4. **Review the completion**:
   ```sql
   status = 'active'
   AND created_date >= TRUNC(SYSDATE) - 90
   ORDER BY created_date DESC FETCH FIRST 100 ROWS ONLY
   ```
5. **Export or refine** as needed

---

### 🔌 Use the REST API

#### Generate SQL

```bash
curl -X POST http://127.0.0.1:5002/api/sql/generate \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "Get top 10 products by sales this month"
  }'
```

**Response:**

```json
{
	"sql": "SELECT product_id, product_name, SUM(quantity) as total_sales FROM products p JOIN order_items oi ON p.product_id = oi.product_id WHERE order_date >= TRUNC(SYSDATE, 'MM') GROUP BY product_id, product_name ORDER BY total_sales DESC FETCH FIRST 10 ROWS ONLY"
}
```

#### Auto-Complete SQL

```bash
curl -X POST http://127.0.0.1:5002/api/sql/autocomplete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "SELECT id, name, email FROM users WHERE"
  }'
```

**Response:**

```json
{
	"completion": "status = 'active' ORDER BY created_at DESC FETCH FIRST 100 ROWS ONLY"
}
```

---

## 🔗 API Reference

### Base URL

```
http://127.0.0.1:5002/api/sql
```

### Endpoints

#### 1. Generate SQL from Natural Language

**Endpoint**: `POST /api/sql/generate`

**Request**:

```json
{
	"instruction": "string - Your natural language instruction"
}
```

**Response** (200 OK):

```json
{
	"sql": "Generated Oracle SQL query"
}
```

**Response** (400/500 Error):

```json
{
	"error": "Error description"
}
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| instruction | string | Yes | Natural language description of the SQL you need |

**Examples**:

- "Get all customers who made purchases in the last 30 days"
- "Show total revenue by product category"
- "List employees with salary above 100000 sorted by department"

**Curl Example**:

```bash
curl -X POST http://127.0.0.1:5002/api/sql/generate \
  -H "Content-Type: application/json" \
  -d '{"instruction": "Get top 5 customers"}'
```

---

#### 2. Auto-Complete SQL Query

**Endpoint**: `POST /api/sql/autocomplete`

**Request**:

```json
{
	"prompt": "string - Partial SQL query"
}
```

**Response** (200 OK):

```json
{
	"completion": "Remaining SQL to complete the query"
}
```

**Response** (400/500 Error):

```json
{
	"error": "Error description"
}
```

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| prompt | string | Yes | Partial SQL query to be completed |

**Examples**:

- "SELECT \* FROM users WHERE"
- "SELECT department, COUNT(\*) FROM employees GROUP BY"
- "SELECT u.id, o.order_id FROM users u JOIN orders o"

**Curl Example**:

```bash
curl -X POST http://127.0.0.1:5002/api/sql/autocomplete \
  -H "Content-Type: application/json" \
  -d '{"prompt": "SELECT * FROM customers WHERE"}'
```

---

#### 3. Health Check

**Endpoint**: `GET /hello`

**Response** (200 OK):

```json
{
	"message": "Hello, World!"
}
```

**Use**: Check if API is running and responsive

---

## ⚙️ Configuration

### API Server Configuration

**File**: `workspace/flask_app.py`

```python
# Change these settings as needed
app.run(
    host="0.0.0.0",    # Listen on all interfaces
    port=5002,          # Port number
    debug=True          # Debug mode (disable in production)
)
```

### LLM Model Configuration

**File**: `workspace/ai_sql_editor.py`

```python
llm = ChatGroq(
    model="openai/gpt-oss-120b",  # LLM model
    temperature=0.3,               # Lower = more deterministic
    max_tokens=1024,              # Max output length
    timeout=60,                   # Request timeout
    max_retries=2,                # Retry attempts
)
```

**Available Models**:

- `openai/gpt-oss-120b` - Largest, most capable (default)
- `llama-3.3-70b-versatile` - Balanced performance
- `llama-3.1-8b-instant` - Ultra-fast, low-latency

### Caching Configuration

**File**: `workspace/ai_sql_editor.py`

```python
cache_config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 3600,  # 1 hour in seconds
}
```

### Streamlit Configuration

**File**: `~/.streamlit/config.toml` (optional)

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#F5F5F5"
secondaryBackgroundColor = "#E8E8E8"
textColor = "#262730"

[browser]
gatherUsageStats = false

[server]
port = 8501
headless = true
```

---

## 📁 Project Structure

```
ai-sql-editor/
├── streamlit_ui.py              # Streamlit web interface
├── flask_app.py                 # Flask API entry point
├── quickstart.sh                # Automated startup script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .env.example                 # Environment variables template
└── workspace/
    ├── ai_sql_editor.py         # Core AI SQL generation logic
    ├── flask_app.py             # Flask application setup
    ├── oracle_schema_extractor.py    # Database schema extraction
    ├── llm_schema_prompt.py          # Schema formatting utilities
    └── oracle_schema_extractor_query.sql  # Oracle query for schema
```

### Key Files Explained

| File                                   | Purpose                                   |
| -------------------------------------- | ----------------------------------------- |
| `streamlit_ui.py`                      | Interactive web interface (Streamlit app) |
| `flask_app.py`                         | REST API server (Flask application)       |
| `workspace/ai_sql_editor.py`           | Core LLM logic and SQL generation chains  |
| `workspace/oracle_schema_extractor.py` | Fetches database schema metadata          |
| `quickstart.sh`                        | Convenience script to start all services  |

---

## 🎯 Advanced Usage

### 1. Integration with Other Applications

**Python Client Example**:

```python
import requests

def generate_sql(instruction):
    response = requests.post(
        "http://127.0.0.1:5002/api/sql/generate",
        json={"instruction": instruction},
        timeout=30
    )
    return response.json()

# Usage
query = generate_sql("Get all orders placed today")
print(query["sql"])
```

**JavaScript/Node.js Example**:

```javascript
async function generateSQL(instruction) {
	const response = await fetch('http://127.0.0.1:5002/api/sql/generate', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ instruction }),
	})
	return response.json()
}

// Usage
const query = await generateSQL('Get top 10 products by revenue')
console.log(query.sql)
```

### 2. Batch Processing

```python
instructions = [
    "Get active users",
    "Show revenue by region",
    "List recent orders"
]

for instruction in instructions:
    result = generate_sql(instruction)
    print(f"Instruction: {instruction}")
    print(f"SQL: {result['sql']}\n")
```

### 3. Custom Prompt Engineering

Modify `workspace/ai_sql_editor.py` to adjust the system prompt:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Oracle SQL expert...
    Your custom instructions here...
    """),
    ("human", "{user_input}")
])
```

### 4. Database Integration

Execute generated queries directly:

```python
import cx_Oracle

def generate_and_execute(instruction):
    # Generate SQL
    result = generate_sql(instruction)
    sql = result["sql"]

    # Execute
    connection = cx_Oracle.connect("user/password@database")
    cursor = connection.cursor()
    cursor.execute(sql)

    # Fetch results
    rows = cursor.fetchall()
    return rows
```

---

## 🚄 Performance Optimization

### 1. Schema Caching Strategy

The schema is cached for 1 hour by default:

```python
# First request: ~5-10 seconds (fetches schema)
# Subsequent requests: <1 second (uses cache)
```

To adjust cache timeout:

```python
# In ai_sql_editor.py
cache_config = {
    "CACHE_DEFAULT_TIMEOUT": 7200  # 2 hours
}
```

### 2. Request Timeout Management

In Streamlit UI sidebar:

- Set appropriate timeout based on your network speed
- Higher timeout for complex queries (60-120 seconds)
- Lower timeout for quick responses (10-30 seconds)

### 3. Model Selection for Speed

For faster responses, use a smaller model:

```python
# In ai_sql_editor.py
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Ultra-fast
    # ... other config
)
```

**Speed Comparison**:
| Model | Speed | Quality |
|-------|-------|---------|
| llama-3.1-8b-instant | ⚡⚡⚡ | ⭐⭐⭐ |
| llama-3.3-70b | ⚡⚡ | ⭐⭐⭐⭐ |
| gpt-oss-120b | ⚡ | ⭐⭐⭐⭐⭐ |

### 4. Temperature Tuning

Lower temperature = faster, more deterministic responses:

```python
# More deterministic (faster)
temperature=0.1

# More creative (slower, more variable)
temperature=0.9
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### ❌ "Cannot connect to API"

**Cause**: Flask server is not running or unreachable

**Solution**:

```bash
# Check if Flask is running
ps aux | grep flask_app.py

# Start Flask if not running
cd workspace && python3 flask_app.py

# Check if port 5002 is in use
lsof -i :5002
```

---

#### ⏱️ "Request timed out"

**Cause**: Query is taking too long or network is slow

**Solution**:

1. Increase timeout in Streamlit sidebar (up to 120 seconds)
2. Verify Groq API is accessible: `ping api.groq.com`
3. Try a simpler instruction first
4. Check server logs for errors

---

#### ❌ "GROQ_API_KEY not set"

**Cause**: Environment variable is missing

**Solution**:

```bash
# Set Groq API key
export GROQ_API_KEY="your-api-key"

# Verify it's set
echo $GROQ_API_KEY

# Then start the app
python3 flask_app.py
```

---

#### ❌ "Oracle connection failed"

**Cause**: Database credentials or connection settings are incorrect

**Solution**:

1. Check `.env` file for correct Oracle connection details
2. Verify Oracle database is running and accessible
3. Test connection manually:
   ```bash
   sqlplus username/password@hostname:port/sid
   ```
4. Check firewall rules allow connection to port 1521

---

#### 🚨 "Module not found" error

**Cause**: Dependencies not installed correctly

**Solution**:

```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt

# Verify specific package
python3 -c "import streamlit; print(streamlit.__version__)"
```

---

#### 📊 "Empty or incomplete SQL response"

**Cause**: LLM generated partial output or malformed response

**Solution**:

1. The app automatically strips markdown and cleans output
2. Try a more specific, detailed instruction
3. Break complex queries into simpler parts
4. Check server logs for LLM response details

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

### Getting Started

1. **Fork the repository**

   ```bash
   git clone https://github.com/yourusername/ai-sql-editor.git
   cd ai-sql-editor
   ```

2. **Create a feature branch**

   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation

4. **Commit your changes**

   ```bash
   git commit -m 'feat: Add amazing feature'
   ```

5. **Push to the branch**

   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Describe your changes
   - Link any related issues
   - Add screenshots if UI changes

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Check code style
pylint workspace/

# Format code
black .
```

### Areas for Contribution

- 🐛 **Bug Fixes**: Report and fix issues
- ✨ **Features**: Query history, execution preview, more databases
- 📚 **Documentation**: Better guides, examples, tutorials
- 🧪 **Tests**: Unit tests, integration tests
- 🌍 **Localization**: Support for multiple languages
- 🎨 **UI/UX**: Improve interface and user experience
- 📦 **Packaging**: Docker, Kubernetes support

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 AI SQL Editor Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 💬 Support

### Getting Help

- **📖 Documentation**: Check [README_STREAMLIT.md](README_STREAMLIT.md) for detailed guides
- **🐛 Issues**: Search [GitHub Issues](https://github.com/yourusername/ai-sql-editor/issues)
- **💡 Discussions**: Join our [GitHub Discussions](https://github.com/yourusername/ai-sql-editor/discussions)
- **📧 Email**: support@example.com

### Frequently Asked Questions

**Q: Can I use this with other databases (MySQL, PostgreSQL)?**
A: Currently optimized for Oracle. Contributions welcome for other databases!

**Q: Does this require an internet connection?**
A: Yes, for Groq API calls. Caching reduces repeated calls.

**Q: Is my data sent to Groq?**
A: Yes, your instructions and schema are sent to Groq LLM for processing. For sensitive data, use on-premise solutions.

**Q: Can I run this offline?**
A: Not currently, as it requires Groq API connectivity. Local LLM support coming soon.

**Q: What's the cost?**
A: Free for Groq's community tier. Check [Groq Pricing](https://groq.com/pricing) for details.

---

## 🙏 Acknowledgments

This project stands on the shoulders of amazing open-source projects:

- **[LangChain](https://www.langchain.com/)** - LLM orchestration framework
- **[Groq](https://groq.com/)** - Fast LLM inference engine
- **[Flask](https://flask.palletsprojects.com/)** - Web framework
- **[Streamlit](https://streamlit.io/)** - Data app framework
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation

Special thanks to all [contributors](https://github.com/yourusername/ai-sql-editor/graphs/contributors) who have helped shape this project.

---

## 🌟 Star History

If you find this project helpful, please consider giving it a star! ⭐

```
        |
   ⭐ ⭐ | ⭐
   ⭐   | ⭐  ⭐
   ⭐ ⭐ | ⭐ ⭐ ⭐
  _____|___________
  2024-11 2024-12 2025-01
```

---

## 📞 Contact & Social

- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Twitter**: [@yourusername](https://twitter.com/yourusername)
- **LinkedIn**: [Your Name](https://linkedin.com/in/yourname)

---

<div align="center">

**Made with ❤️ for the Developer Community**

[⬆ Back to Top](#-ai-sql-editor---intelligent-oracle-sql-generation-with-llm)

</div>
