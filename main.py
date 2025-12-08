print("1. Starting Python script...")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from fastapi.middleware.cors import CORSMiddleware
print("2. Libraries imported.")

app = FastAPI()


# --- NEW: ALLOW FRONTEND CONNECTION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- CONFIGURATION ---
print("3. Connecting to Redis...")
try:
    # Set a short timeout (1 second) so it doesn't hang forever
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True, socket_timeout=1)
    redis_client.ping() # Force a check now
    print("âœ… Redis Connected Successfully!")
except Exception as e:
    print(f"âŒ Redis Connection Failed: {e}")

print("4. Connecting to MongoDB...")
try:
    MONGO_URL = "mongodb://localhost:27017"
    # Set timeout to 2 seconds
    mongo_client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    print("âœ… MongoDB Client Created")
except Exception as e:
    print(f"âŒ MongoDB Setup Failed: {e}")

db = mongo_client["live_score_db"]
matches_collection = db["matches"]

class MatchCreate(BaseModel):
    match_id: int
    home_team: str
    away_team: str

@app.get("/")
def home():
    print("ðŸ”” Request received: Home Page")
    return {"message": "Live Score API is running!"}

@app.post("/matches")
async def create_match(match: MatchCreate):
    print(f"ðŸ“ Request received: Create Match {match.match_id}")
    try:
        match_data = match.dict()
        match_data["score"] = "0-0"
        match_data["minute"] = 0
        await matches_collection.insert_one(match_data)
        
        redis_data = match_data.copy()
        if "_id" in redis_data: del redis_data["_id"]
        redis_client.set(f"match:{match.match_id}", json.dumps(redis_data))
        
        print("âœ… Match Created Successfully")
        return {"status": "created"}
    except Exception as e:
        print(f"âŒ Error creating match: {e}")
        return {"error": str(e)}

@app.get("/matches/{match_id}/score")
async def get_score(match_id: int):
    print(f"ðŸ” Request received: Get Score for {match_id}")
    try:
        cached = redis_client.get(f"match:{match_id}")
        if cached:
            print("âœ… Found in Redis")
            return json.loads(cached)
        
        print("âš ï¸ Not in Redis, checking Mongo...")
        match = await matches_collection.find_one({"match_id": match_id})
        if match:
            match.pop("_id")
            return match
        raise HTTPException(status_code=404, detail="Not found")
    except Exception as e:
        print(f"âŒ Error getting score: {e}")
        return {"error": str(e)}
# NEW: Get All Matches (for the dashboard)
@app.get("/matches")
async def get_all_matches():
    # Fetch all matches from MongoDB (exclude the internal _id)
    matches = await matches_collection.find({}, {"_id": 0}).to_list(length=100)
    return matches
