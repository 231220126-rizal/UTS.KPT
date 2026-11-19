# database.py: Koneksi aiosqlite dan inisialisasi tabel
# Menggunakan aiosqlite untuk operasi basis data secara asinkron (non-blocking)

# pyrefly: ignore[missing-import]
import aiosqlite

DATABASE = "toko_buku.db"

# SQL untuk membuat tabel buku (resource utama)
# Kolom stok bertipe INTEGER sebagai kolom kuantitas wajib
CREATE_BOOKS_TABLE = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    judul TEXT NOT NULL,
    penulis TEXT NOT NULL,
    penerbit TEXT NOT NULL,
    harga REAL NOT NULL,
    stok INTEGER NOT NULL CHECK(stok >= 0)
);
"""

# SQL untuk membuat tabel transaksi (resource transaksi)
CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    jumlah INTEGER NOT NULL,
    total_harga REAL NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id)
);
"""


async def get_db():
    """Membuat koneksi ke database SQLite secara asinkron."""
    db = await aiosqlite.connect(DATABASE)
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    """Inisialisasi tabel database saat aplikasi pertama kali dijalankan."""
    db = await aiosqlite.connect(DATABASE)
    await db.execute(CREATE_BOOKS_TABLE)
    await db.execute(CREATE_TRANSACTIONS_TABLE)
    await db.commit()
    await db.close()
