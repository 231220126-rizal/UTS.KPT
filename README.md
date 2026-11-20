# Video Presentasi UTS: https://youtu.be/pnFZeQ9X_5A

# 📚 Toko Buku API – UTS Komputasi Paralel dan Terdistribusi

REST API untuk manajemen toko buku yang dibangun menggunakan **FastAPI**, **aiosqlite**, **BackgroundTasks**, dan **asyncio.Lock**. Aplikasi ini mendemonstrasikan konsep concurrency, async processing, dan pencegahan race condition.

## 🏗️ Arsitektur

```
Client Request
       │
       ▼
   FastAPI App (main.py)
       │
       ├── routes/resource.py    → CRUD Buku (async via aiosqlite)
       └── routes/transaction.py → Transaksi + BackgroundTasks + asyncio.Lock
                │
                ▼
           SQLite Database (aiosqlite - non-blocking)
```

## ⚙️ Panduan Instalasi

### 1. Clone Repository

```bash
git clone <URL_REPO>
cd uts
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Inisialisasi Data Awal

```bash
python seed.py
```

### 5. Jalankan Server

```bash
# Dengan 1 worker
uvicorn main:app --workers 1 --port 8000

# Dengan 4 worker
uvicorn main:app --workers 4 --port 8000
```

### 6. Akses Swagger UI

Buka browser di: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📋 Daftar Endpoint

| Method | Path                | Keterangan                                                   |
|--------|---------------------|--------------------------------------------------------------|
| GET    | `/`                 | Root endpoint, info API                                      |
| GET    | `/books`            | Daftar semua buku (`?skip=0&limit=10`)                      |
| GET    | `/books/{id}`       | Detail satu buku berdasarkan ID                              |
| POST   | `/books`            | Tambah buku baru (validasi Pydantic)                         |
| PUT    | `/books/{id}`       | Perbarui data buku                                           |
| DELETE | `/books/{id}`       | Hapus permanen buku (hard delete)                            |
| POST   | `/transactions`     | Buat transaksi (response instan, proses di background)       |
| GET    | `/transactions`     | Daftar transaksi (`?status=pending`)                         |
| GET    | `/transactions/{id}`| Detail transaksi beserta status terkini                      |

## 🧪 Pengujian Race Condition

```bash
# Terminal 1: Jalankan server
uvicorn main:app --port 8000

# Terminal 2: Jalankan skrip pengujian
python test_race.py
```

## 📊 Benchmark (Locust)

```bash
# Terminal 1: Jalankan server
uvicorn main:app --workers 1 --port 8000

# Terminal 2: Jalankan Locust
locust -f locustfile.py --headless -u 20 -r 10 --run-time 30s
```

## 📁 Struktur Proyek

```
project/
├── main.py              # Inisialisasi FastAPI dan registrasi router
├── database.py          # Koneksi aiosqlite dan inisialisasi tabel
├── models.py            # Skema Pydantic (request dan response)
├── routes/
│   ├── __init__.py
│   ├── resource.py      # Endpoint CRUD resource utama (Buku)
│   └── transaction.py   # Endpoint transaksi asinkron
├── seed.py              # Skrip inisialisasi minimal 10 data awal
├── test_race.py         # Skrip pengujian race condition
├── locustfile.py        # Skenario pengujian beban Locust
├── requirements.txt     # Daftar pustaka dependensi Python
└── docs/
    └── laporan_uts.pdf  # Laporan hasil pengujian dan analisis
```

## 📚 Referensi

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [aiosqlite](https://aiosqlite.omnilib.dev)
- [Uvicorn](https://www.uvicorn.org)
- [Locust](https://locust.io)
