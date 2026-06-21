# Repository-Aware RAG Assistant

Ask natural language questions about any code repository and get accurate answers with source references.

## Quick Start

### 1. Install Dependencies
` ` `bash
pip install -r requirements.txt
` ` `

### 2. Download Sample Repository
` ` `bash
git clone https://github.com/fastapi/fastapi.git sample_repo
` ` `

### 3. Ingest the Repository
` ` `bash
python ingestion_script.py sample_repo
` ` `

### 4. Run the Assistant
` ` `bash
python ui/cli.py
` ` `

## Example Questions

- "Where is the routing logic?"
- "How do I add a new endpoint?"
- "What classes handle authentication?"

## Features

-  Multi-language code parsing
-  Smart chunking by functions
-  Hybrid search (semantic + keyword)
-  CLI interface

## License

MIT

## Running the Web Interface

```bash
streamlit run ui/web.py
```

Then open http://localhost:8501 in your browser.

## Running the CLI Interface

```bash
python ui/cli.py
```
