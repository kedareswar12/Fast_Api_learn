from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

# #region agent log
import json, time
from pathlib import Path as _Path
try:
    _log = _Path(__file__).resolve().parents[2] / "debug-d679f0.log"
    _log.open("a", encoding="utf-8").write(json.dumps({"sessionId":"d679f0","runId":"post-fix","hypothesisId":"A","location":"path.py:import","message":"fastapi import succeeded","data":{"import_name":"fastapi","class_name":"FastAPI"},"timestamp":int(time.time()*1000)}) + "\n")
except Exception as _e:
    pass
# #endregion

app = FastAPI()

@app.get("/shipment/{item_id}")
def get_shipment(item_id : int ) -> dict:
    # #region agent log
    try:
        _log = _Path(__file__).resolve().parents[2] / "debug-d679f0.log"
        _log.open("a", encoding="utf-8").write(json.dumps({"sessionId":"d679f0","runId":"post-fix","hypothesisId":"C","location":"path.py:get_shipment","message":"route handler hit","data":{"path":"/shipment"},"timestamp":int(time.time()*1000)}) + "\n")
    except Exception:
        pass
    # #endregion
    return {
        "id" :  item_id ,
        "content" : "wodden box",
        "status" : "In transit"
    }


#Scalar documentation 
@app.get("/scalar", include_in_schema=False)
def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
