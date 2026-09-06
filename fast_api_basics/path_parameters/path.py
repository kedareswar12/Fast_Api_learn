from fastApi import FastAPi

app = FastAPi()

@app("/shipment")
def get_shipment():
    return {
        "content" : "wodden box",
        "status" : "In transit"
    }