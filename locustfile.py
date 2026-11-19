# locustfile.py: Skenario pengujian beban menggunakan Locust
# Membandingkan performa 1 worker vs 4 worker Uvicorn

# pyrefly: ignore[missing-import]
from locust import HttpUser, task, between, tag


class TokoBukuUser(HttpUser):
    """
    Simulasi pengguna Toko Buku API untuk pengujian beban.
    Dua skenario diuji:
    - Skenario Read: GET /books (100 request, konkurensi 20)
    - Skenario Write: POST /transactions (50 request, konkurensi 10)
    """
    wait_time = between(0.1, 0.5)
    host = "http://127.0.0.1:8000"

    @tag("read")
    @task(3)
    def get_books(self):
        """Skenario Read: mengambil daftar buku."""
        self.client.get("/books?skip=0&limit=10")

    @tag("write")
    @task(1)
    def create_transaction(self):
        """Skenario Write: membuat transaksi pembelian buku."""
        self.client.post(
            "/transactions",
            json={"book_id": 1, "jumlah": 1},
        )
