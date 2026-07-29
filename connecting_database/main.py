from fastapi import FastAPI , Depends,  HTTPException
from pydantic import BaseModel
from typing import Optional , List
from sqlalchemy.orm import session
from model1 import TodoModel
from database import engine, SessionLocal


# ---------------------------------------------------------------------------
# CRUD APPLICATION USING FASTAPI
# CRUD = Create, Read, Update, Delete -> the 4 basic operations any backend
# needs to manage data. Here we're doing it with NO database - just an
# in-memory Python list ("todos"). This means all data is LOST when the
# server restarts. A real app would use a database (SQLite/Postgres/etc.)
# instead of a plain list.
# ---------------------------------------------------------------------------

app = FastAPI()
TodoModel.metadata.create_all(bind = engine)  # to create all the tables in the database 

# our "fake database" - just a plain Python list that lives in memory
# each item inside it will be a dictionary, e.g. {"id": 1, "title": "...", ...}
# todos = []


# ---------------------------------------------------------------------------
# THE Todo MODEL (Pydantic BaseModel)
# ---------------------------------------------------------------------------
# This defines the SHAPE of a Todo item - what fields it must have, and
# what type each field must be. FastAPI uses this to:
#   1. Automatically validate incoming JSON (reject bad data with a 422 error)
#   2. Auto-generate the interactive docs (/docs) with the correct fields
#   3. Convert incoming JSON into a proper Python object with .id, .title etc.
#
# Optional[str] = None  ->  this field is NOT required. If the client
#                            doesn't send it, it defaults to None.
# bool = False           ->  not required either, defaults to False.
class TodoBase(BaseModel):

  title: str
  description: Optional[str] = None
  completed: bool = False


class TodoCreate(TodoBase):
  pass 
class TodoUpdate(TodoBase):
  pass

class TodoResponse(TodoBase):
  id : int 
  class Config:
    orm_mode = True 
    
def get_db():
  db = SessionLocal()
  try:
    yield db 
  finally:
    db.close()
    

# ---------------------------------------------------------------------------
# READ (all) -> GET /todos
# ---------------------------------------------------------------------------
# GET requests are for RETRIEVING data - they should never change anything.
# This just returns the entire "todos" list as-is. FastAPI automatically
# converts the Python list of dicts into a JSON array in the response.
@app.get("/todos" , response_model=List[TodoResponse])
def get_todos(db : session = Depends(get_db)):
  todos = db.query(TodoModel).all()
  return todos  


# ---------------------------------------------------------------------------
# READ (one) -> GET /todos/{todo_id}
# ---------------------------------------------------------------------------
# {todo_id} in the path is a PATH PARAMETER - its value comes directly from
# the URL. E.g. hitting /todos/3 makes todo_id = 3 automatically.
# "todo_id: int" tells FastAPI to convert it to an int and validate it
# (a non-numeric value here would auto-return a 422 error).
#
# LOGIC: loop through every todo in the list, compare its 'id' key against
# todo_id. If found, return it immediately.
#
# IMPORTANT BUG PATTERN TO REMEMBER:
# The "not found" return must be OUTSIDE the for loop (same indentation
# level as "for", NOT inside the "if"). If you put it inside the loop,
# the function gives up and returns "not found" after checking just the
# FIRST item, instead of checking the whole list. This was a real bug we
# hit and fixed - always double check your indentation here.
@app.get("/todos/{todo_id}",response_model=List[TodoResponse])
def get_todo(todo_id: int , db : session = Depends(get_db)):
  # for todo in todos:
  #   if todo['id'] == todo_id:
  #     return todo
  # # this only runs if the loop finishes WITHOUT finding a match
  # return {"error": "Todo not found"}
  todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
  if not todo:
      raise HTTPException(status_code=404, detail="Todo not found")
  return todo


# ---------------------------------------------------------------------------
# CREATE -> POST /todos
# ---------------------------------------------------------------------------
# POST is the correct HTTP method for CREATING new data (never GET - GET
# is only for reading/fetching, not for causing changes).
#
# "todo: Todo" means: expect a JSON object in the REQUEST BODY that matches
# the Todo model's shape. FastAPI parses + validates it automatically and
# gives us a proper Todo object (with .id, .title, .description, .completed).
#
# .dict() (older Pydantic v1 style) / .model_dump() (Pydantic v2 style)
# converts that Todo OBJECT back into a plain Python dictionary, so we can
# store it in our "todos" list consistently (all items in the list are
# plain dicts, so we access them later with square-bracket syntax like
# todo['id'], not dot notation like todo.id).
#
# ROUTE COLLISION WARNING: this path ("/todos") is the SAME as get_todos()
# above - but that's fine here ONLY because the HTTP METHOD is different
# (GET vs POST). FastAPI treats "GET /todos" and "POST /todos" as two
# completely separate routes. What you must NEVER do is define the same
# path AND same method twice - that's what caused our earlier bug where
# the second function became unreachable dead code.



# @app.post("/todos")
# def create_todo(todo: TodoBase):
#   todos.append(todo.dict())
#   return todos[-1]   # return the item we just added (last item in the list)


@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: session = Depends(get_db)):
    new_todo = TodoModel(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# ---------------------------------------------------------------------------
# DELETE -> DELETE /todos/{todo_id}
# ---------------------------------------------------------------------------
# DELETE is the correct HTTP method for removing data.
# Same path parameter pattern as get_todo() above.
#
# LOGIC: loop through the list, find the todo whose 'id' matches todo_id,
# then use Python's built-in list.remove(item) to delete it BY VALUE
# (it finds the matching item internally - we don't need to track its
# position/index for this one).
#
# Note this function's structure is the CORRECT version of the pattern -
# the "not found" return is properly OUTSIDE the loop, only reached if
# nothing matched after checking every item. Use this as your reference
# for how get_todo() should also be structured.


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: session = Depends(get_db)):
  # for todo in todos:
  #   if todo['id'] == todo_id:
  #     todos.remove(todo)
  #     return {"Message": "todo deleted successfully"}
  # return {"error": "Todo not found"}
  todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
  if not todo:
    raise HTTPException(status_code=404, detail="Todo not found")
  db.delete(todo)
  db.commit()
  return {"message": "todo deleted successfully"}


# ---------------------------------------------------------------------------
# UPDATE -> PUT /todos/{todo_id}
# ---------------------------------------------------------------------------
# PUT is the correct HTTP method for a FULL REPLACE of an existing item.
# (PATCH would be used instead for a PARTIAL update - changing only some
# fields while leaving the rest untouched. PUT expects the CLIENT to send
# the complete object every time.)
#
# Two inputs here:
#   - todo_id: int          -> path parameter, tells us WHICH todo to update
#   - updated_todo: Todo    -> request body, the NEW data to replace it with
#
# WHY enumerate() IS NEEDED HERE (and wasn't needed in delete_todo):
#   delete_todo uses todos.remove(todo) - Python finds and removes an item
#   BY VALUE, no position needed.
#   There is NO equivalent "replace by value" method for lists. To OVERWRITE
#   an item, you must know its exact INDEX (position) in the list, and do
#   todos[index] = new_value. That's exactly what enumerate() gives us:
#   both the index AND the value on each loop iteration, instead of just
#   the value alone (which a normal "for todo in todos" loop gives).
#
# COMMON MISTAKE TO AVOID: writing update_todos.model_dump() instead of
# updated_todo.model_dump(). update_todos is the FUNCTION's own name -
# functions don't have a .model_dump() method, only Pydantic model
# INSTANCES do (like the updated_todo parameter). Mixing up a function
# name with a parameter name like this causes an AttributeError, which
# shows up to the client as a generic "Internal Server Error" (500).
# Always check your terminal's traceback to see the real Python error
# when you hit a 500 - the error message itself tells you exactly which
# line and which mistake caused it.
@app.put("/todos/{todo_id}")
# def update_todos(todo_id: int, updated_todo: Todo):
#   for index, todo in enumerate(todos):
#     if todo['id'] == todo_id:
#       todos[index] = updated_todo.model_dump()
#       return todos[index]
#   return {"error": "Todo not found"}
def update_todo(todo_id: int, updated_todo: TodoUpdate, db: session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    for key, value in updated_todo.dict().items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo

# ---------------------------------------------------------------------------
# QUICK REFERENCE - HTTP METHODS USED IN THIS FILE
# ---------------------------------------------------------------------------
# GET     -> read/fetch data                  (get_todos, get_todo)
# POST    -> create new data                  (create_todo)
# PUT     -> full replace of existing data     (update_todos)
# DELETE  -> remove existing data              (delete_todo)
#
# (Not used here, but good to know: PATCH -> partial update of existing data)
#
# ---------------------------------------------------------------------------
# QUICK REFERENCE - WHERE DOES EACH PIECE OF DATA COME FROM?
# ---------------------------------------------------------------------------
# PATH PARAMETER   -> part of the URL itself, e.g. /todos/3  ->  todo_id = 3
# QUERY PARAMETER  -> after "?" in the URL, e.g. ?q=kedar  (key=value, "=" not ":")
# REQUEST BODY     -> JSON sent in the body of POST/PUT/PATCH requests,
#                     used for a Pydantic model parameter like "todo: Todo"
#                     (cannot be tested by just pasting a URL in the browser -
#                     browsers only send GET. Use /docs (Swagger UI) instead,
#                     or a tool like curl/Postman/requests library.)
#
# ---------------------------------------------------------------------------
# QUICK REFERENCE - JSON vs URL SYNTAX (easy to mix up!)
# ---------------------------------------------------------------------------
# JSON body        uses  :   e.g. {"id": 1, "title": "Todo1"}
# URL query string  uses  =   e.g. ?q=kedar&id=1
# Never swap these two - {"id" = 1} is invalid JSON, and ?q:kedar is not a
# valid query param.