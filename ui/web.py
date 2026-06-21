import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from local_llm import OllamaLLM
from assistant import RAGAssistant

def force_ollama(self):
    return OllamaLLM()

RAGAssistant._setup_llm = force_ollama

st.set_page_config(
    page_title="Repository RAG Assistant",
    page_icon="book",
    layout="wide"
)

st.title("Repository-Aware RAG Assistant")
st.markdown("Ask questions about your code repository and get answers with source references.")

@st.cache_resource
def get_assistant():
    return RAGAssistant()

assistant = get_assistant()

with st.sidebar:
    st.header("Repository Info")
    chunk_count = assistant.vector_store.count()
    st.metric("Total Chunks", chunk_count)
    
    if chunk_count == 0:
        st.warning("No data in vector database. Please run ingestion first:")
        st.code("python ingestion_script.py /path/to/repo")
    
    st.header("Commands")
    col1, col2 = st.columns(2)
    if col1.button("Show Stats"):
        st.session_state.show_stats = True
    if col2.button("Clear Data"):
        if st.button("Confirm Clear"):
            assistant.vector_store.delete_all()
            st.success("Database cleared!")
            st.rerun()
    
    st.header("Example Questions")
    example_questions = [
        "What files are in this repository?",
        "What does the hello_world function do?",
        "How does the Calculator class work?",
        "Show me the divide method",
        "What is the main function?"
    ]
    for q in example_questions:
        if st.button(q, use_container_width=True):
            st.session_state.question = q
            st.session_state.ask_question = True
            st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "ask_question" not in st.session_state:
    st.session_state.ask_question = False
if "question" not in st.session_state:
    st.session_state.question = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question about your code...")

if prompt:
    st.session_state.ask_question = False
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = assistant.ask(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
    st.rerun()

elif st.session_state.ask_question and st.session_state.question:
    q = st.session_state.question
    st.session_state.ask_question = False
    st.session_state.messages.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.markdown(q)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = assistant.ask(q)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
    st.rerun()

if st.session_state.get("show_stats", False):
    with st.expander("Database Statistics"):
        st.write(f"Total chunks: {chunk_count}")
        if chunk_count > 0:
            import chromadb
            client = chromadb.PersistentClient(path='vector_db')
            collection = client.get_collection('code_chunks')
            results = collection.get(include=['metadatas'])
            files = set()
            for meta in results['metadatas']:
                files.add(meta.get('file_path', 'unknown'))
            st.write("Files in database:")
            for f in files:
                st.write(f"- {f}")
    st.session_state.show_stats = False

st.sidebar.markdown("---")
st.sidebar.caption("Built with LangChain, ChromaDB, and Ollama")
