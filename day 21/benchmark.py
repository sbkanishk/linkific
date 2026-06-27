import asyncio
import time
import httpx

SYNC_URL = "http://127.0.0.1:8000/sync-slow"
ASYNC_URL = "http://127.0.0.1:8000/async-fast"
CONCURRENT_REQUESTS = 10

async def test_endpoint(client, url, request_id):
    start = time.time()
    try:
        response = await client.get(url, timeout=30.0)
        duration = time.time() - start
        print(f"  📥 Req #{request_id} finished in {duration:.2f}s (Status: {response.status_code})")
        return duration
    except Exception as e:
        print(f"  ❌ Req #{request_id} failed: {e}")
        return 0

async def run_benchmark():
    async with httpx.AsyncClient() as client:
        print(f"🏁 Starting Benchmark: Sending {CONCURRENT_REQUESTS} requests concurrently...")
        
        # --- TEST 1: SYNCHRONOUS ENDPOINT ---
        print("\n🐌 Testing Synchronous /sync-slow endpoint...")
        sync_start = time.time()
        # Even using gather, the sync endpoint blocks the single-threaded server!
        sync_tasks = [test_endpoint(client, SYNC_URL, i) for i in range(1, CONCURRENT_REQUESTS + 1)]
        await asyncio.gather(*sync_tasks)
        sync_total = time.time() - sync_start
        
        # --- TEST 2: ASYNCHRONOUS ENDPOINT ---
        print("\n🚀 Testing Asynchronous /async-fast endpoint...")
        async_start = time.time()
        # The async endpoint allows the event loop to instantly loop through them all!
        async_tasks = [test_endpoint(client, ASYNC_URL, i) for i in range(1, CONCURRENT_REQUESTS + 1)]
        await asyncio.gather(*async_tasks)
        async_total = time.time() - async_start
        
        # --- FINAL COMPARISON REPORT ---
        print("\n" + "="*45)
        print("📊 FINAL PERFORMANCE COMPARISON REPORT")
        print("="*45)
        print(f"🐌 Total Time (Sync Endpoint) : {sync_total:.2f} seconds")
        print(f"🚀 Total Time (Async Endpoint): {async_total:.2f} seconds")
        
        speedup = sync_total / async_total if async_total > 0 else 0
        print(f"\n⚡ Async was {speedup:.1f}x FASTER than Sync under concurrent load!")
        print("="*45)

if __name__ == "__main__":
    asyncio.run(run_benchmark())