from functools import wraps
import json
import threading
import time
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
import redis

app = FastAPI()

def get_redis():
    client = redis.Redis(host='redis', port=6379, decode_responses=True)
    try:
        yield client
    finally:
        pass

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def redis_listener():
    pubsub = r.pubsub()
    pubsub.subscribe("global_alerts")
    print("?? Radio station tuned to 'global_alerts'. Listening for live broadcasts...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"?? REAL-TIME ALERT RECEIVED INSIDE CONTAINER: {message['data']}")

threading.Thread(target=redis_listener, daemon=True).start()

def cache(ttl: int = 60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            arg_str = ",".join([f"{k}={v}" for k, v in kwargs.items()])
            cache_key = f"{func.__name__}:{arg_str}"
            cached_data = r.get(cache_key)
            if cached_data:
                print(f"? DECORATOR HIT! Serving {cache_key} from cache.")
                return json.loads(cached_data)
            print(f"?? DECORATOR MISS! Executing function for {cache_key}...")
            result = func(*args, **kwargs)
            r.set(cache_key, json.dumps(result), ex=ttl)
            return result
        return wrapper
    return decorator

class UserUpdate(BaseModel):
    name: str
    role: str

@app.get("/users/{user_id}")
@cache(ttl=30)
def get_user_profile(user_id: int):
    time.sleep(2)
    return {
        "user_id": user_id,
        "name": "Kanishk",
        "role": "Backend Engineer",
        "updated_at": time.time(),
    }

@app.put("/users/{user_id}")
def update_user_profile(user_id: int, updated_user: UserUpdate):
    cache_key = f"get_user_profile:user_id={user_id}"
    r.delete(cache_key)
    return {"message": "Profile updated and cache cleared!", "data": updated_user}

@app.get("/limited-api/{user_id}")
def secure_endpoint(user_id: int, redis_db: redis.Redis = Depends(get_redis)):
    rate_key = f"rate:{user_id}"
    current_requests = redis_db.incr(rate_key)
    if current_requests == 1:
        redis_db.expire(rate_key, 60)
    if current_requests > 5:
        return {
            "status": "error",
            "message": "Too many requests! Slow down, Master Hacker. ??",
            "retry_after_seconds": redis_db.ttl(rate_key)
        }
    return {"status": "success", "requests_this_minute": current_requests}

@app.post("/broadcast")
def broadcast_message(message: str, redis_db: redis.Redis = Depends(get_redis)):
    redis_db.publish("global_alerts", message)
    return {"status": "Broadcast successfully transmitted across the system!"}

@app.get("/checkout/{item_id}")
def process_payment(item_id: str, redis_db: redis.Redis = Depends(get_redis)):
    lock_key = f"lock:checkout:{item_id}"
    acquire_lock = redis_db.set(lock_key, "locked", nx=True, ex=10)
    if not acquire_lock:
        raise HTTPException(status_code=423, detail="?? System busy processing this item checkout.")
    try:
        time.sleep(4)
        return {"status": "success", "message": f"Item {item_id} purchased successfully!"}
    finally:
        redis_db.delete(lock_key)
