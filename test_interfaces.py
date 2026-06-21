import subprocess
import sys

print("Testing both interfaces...")

print("\n1. Testing CLI interface:")
print("   Run: python ui/cli.py")
print("   (Type '/quit' to exit)")

print("\n2. Testing Web UI interface:")
print("   Run: streamlit run ui/web.py")
print("   (Open http://localhost:8501 in browser)")

print("\nTo run both:")
print("  Terminal 1: python ui/cli.py")
print("  Terminal 2: streamlit run ui/web.py")
