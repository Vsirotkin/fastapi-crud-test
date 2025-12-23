# fastapi-crud-test
✅ FastAPI CRUD Service for AI IDE BAS Integration Test (на английском, профессиональный стиль)
This repository contains a minimal FastAPI service implementing a full CRUD interface over a SQLite database, integrated with the AI IDE BAS VS Code extension as part of a technical evaluation task.

✅ Requirements
Python ≥ 3.13
uv (recommended) or pip/venv
Node.js ≥ 18 (for running the AI IDE BAS extension in dev mode)
VS Code (for extension debugging)
🚀 Features Implemented
RESTful API with 4 standard CRUD endpoints for the Item entity:
POST /items – create a new item
GET /items – list all items
GET /items/{id} – retrieve a single item by ID
PUT /items/{id} – update an existing item
DELETE /items/{id} – delete an item
Persistent storage using SQLite (file: test.db)
CORS middleware enabled for all origins (required for Webview communication)
Self-contained project with dependency management via uv
📦 Installation & Setup
1. Clone and initialize the FastAPI service
git clone https://github.com/your-username/fastapi-crud-test.git
cd fastapi-crud-test
uv venv
source .venv/bin/activate  # Linux/macOS
# .\.venv\Scripts\activate  # Windows (CMD)
uv add "fastapi>=0.127.0" "uvicorn[standard]>=0.34.0"
2. Run the API server
make run
# or directly:
uvicorn main:app --reload
The service will be available at http://localhost:8000.
Interactive documentation: http://localhost:8000/docs.

3. Integrate with AI IDE BAS extension
Note: This step is performed in the AI IDE BAS repository.

Clone the extension:

git clone https://github.com/dradns/AI-IDE-BAS.git
cd AI-IDE-BAS/ai_ide_bas_main
Install dependencies:

pnpm install
In src/core/webview/ClineProvider.ts, the following modifications were made:

Added a fixed-position button to the HTML body in both getHtmlContent() and getHMRHtmlContent() methods.
Injected an inline script (with proper CSP nonce) that sends a POST request to http://localhost:8000/items on click.
Extended the Content Security Policy (connect-src) to allow requests to http://localhost:8000.
Start the Vite development server for the Webview UI:

pnpm --filter webview-ui dev
Launch the extension in debug mode from VS Code (F5).

Open the AI IDE BAS panel → click the "🚀 Отправить в FastAPI" button.

🔍 Verification
Upon button click:

The extension sends a JSON payload to POST /items.
The FastAPI server logs the request and persists the record in test.db.
Success is confirmed by:
HTTP 200 response
New entry in the items table
Visual feedback via button press effect (onmousedown/onmouseup)
Example record:

{
  "name": "Test from AI IDE BAS",
  "description": "Sent via custom button in VS Code extension"
}
🗂 Project Structure
.
├── main.py            # FastAPI application with CRUD logic and SQLite integration
├── Makefile           # Convenient `make run` target
├── pyproject.toml     # Project metadata and dependencies
└── .gitignore         # Excludes virtual env, DB file, and IDE files
📝 Notes
The SQLite database (test.db) is created automatically on first run in the project root.
CORS is intentionally permissive (allow_origins=["*"]) to support local Webview integration.
The button and script are injected directly into the Webview HTML to avoid modifying the React application.
🧪 Testing
You can test the API independently using curl:

curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Integration test","description":"From curl"}'
✉️ Author
Technical test implementation for AI IDE BAS integration challenge.


---
It works! 🚀