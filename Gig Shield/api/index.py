import os
import sys
from dotenv import load_dotenv

# Ensure the project root is on sys.path when Vercel imports this file.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from app import app
application = app

load_dotenv()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)

