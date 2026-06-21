#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from assistant import RAGAssistant

def main():
    print("=" * 60)
    print(" Repository-Aware RAG Assistant - CLI")
    print("=" * 60)
    print("\nCommands:")
    print("  /help    - Show this help")
    print("  /stats   - Show database statistics")
    print("  /quit    - Exit")
    print("  /ingest  - Ingest a new repository")
    print("\n" + "=" * 60)
    
    assistant = RAGAssistant()
    
    if assistant.vector_store.count() == 0:
        print("\n  Vector database is empty!")
        print("Run: python ingestion_script.py /path/to/repo")
        print("\nOr type '/ingest' to ingest a repository now")
    
    while True:
        try:
            question = input("\n Ask a question: ").strip()
            
            if not question:
                continue
            
            if question.lower() == '/quit':
                print("Goodbye! ")
                break
            
            elif question.lower() == '/help':
                print("\nExample questions:")
                print("  - Where is the main function?")
                print("  - How do I use the API?")
                print("  - What classes handle authentication?")
                continue
            
            elif question.lower() == '/stats':
                count = assistant.vector_store.count()
                print(f"\n Database contains {count} code chunks")
                continue
            
            elif question.lower() == '/ingest':
                repo_path = input("Enter repository path: ").strip()
                if Path(repo_path).exists():
                    assistant.ingest_repository(repo_path)
                else:
                    print(f" Path not found: {repo_path}")
                continue
            
            answer = assistant.ask(question)
            print(f"\n Answer:\n{answer}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n Error: {e}")

if __name__ == "__main__":
    main()
