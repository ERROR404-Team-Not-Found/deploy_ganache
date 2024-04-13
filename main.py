import os
from fastapi import FastAPI, HTTPException, Request
from web3 import Web3
from eth_utils import to_checksum_address
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from dotenv import load_dotenv
import requests

#from middleware import TokenVerificationMiddleware

app = FastAPI()

load_dotenv()

#app.add_middleware(TokenVerificationMiddleware)

# CORS middleware to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Connect to the local Ethereum node
web3 = Web3(Web3.HTTPProvider(os.getenv("GANACHE_URL")))

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     authorization = request.headers.get("Authorization")
#     if authorization is None or not authorization.startswith("Bearer "):
#         return JSONResponse(status_code=401, content="Unauthorized!")

#     token = authorization.split(" ")[1]
#     response = requests.get(os.getenv("KEYCLOAK_URL"), headers={"Authorization": f"Bearer {token}"})
#     if response.status_code != 200:
#         return JSONResponse(status_code=401, content="Unauthorized!")
    
#     response = await call_next(request)
#     return response

@app.get('/transactions/{user_address}')
async def get_transactions(user_address: str):
    try:
        user_address = user_address.lower()
        latest_block_number = web3.eth.block_number
        transactions = []

        for i in range(latest_block_number + 1):
            block = web3.eth.get_block(i, full_transactions=True)
            for tx in block.transactions:
                tx_dict = {
                    key: value.hex() if isinstance(value, bytes) else value
                    for key, value in tx.items()
                }

                tx_dict['from'] = tx_dict['from'].lower()
                tx_dict['to'] = tx_dict['to'].lower()

                if tx_dict['from'] == user_address or tx_dict['to'] == user_address:
                    transactions.append(tx_dict)

        return transactions
    except Exception as e:
        print('Error:', e)
        raise HTTPException(status_code=500, detail='Internal Server Error')

@app.get('/balance/{user_address}')
async def get_balance(user_address: str):
    try:
        user_address = to_checksum_address(user_address)
        balance = web3.eth.get_balance(user_address)
        return {'balance': balance}
    except Exception as e:
        print('Error:', e)
        raise HTTPException(status_code=500, detail='Internal Server Error')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8093)
