from fastapi import FastAPI, Cookie, Header
from .redis_helper import get_redis_connection
from .config import PUBLIC_KEY_PATH
import jwt
from typing import Annotated

app = FastAPI()

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
    redis = get_redis_connection()
    if redis is None:
        return {"error": "Cannot connect to Redis"}
    # redis contains zset with user_id as key and server_id as value 
    # return all server_id for the user
    # token in cookie
    id = get_user_id(x_token)
    if id is None:
        return {"error": "Invalid token"}
    return redis.smembers(id)

@app.get("/{server_id}")
def get_server(server_id: str, x_token: Annotated[str, Header()]):
    redis = get_redis_connection()
    if redis is None:
        return {"error": "Cannot connect to Redis"}
    # redis contains hash with server_id as key and server details as value
    # return server details
    # token in cookie
    id = get_user_id(x_token)
    if id is None:
        return {"error": "Invalid token"}
    # check if server_id is in zset with user_id as key
    if not redis.sismember(id, server_id):
        return {"error": "Server not found"}
    return redis.hgetall(server_id)
