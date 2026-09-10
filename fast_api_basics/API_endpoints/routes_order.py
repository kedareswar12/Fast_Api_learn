from typing import Any
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

@app.get("/shipment/latest")
def get_shipment() -> dict[str ,Any]:
    return {
        "id" : 321,
        "weight" : 21,
        "contetnt" : "wodden chair",
        "status" :"placed"
    }


@app.get("/shipment/{int_id}")
def get_shipment(int_id :int) -> dict[str ,Any]:
    return {
        "id" : int_id,
        "weight" : 1.2,
        "contetnt" : "wodden table",
        "status" :"Intransit"
    }

# @app.get("/shipment/latest")
# def get_shipment(int_id :int) -> dict[str ,Any]:
#     return {
#         "id" : 7848,
#         "weight" : 1.2,
#         "contetnt" : "wodden chair",
#         "status" :"Placed"
#     }


# Route position suppose if you have 
"""

this one -> /shipment/{id}
and next -> /shipment/lattest 
then write the latest one onto the top and then bring the other one to the bottom 
/shipment/lattest this one needs to be first 


"""
#Scalar documentation 
@app.get("/scalar", include_in_schema=False)
def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
 