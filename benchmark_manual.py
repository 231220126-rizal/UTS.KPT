# pyrefly: ignore[missing-import]
import asyncio, httpx, time

async def benchmark():
    base = "http://127.0.0.1:8000"
    results = {}

    # === READ benchmark: 100 requests ===
    async with httpx.AsyncClient(timeout=30) as client:
        start = time.perf_counter()
        tasks = [client.get(f"{base}/books?skip=0&limit=10") for _ in range(100)]
        resps = await asyncio.gather(*tasks)
        elapsed = time.perf_counter() - start
        ok = sum(1 for r in resps if r.status_code == 200)
        results["read"] = {
            "total": elapsed,
            "ok": ok,
            "throughput": ok / elapsed,
            "avg_lat": (elapsed / ok) * 1000
        }

    # === WRITE benchmark: 50 requests ===
    async with httpx.AsyncClient(timeout=60) as client:
        start = time.perf_counter()
        tasks = [client.post(f"{base}/transactions", json={"book_id": 3, "jumlah": 1}) for _ in range(50)]
        resps = await asyncio.gather(*tasks)
        elapsed = time.perf_counter() - start
        ok = sum(1 for r in resps if r.status_code in [200, 201])
        results["write"] = {
            "total": elapsed,
            "ok": ok,
            "throughput": ok / elapsed if ok else 0,
            "avg_lat": (elapsed / ok) * 1000 if ok else 0
        }

    r = results["read"]
    w = results["write"]
    print(f"READ  total={r['total']:.2f}s throughput={r['throughput']:.1f}req/s avg_lat={r['avg_lat']:.1f}ms ok={r['ok']}")
    print(f"WRITE total={w['total']:.2f}s throughput={w['throughput']:.1f}req/s avg_lat={w['avg_lat']:.1f}ms ok={w['ok']}")

asyncio.run(benchmark())
