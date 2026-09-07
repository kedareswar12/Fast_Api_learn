from fastapi import FastAPI

app = FastAPI()

@app.get("/shipment")
def get_shipment():
    return {
        "Order Name" : "Wodden Box",
        "Shipment Status" : "In_transit"
    }

"""

# -Tips to remember

if you need to run any fastapi application go to the documentation 
you will see the fastapi standard file so that you will get the doc to download the fast api file


else you can use the uvcorn to run this fast api application

# uv add uvicorn
# uv run uvicorn fast_api_basics.API_endpoints.api_endpoint_main:app --reload

this will re run your project file 


else use uvicorn <foldername>.<filename>:app --reload


"""
