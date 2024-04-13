import os
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import requests

load_dotenv()


class TokenVerificationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, authorization: Request, call_next):
        
        if authorization is None or not authorization.startswith("Bearer "):
            return JSONResponse(status_code=401, content="Unauthorized!")
    
        token = authorization.split(" ")[1]
        response = requests.get(os.getenv("KEYCLOAK_URL"), headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            return JSONResponse(status_code=401, content="Unauthorized!")