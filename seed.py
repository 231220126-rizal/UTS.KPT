# seed.py: Skrip inisialisasi data awal (minimal 10 buku)
# Jalankan sekali untuk mengisi database dengan data sample

import asyncio
# pyrefly: ignore[missing-import]
import aiosqlite
from database import DATABASE, init_db

# Data awal 12 buku untuk pengujian
SEED_DATA = [
    ("Laskar Pelangi", "Andrea Hirata", "Bentang Pustaka", 89000, 25),
    ("Bumi Manusia", "Pramoedya Ananta Toer", "Hasta Mitra", 95000, 15),
    ("Filosofi Teras", "Henry Manampiring", "Kompas", 78000, 30),
    ("Atomic Habits", "James Clear", "Gramedia Pustaka", 109000, 20),
    ("Sapiens", "Yuval Noah Harari", "Kepustakaan Populer Gramedia", 125000, 10),
    ("Pulang", "Tere Liye", "Republika", 85000, 18),
    ("Laut Bercerita", "Leila S. Chudori", "Kepustakaan Populer Gramedia", 92000, 12),
    ("Cantik Itu Luka", "Eka Kurniawan", "Gramedia Pustaka", 98000, 8),
    ("Hujan", "Tere Liye", "Gramedia Pustaka", 79000, 22),
    ("Negeri 5 Menara", "Ahmad Fuadi", "Gramedia Pustaka", 88000, 14),
    ("Perahu Kertas", "Dee Lestari", "Bentang Pustaka", 82000, 16),
    ("Dilan 1990", "Pidi Baiq", "Pastel Books", 75000, 35),
]


async def seed():
    """Menginisialisasi tabel dan mengisi data awal ke database."""
    # Pastikan tabel sudah dibuat
    await init_db()

    db = await aiosqlite.connect(DATABASE)
    try:
        # Hapus tabel lama dan buat ulang agar ID dimulai dari 1
        await db.execute("DROP TABLE IF EXISTS transactions")
        await db.execute("DROP TABLE IF EXISTS books")
        await db.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                penulis TEXT NOT NULL,
                penerbit TEXT NOT NULL,
                harga REAL NOT NULL,
                stok INTEGER NOT NULL CHECK(stok >= 0)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                jumlah INTEGER NOT NULL,
                total_harga REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        """)

        # Insert data awal
        await db.executemany(
            "INSERT INTO books (judul, penulis, penerbit, harga, stok) VALUES (?, ?, ?, ?, ?)",
            SEED_DATA,
        )
        await db.commit()
        print(f"✅ Berhasil menambahkan {len(SEED_DATA)} buku ke database.")

        # Tampilkan data yang dimasukkan
        cursor = await db.execute("SELECT * FROM books")
        rows = await cursor.fetchall()
        print("\n📚 Daftar Buku:")
        print(f"{'ID':<4} {'Judul':<25} {'Penulis':<30} {'Harga':>10} {'Stok':>5}")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]:<4} {row[1]:<25} {row[2]:<30} Rp{row[4]:>8,.0f} {row[5]:>5}")
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(seed())
