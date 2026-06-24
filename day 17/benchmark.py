import urllib.request
import concurrent.futures
import time

URLS = {
    "Django": "http://127.0.0.1:8000/api/tasks/",
    "FastAPI": "http://127.0.0.1:8001/tasks/?user_id=1"
}

REQUEST_COUNT = 100  # Number of concurrent hits

def hit_endpoint(url):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return response.getcode()
    except Exception:
        return None

def run_test(name, url):
    print(f"⚡ Hammering {name} with {REQUEST_COUNT} threads...")
    start_time = time.time()
    
    # Fire requests concurrently using standard library thread pooling
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(hit_endpoint, [url] * REQUEST_COUNT))
        
    duration = time.time() - start_time
    success_count = len([r for r in results if r == 200])
    
    print(f"📊 {name} Performance Results:")
    print(f"   - Total Duration: {duration:.4f} seconds")
    print(f"   - Throughput Rate: {REQUEST_COUNT / duration:.2f} req/sec")
    print(f"   - Success Binds: {success_count}/{REQUEST_COUNT}\n")

if __name__ == "__main__":
    print("🚀 Initiating Zero-Dependency Live Benchmark... \n")
    
    # Test Django
    try:
        run_test("Django", URLS["Django"])
    except Exception as e:
        print(f"Django connection failed: {e}\n")
        
    # Test FastAPI
    try:
        run_test("FastAPI", URLS["FastAPI"])
    except Exception as e:
        print(f"FastAPI connection failed: {e}\n")