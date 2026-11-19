# main.py: Inisialisasi FastAPI dan registrasi router
# Entry point utama aplikasi Toko Buku API

# pyrefly: ignore[missing-import]
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routes import resource, transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle event: inisialisasi database saat aplikasi pertama kali dijalankan.
    Menggunakan asynccontextmanager sebagai pengganti on_event("startup").
    """
    await init_db()
    yield


app = FastAPI(
    title="Toko Buku API",
    description="REST API untuk manajemen toko buku dengan fitur concurrency dan async processing. "
                "Dibangun menggunakan FastAPI, aiosqlite, BackgroundTasks, dan asyncio.Lock.",
    version="1.0.0",
    lifespan=lifespan,
)

# Registrasi router endpoint
app.include_router(resource.router)
app.include_router(transaction.router)


@app.get("/", tags=["Root"])
async def root():
    """Endpoint root untuk memastikan API berjalan."""
    return {
        "message": "Selamat datang di Toko Buku API",
        "docs": "/docs",
        "endpoints": {
            "books": "/books",
            "transactions": "/transactions",
        },
    }
