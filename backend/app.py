import os
from fastapi import FastAPI, Request
from reclaim_python_sdk import ReclaimProofRequest, verify_proof, Proof
import uvicorn
from urllib.parse import unquote
import json
from fastapi.middleware.cors import CORSMiddleware
 
app = FastAPI()

# Need for frontend to access the backend ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# set -a && source .creds && set +a
BASE_URL = os.environ.get('BASE_URL', "http://localhost:3000")  # if using ngrok, provide the ngrok base url
APP_ID = os.environ.get('APP_ID', 'APP_ID')
APP_SECRET = os.environ.get('APP_SECRET', 'APP_SECRET')
PROVIDER_ID = os.environ.get('PROVIDER_ID', 'PROVIDER_ID')

# Route to generate SDK configuration
# http://localhost:3000/generate-config 
@app.get("/generate-config")
async def generate_config(): 
    try:
        reclaim_proof_request = await ReclaimProofRequest.init(APP_ID, APP_SECRET, PROVIDER_ID, {"provider_version": "latest"})
        reclaim_proof_request.set_app_callback_url(BASE_URL+"/receive-proofs")        
        reclaim_proof_request_config = reclaim_proof_request.to_json_string()
        return {"reclaimProofRequestConfig": reclaim_proof_request_config}
    except Exception as e:
        return {"error": str(e)}, 500
 
 # Route to receive proofs
 # curl -X POST http://localhost:3000/receive-proofs -d '{"proof": "proof_data"}'
@app.post("/receive-proofs")
async def receive_proofs(request: Request):
   # Get the raw body content
    body = await request.body()
    # Decode the bytes to string
    body_str = body.decode()
    # unquote the body string to remove the url encoding
    body_str = unquote(body_str)
    # parse the body string to a dictionary
    parsed_data = json.loads(body_str)
    # print('parsed_data', parsed_data)
    proof = Proof.from_json(parsed_data)
 
    result = await verify_proof(proof)
    if not result:
        return {"status": "failed", "message": "Proof verification failed"} , 400
 
    return {"status": "success"}
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)