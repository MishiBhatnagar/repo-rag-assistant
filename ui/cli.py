#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from local_llm import OllamaLLM
from assistant import RAGAssistant

# Force Ollama
def force_ollama(self):
    print("Using Ollama (local LLM)")
    return OllamaLLM()

RAGAssistant._setup_llm = force_ollama

def main():
    print("=" * 60)
    print("Repository-Aware RAG Assistant - CLI")
    print("=" * 60)
    print("\nCommands:")
    print("  /help    - Show this help")
    print("  /stats   - Show database statistics")
    print("  /quit    - Exit")
    print("  /ingest  - Ingest a new repository")
    print("\n" + "=" * 60)
    
    assistant = RAGAssistant()
    
    if assistant.vector_store.count() == 0:
        print("\nWarning: Vector database is empty!")
        print("Run: python ingestion_script.py /path/to/repo")
    
    while True:
        try:
            question = input("\nAsk a question: ").strip()
            
            if not question:
                continue
            
            if question.lower() == '/quit':
                print("Goodbye!")
                break
            
            elif question.lower() == '/help':
                print("\nExample questions:")
                print("  - Where is the main function?")
                print("  - How do I use the API?")
                print("  - What classes handle authentication?")
                print("  - Show me the calculator methods")
                continue
            
            elif question.lower() == '/stats':
                count = assistant.vector_store.count()
                print(f"\nDatabase contains {count} code chunks")
                continue
            
            elif question.lower() == '/ingest':
                repo_path = input("Enter repository path: ").strip()
                if Path(repo_path).exists():
                    assistant.ingest_repository(repo_path)
                else:
                    print(f"Path not found: {repo_path}")
                continue
            
            answer = assistant.ask(question)
            print(f"\nAnswer:\n{answer}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
