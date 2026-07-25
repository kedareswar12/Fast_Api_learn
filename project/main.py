from fastapi import FastAPI

app = FastAPI() # creating the instance 

# the app instance is the main  componet of our FastAPI -> used to configure the application 


# /ping is the corresponding path of the endpoint 
@app.get("/ping")
async def root():
  return {"message" : "Hello World"}







