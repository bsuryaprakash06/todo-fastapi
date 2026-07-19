# Todo FastAPI

A clean, minimal, and fully functional REST API for managing tasks, built with FastAPI. This project focuses on excellent documentation, sensible folder structure, and consistent error handling without unnecessary over-engineering.

## Features

- **CRUD Operations:** Create, Read, Update, and Delete tasks.
- **Search & Filtering:** Search for tasks by title using a query parameter.
- **Statistics:** View total, completed, and pending task counts.
- **Data Validation:** Pydantic models ensure valid input (e.g., non-empty titles).
- **Interactive Documentation:** Beautiful Swagger UI (`/docs`) out of the box.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bsuryaprakash06/todo-fastapi.git
   cd todo-fastapi
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000). You can view the interactive documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoint Table

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns a welcome message. |
| `GET` | `/health` | Server health check. |
| `GET` | `/tasks` | Retrieves all tasks. Accepts optional `?search=` query. |
| `GET` | `/tasks/{id}` | Retrieves a single task by its ID. |
| `POST` | `/tasks` | Creates a new task. |
| `PUT` | `/tasks/{id}` | Updates an existing task's title or status. |
| `DELETE` | `/tasks/{id}` | Permanently deletes a task. |
| `GET` | `/stats` | Returns total, completed, and pending task statistics. |

## Interactive Documentation

FastAPI automatically generates an interactive Swagger UI for the API endpoints. You can view it by navigating to `/docs` in your browser.

## Example curl Output

Here's an example of creating a new task using `curl`:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Study FastAPI"
}'
```

**Response:**
```json
{
  "title": "Study FastAPI",
  "id": 4,
  "done": false
}
```

## License

This project is licensed under the MIT License.
