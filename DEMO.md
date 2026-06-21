# Demo Video Script - 5 Minutes

## Introduction (30 seconds)
Hello, this is a Repository-Aware RAG Assistant. It ingests code repositories and answers natural language questions with source references.

## Part 1: Ingestion (1 minute)
1. Show the test repository:
   `cat test_repo/test.py`
   `cat test_repo/README.md`

2. Ingest the repository:
   `python ingestion_script.py test_repo`

3. Show database statistics:
   `python -c "from assistant import RAGAssistant; a=RAGAssistant(); print(a.vector_store.count())"`

## Part 2: CLI Interface (1.5 minutes)
1. Run CLI:
   `python ui/cli.py`

2. Ask questions:
   - "What files are in this repository?"
   - "What does the hello_world function do?"
   - "How does the Calculator class work?"

3. Show source references in answers

## Part 3: Web UI Interface (1.5 minutes)
1. Run Web UI:
   `streamlit run ui/web.py`

2. Show the browser interface:
   - Sidebar with stats
   - Chat interface
   - Example questions

3. Ask same questions in Web UI

## Part 4: Features Summary (30 seconds)
- Multi-language parsing
- Syntax-aware chunking
- Hybrid search (semantic + BM25)
- LLM integration with Ollama
- Source references in answers
- Both CLI and Web interfaces

## Conclusion (30 seconds)
The RAG Assistant successfully answers questions about code repositories with accurate, contextual responses and source references.
