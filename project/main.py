from fastapi import FastAPI
from pydantic import BaseModel
# creating the FastAPI instance
# this "app" object is the MAIN component of our FastAPI application
# every route (endpoint) we define below gets registered onto this "app" object
app = FastAPI()


class Custom(BaseModel):
  name:str
  age:int

# ---------------------------------------------------------------------------
# BASIC ROUTE
# ---------------------------------------------------------------------------

# "/ping" is the path of this endpoint
# @app.get(...) tells FastAPI: "when someone sends a GET request to this path,
# run the function below"
@app.get("/ping")
async def root():
  return {"message": "Hello World"}


# ---------------------------------------------------------------------------
# WHY ROUTE ORDER MATTERS IN FASTAPI (this was the bug we spent all day on!)
# ---------------------------------------------------------------------------
#
# FastAPI (via Starlette underneath) checks routes IN THE ORDER they are
# defined in the file, TOP to BOTTOM. The moment it finds a route that
# matches the incoming URL, it uses that one and STOPS looking further down.
#
# This means:
#   1. You must NEVER define the same path twice (e.g. "/blog/{blog_id}"
#      defined twice). If you do, only the FIRST one will ever run - the
#      second becomes dead code that silently never executes. No error is
#      thrown, which makes this bug very easy to miss.
#
#   2. If you have a STATIC path like "/blog/comments" and a DYNAMIC path
#      like "/blog/{blog_id}", the STATIC one must be defined FIRST.
#      Why? Because "/blog/{blog_id}" will match ANY value in that position
#      - including the literal word "comments". So if the dynamic route is
#      defined first, a request to "/blog/comments" would incorrectly get
#      captured by "/blog/{blog_id}" (with blog_id="comments", which would
#      then fail since blog_id is typed as int).
#
# Example of CORRECT ordering (commented out below, kept for reference):
#
# @app.get("/blog/comments")          <-- static path FIRST
# async def read_comments():
#   return {"comments": "No comments yet"}
#
# @app.get("/blog/{blog_id}")         <-- dynamic path SECOND
# async def read_blog(blog_id: int):
#   return {"blog_id": blog_id}
#
# If you're ever unsure where to place a route, keep the static block ABOVE
# the dynamic block, and test in the browser to confirm.


# ---------------------------------------------------------------------------
# PATH PARAMETERS vs QUERY PARAMETERS
# ---------------------------------------------------------------------------
#
# PATH PARAMETER:
#   Example URL: /blog/2
#   Here, "2" is part of the URL PATH itself. In the function signature,
#   "blog_id: int" tells FastAPI to:
#     - extract that value from the URL
#     - convert it to an int automatically
#     - validate it (if someone passes "/blog/abc", FastAPI auto-returns
#       a 422 error, since "abc" isn't a valid int)
#
# QUERY PARAMETER:
#   Example URL: /blog/2?q=kedar
#   Everything after the "?" is the query string. Each key=value pair here
#   is a query parameter (multiple ones are joined with "&", e.g.
#   /blog/2?q=kedar&age=21).
#
#   To accept a query parameter in FastAPI, you just add it as a normal
#   function argument that is NOT part of the path (i.e., not inside {}
#   in the @app.get(...) path string). FastAPI automatically knows it's
#   a query param because it doesn't match any {placeholder} in the path.
#
#   "q: str = None" means:
#     - q is expected to be a string
#     - it's OPTIONAL, defaulting to None if not provided in the URL
#
# IMPORTANT SYNTAX NOTE: query params in the URL must use "=" not ":"
#   Correct:   /blog/2?q=kedar
#   Incorrect: /blog/2?q:kedar   <-- this will NOT be parsed as q="kedar"

@app.post("/blog/{blog_id}")
async def read_blog(blog_id: int, request_body : Custom, q: str = None):
  # print() here is just for us to see the query param value in the
  # terminal/server logs while debugging. It has nothing to do with what
  # gets sent back to the browser - that's controlled by the return statement.
  print(request_body.name)
  print(q, flush=True)

  # whatever we return here gets automatically converted to JSON by FastAPI
  # and sent back as the HTTP response body
  return {"blog_id": blog_id, "q": q}


# Request body -> 3rd type