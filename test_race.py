# test_race.py: Skrip pengujian race condition
# Mengirim 2 request POST /transactions secara serentak untuk stok tersisa 1
# Digunakan untuk menguji mekanisme asyncio.Lock (B3)

import asyncio
# pyrefly: ignore[missing-import]
import httpx

BASE_URL = "http://127.0.0.1:8000"


async def main():
    """
    Eksekusi 2 request serentak ke endpoint transaksi.

    Skenario:
    - Stok buku ID 1 diatur menjadi 1
    - Dua request pembelian masing-masing 1 unit dikirim bersamaan

    Hasil yang diharapkan:
    - TANPA Lock (USE_LOCK=False): kedua transaksi completed (overselling)
    - DENGAN Lock (USE_LOCK=True): satu completed, satu failed
    """
    async with httpx.AsyncClient(timeout=30) as client:
        # ===== PERSIAPAN: Reset stok buku ID 1 menjadi 1 =====
        print("=" * 60)
        print("🧪 PENGUJIAN RACE CONDITION - test_race.py")
        print("=" * 60)

        reset_resp = await client.put(
            f"{BASE_URL}/books/1",
            json={"stok": 1}
        )
        if reset_resp.status_code == 200:
            book_data = reset_resp.json()
            print(f"\n✅ Reset stok buku ID 1: stok = {book_data['stok']}")
            print(f"   Buku: {book_data['judul']} - Rp{book_data['harga']:,.0f}")
        else:
            print(f"\n❌ Gagal reset stok: {reset_resp.status_code} {reset_resp.text}")
            return

        # ===== KIRIM 2 REQUEST SERENTAK =====
        print(f"\n📤 Mengirim 2 request POST /transactions secara serentak...")
        payload = {"book_id": 1, "jumlah": 1}
        print(f"   Payload: {payload}")

        # Kirim dua request secara serentak dalam milidetik yang sama
        req1 = client.post(f"{BASE_URL}/transactions", json=payload)
        req2 = client.post(f"{BASE_URL}/transactions", json=payload)

        res1, res2 = await asyncio.gather(req1, req2)

        print(f"\n📥 Respon Request 1: [{res1.status_code}] {res1.json()}")
        print(f"📥 Respon Request 2: [{res2.status_code}] {res2.json()}")

        # ===== TUNGGU BACKGROUND TASKS SELESAI =====
        print("\n⏳ Menunggu 5 detik agar background tasks selesai...")
        await asyncio.sleep(5)

        # ===== CEK HASIL =====
        # Cek status kedua transaksi
        trx1_id = res1.json().get("id")
        trx2_id = res2.json().get("id")

        if trx1_id:
            trx1_resp = await client.get(f"{BASE_URL}/transactions/{trx1_id}")
            trx1 = trx1_resp.json()
            print(f"\n📋 Transaksi #{trx1_id}: status = {trx1['status']}")

        if trx2_id:
            trx2_resp = await client.get(f"{BASE_URL}/transactions/{trx2_id}")
            trx2 = trx2_resp.json()
            print(f"📋 Transaksi #{trx2_id}: status = {trx2['status']}")

        # Cek stok akhir
        book_resp = await client.get(f"{BASE_URL}/books/1")
        book_final = book_resp.json()
        print(f"\n📊 Stok akhir buku ID 1: {book_final['stok']}")

        # Analisis
        print("\n" + "=" * 60)
        if book_final["stok"] < 0:
            print("⚠️  RACE CONDITION TERDETEKSI!")
            print("   Stok menjadi negatif (overselling).")
            print("   Ini terjadi karena TIDAK menggunakan asyncio.Lock.")
        elif trx1 and trx2:
            completed = sum(1 for t in [trx1, trx2] if t["status"] == "completed")
            failed = sum(1 for t in [trx1, trx2] if t["status"] == "failed")
            if completed == 1 and failed == 1:
                print("✅ LOCK BERHASIL MENCEGAH RACE CONDITION!")
                print(f"   {completed} transaksi completed, {failed} transaksi failed.")
                print("   asyncio.Lock memastikan hanya satu yang berhasil.")
            elif completed == 2:
                print("⚠️  RACE CONDITION TERDETEKSI!")
                print("   Kedua transaksi berhasil completed (overselling).")
            else:
                print(f"   Hasil: {completed} completed, {failed} failed")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
