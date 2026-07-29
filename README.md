# FastAPI Todo App

A simple CRUD (Create, Read, Update, Delete) Todo application built with **FastAPI**, **SQLAlchemy**, and **MySQL**, served with **Uvicorn**.

This project is part of a learning module on FastAPI — covering how to build REST APIs in Python, connect them to a relational database, and validate data using Pydantic.

---

## 🚧 Status

This module is a work in progress. Stay tuned for updates as more features and notes are added.

---

## 📚 What You'll Learn

- Setting up a FastAPI project and running it with Uvicorn
- Defining Pydantic models for request/response validation
- Connecting FastAPI to a MySQL database using SQLAlchemy
- Writing full CRUD endpoints (GET, POST, PUT, DELETE)
- Using dependency injection (`Depends`) for database sessions
- Common pitfalls: schema mismatches, model vs. table drift, HTTP status codes

---

## 🛠️ Tech Stack

| Layer          | Tool                     |
|----------------|--------------------------|
| Web framework  | FastAPI                  |
| ASGI server    | Uvicorn                  |
| ORM            | SQLAlchemy               |
| Database       | MySQL                    |
| Validation     | Pydantic                 |
| Language       | Python 3.8               |

---

## 📁 Project Structure
connecting_database/
├── main.py # FastAPI app + all CRUD routes
├── model1.py # SQLAlchemy TodoModel (table definition)
├── database.py # DB engine, session, and Base setup
└── README.md


---

## ⚙️ Setup

1. Create and activate a virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
```

2. Install dependencies:
```bash
   pip install fastapi uvicorn sqlalchemy mysql-connector-python
```

3. Configure your MySQL connection in `database.py`.

4. Run the server:
```bash
   uvicorn main:app --reload
```

5. Open the interactive API docs:

http://127.0.0.1:8000/docs

---

## 🔗 API Endpoints

| Method | Endpoint         | Description         |
|--------|------------------|----------------------|
| GET    | `/todos`         | Get all todos        |
| GET    | `/todos/{id}`    | Get a single todo    |
| POST   | `/todos`         | Create a new todo    |
| PUT    | `/todos/{id}`    | Update a todo        |
| DELETE | `/todos/{id}`    | Delete a todo        |

---

## 📝 Notes / Lessons Learned

- `TodoModel.metadata.create_all(bind=engine)` only creates tables that **don't already exist** — it won't alter an existing table if the model changes. Use Alembic for real migrations.
- Keep column names in the SQLAlchemy model and the actual database table in sync — a mismatch (like a typo in a column name) causes a `ProgrammingError` at query time, not at startup.
- Use `raise HTTPException(status_code=404, ...)` for "not found" cases instead of returning a `200` with an error message in the body.

---

## 🔜 Coming Up

- [ ] Add Alembic migrations
- [ ] Add authentication
- [ ] Add pagination/filtering to `GET /todos`
- [ ] Write unit tests
