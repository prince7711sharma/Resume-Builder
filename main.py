import sys
import os
import traceback

# Force current directory into path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("--- DEBUG: Attempting to import app.main ---")
    from app.main import app
    print("--- DEBUG: Import successful ---")
except Exception as e:
    print("--- DEBUG: IMPORT FAILED! ---")
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
