print("1. Starting Python script...")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import redis
import json
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
import time # Imported to handle timestamps

app = FastAPI()

# --- CORS: ALLOW FRONTEND CONNECTION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB SETUP ---
try:
    # Redis for caching live scores
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True, socket_timeout=1)
    redis_client.ping()
    print("✅ Redis Connected")
except:
    print("❌ Redis Failed (Ensure Docker is running)")

try:
    # MongoDB for storing match history
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
    db = mongo_client["live_score_db"]
    matches_collection = db["matches"]
    print("✅ Mongo Connected")
except:
    print("❌ Mongo Failed (Ensure Docker is running)")

# --- DATA MODELS ---

class MatchCreate(BaseModel):
    match_id: int
    home_team: str
    away_team: str
    is_live: bool = True

class MatchUpdate(BaseModel):
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    is_live: Optional[bool] = None

# --- ENDPOINTS ---

@app.post("/matches")
async def create_match(match: MatchCreate):
    try:
        # 1. Check if ID exists
        if await matches_collection.find_one({"match_id": match.match_id}):
            raise HTTPException(status_code=400, detail="ID exists")

        # 2. Prepare Data
        match_data = match.dict()
        match_data["home_score"] = 0
        match_data["away_score"] = 0
        
        # Automatic Timer: Save the current server time
        match_data["start_timestamp"] = time.time() 
        
        # 3. Save to MongoDB
        await matches_collection.insert_one(match_data)
        
        # 4. Save to Redis & Prepare Response (CRITICAL FIX HERE)
        # We copy the data and remove '_id' so it doesn't crash Postman
        redis_data = match_data.copy()
        if "_id" in redis_data: del redis_data["_id"]
        
        redis_client.set(f"match:{match.match_id}", json.dumps(redis_data))
        
        # Return the clean data (without _id)
        return redis_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}

@app.put("/matches/{match_id}")
async def update_match_score(match_id: int, update: MatchUpdate):
    # We ONLY update scores now, not time.
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    
    if not update_data:
        return {"message": "No data provided"}

    # Update MongoDB
    await matches_collection.update_one({"match_id": match_id}, {"$set": update_data})
    
    # Update Redis (Fetch clean data without _id)
    updated_match = await matches_collection.find_one({"match_id": match_id}, {"_id": 0})
    
    if updated_match:
        redis_client.set(f"match:{match_id}", json.dumps(updated_match))
        return updated_match
    else:
        raise HTTPException(status_code=404, detail="Match not found")

@app.get("/matches")
async def get_all_matches():
    # Fetch all matches from MongoDB (exclude the internal _id)
    matches = await matches_collection.find({}, {"_id": 0}).to_list(length=100)
    
    # Calculate the 'minute' dynamically based on start_timestamp
    current_time = time.time()
    for m in matches:
        if m.get("is_live") and m.get("start_timestamp"):
            elapsed_seconds = current_time - m["start_timestamp"]
            # Convert to minutes (integer) and format as string "35'"
            m["minute"] = f"{int(elapsed_seconds // 60)}'"
        else:
            # If no timestamp or not live, default to 0'
            if "minute" not in m: m["minute"] = "0'"
            
    return matches  # 5. DELETE A MATCH (New!)
@app.delete("/matches/{match_id}")
async def delete_match(match_id: int):
    # 1. Delete from MongoDB
    delete_result = await matches_collection.delete_one({"match_id": match_id})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Match not found")

    # 2. Delete from Redis (Clean up cache)
    redis_client.delete(f"match:{match_id}")
    
    return {"message": f"Match {match_id} deleted successfully"}
