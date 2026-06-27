from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
import asyncio
import time
import httpx
import aiofiles
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select

# 🗄️ Database Configuration
DATABASE_URL = "sqlite+aiosqlite:///./async_sandbox.db"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# 🛠️ Database Setup
class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    price: Mapped[float]

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        if not result.scalars().first():
            session.add_all([
                Product(name="Async Flying Shoes", price=99.99),
                Product(name="Event Loop Coffee Mug", price=14.99),
                Product(name="Non-Blocking Keyboard", price=120.00)
            ])
            await session.commit()
    yield
    await engine.dispose()

# 🚀 FastAPI App
app = FastAPI(title="Day 21: Async Speed Demon", lifespan=lifespan)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# --- 🐌 Sync vs 🚀 Async Endpoints ---
@app.get("/sync-slow")
def sync_slow():
    time.sleep(3)
    return {"status": "Completed synchronously", "time_taken": "3 seconds"}

@app.get("/async-fast")
async def async_fast():
    await asyncio.sleep(3)
    return {"status": "Completed asynchronously", "time_taken": "3 seconds"}

# --- 📡 Concurrent HTTP & File I/O Endpoints ---
@app.get("/fetch-pokemon/{pokemon_name}")
async def get_pokemon(pokemon_name: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()["forms"][0]
        return {"error": "Pokemon not found"}

@app.get("/batch-fetch")
async def batch_fetch():
    start_time = time.time()
    pokemon_list = ["ditto", "pikachu", "charizard"]
    async with httpx.AsyncClient() as client:
        tasks = [client.get(f"https://pokeapi.co/api/v2/pokemon/{p}") for p in pokemon_list]
        responses = await asyncio.gather(*tasks)
    
    async with aiofiles.open("api_logs.txt", mode="a") as log_file:
        await log_file.write(f"Batch fetch completed at {start_time}\n")
    
    end_time = time.time()
    return {"message": f"Fetched {len(responses)} pokemon!", "duration_seconds": round(end_time - start_time, 2)}

# --- 🗄️ Async Database Endpoint ---
@app.get("/products")
async def read_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()

# --- 🛡️ Async Error & Timeout Handling Endpoint ---
@app.get("/safely-fetch-faulty-api")
async def safely_fetch():
    """Demonstrates how to handle timeouts and errors without killing the event loop."""
    # Simulating an API endpoint that takes way too long to respond
    delayed_url = "https://httpbin.org/delay/5" 
    
    async with httpx.AsyncClient() as client:
        try:
            print("⏳ Attempting to fetch external API with a strict 2-second timeout...")
            # Wrap our coroutine with a hard timeout wall
            response = await asyncio.wait_for(client.get(delayed_url), timeout=2.0)
            return response.json()
            
        except asyncio.TimeoutError:
            print("⚠️ Catch! The external server was too slow, but our event loop survived!")
            return {"error": "The external API timed out, but the server is running smoothly."}
        except httpx.HTTPError as http_err:
            return {"error": f"A network error occurred: {http_err}"}

# --- 🔌 Live WebSocket Endpoint ---
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """Establishes a persistent bidirectional connection on the event loop."""
    await websocket.accept()
    print("🔌 WebSocket client successfully connected!")
    try:
        while True:
            # Wait asynchronously for messages sent by the client
            data = await websocket.receive_text()
            print(f"📥 Received from client: {data}")
            # Echo back to the client immediately
            await websocket.send_text(f"🚀 Async Server Echo: {data}")
    except WebSocketDisconnect:
        print("🔌 WebSocket client disconnected gracefully.")