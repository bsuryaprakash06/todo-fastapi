# Todo FastAPI

A lightweight RESTful API for managing tasks, built with FastAPI and designed to demonstrate CRUD operations, request validation, and interactive API documentation.

## Features

- CRUD operations for task management
- Request validation using Pydantic
- Interactive OpenAPI (Swagger UI) documentation
- Search tasks by title
- Task statistics endpoint
- In-memory data storage
- Standard HTTP status codes and error responses

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn

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

## Running the Application

Start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Interactive API documentation is available at:

http://127.0.0.1:8000/docs

![Swagger Screenshot](swagger_screenshot.png)

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | API information |
| GET | /health | Health check |
| GET | /tasks | Retrieve all tasks |
| GET | /tasks/{id} | Retrieve a task |
| POST | /tasks | Create a task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |
| GET | /stats | Retrieve task statistics |

## Example Request

```bash
curl -i -X 'POST' \
  'http://127.0.0.1:8000/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Study FastAPI"
}'
```

**Response:**
```http
HTTP/1.1 201 Created
content-length: 49
content-type: application/json

{
  "title": "Study FastAPI",
  "id": 4,
  "done": false
}
```

## Project Structure

```text
todo-fastapi/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── data.py
│   └── helpers.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

## License

Licensed under the MIT License.
