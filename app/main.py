from fastapi import FastAPI, Cookie, HTTPException, Header
from .config import PUBLIC_KEY_PATH, REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_USER, REDIS_PASSWORD
from .models.redis_helper import RedisConnector
import jwt
from typing import Annotated

app = FastAPI()
r = RedisConnector(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, user=REDIS_USER)

def get_payload(token: str):
    with open(PUBLIC_KEY_PATH, "r") as f:
        public_key = f.read()
        return jwt.decode(token, public_key, algorithms=["RS256"])

def get_user_id(token: str):
    payload = get_payload(token)
    if payload is None:
        return None
    return payload.get("sub")

def get_admin(token: str):
    payload = get_payload(token)
    if payload is None:
        return None
    return payload.get("admin")

@app.get("/")
def list_servers(x_token: Annotated[str, Header()]):
    # redis contains zset with user_id as key and server_id as value 
    # return all server_id for the user
    # token in cookie
    user_id = get_user_id(x_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return r.get_instance(user_id)

@app.get("/{server_id}")
def get_server(server_id: str, x_token: Annotated[str, Header()]):
    # redis contains hash with server_id as key and server details as value
    # return server details
    # token in cookie
    id = get_user_id(x_token)
    if id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    # check if server_id is in zset with user_id as key
    if not r.is_instance(id, server_id):
        raise HTTPException(status_code=404, detail="Server not found")
    return {"status": "ok"}
