# generate_laporan.py - Versi rapi dan profesional

# pyrefly: ignore[missing-import]
from fpdf import FPDF
# pyrefly: ignore[missing-import]
from fpdf.enums import XPos, YPos
import os

# ── Path aset ────────────────────────────────────────────────────────────────
BASE   = r"c:\Users\Asus\OneDrive\Desktop\uts\docs"
LOGO   = os.path.join(BASE, "logo_umpontianak.png")
IMG_NO = os.path.join(BASE, "race_tanpa_lock.png")
IMG_OK = os.path.join(BASE, "race_dengan_lock.png")

# ── Identitas ─────────────────────────────────────────────────────────────────
NAMA     = "Muhammad Rizal Assidiq"
NIM      = "231220126"
PRODI    = "Teknik Informatika"
MK       = "Komputasi Paralel dan Terdistribusi"
DOSEN    = "Yulrio Brianorman, S.Si., M.T."
SEMESTER = "Ganjil 2026/2027"

# ── Palet warna ───────────────────────────────────────────────────────────────
BIRU_TUA  = (0,  51, 102)
BIRU_MUDA = (41, 128, 185)
ABU_TUA   = (60,  60,  60)
ABU_MUDA  = (240, 243, 248)
PUTIH     = (255, 255, 255)
MERAH_TUA = (120,  20,  20)
HIJAU_TUA = (20,  100,  40)


# ─────────────────────────────────────────────────────────────────────────────
class PDF(FPDF):
    # ── Header & Footer ──────────────────────────────────────────────────────
    def header(self):
        if self.page_no() == 1:          # halaman cover tanpa header
            return
        self.set_fill_color(*BIRU_TUA)
        self.rect(0, 0, 210, 11, "F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*PUTIH)
        self.set_y(1.5)
        self.cell(0, 8,
                  f"Laporan UTS  |  {MK}  |  {SEMESTER}",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_text_color(*ABU_TUA)
        self.ln(4)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-13)
        self.set_draw_color(*BIRU_TUA)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*ABU_TUA)
        self.set_y(-11)
        self.cell(95, 7, f"{NAMA}  |  NIM: {NIM}",
                  new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
        self.cell(95, 7, f"Halaman {self.page_no()}/{{nb}}",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

    # ── Judul bab ────────────────────────────────────────────────────────────
    def bab(self, nomor, judul):
        self.set_fill_color(*BIRU_TUA)
        self.set_text_color(*PUTIH)
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 11, f"  {nomor}.  {judul}",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L", fill=True)
        self.ln(4)
        self.set_text_color(*ABU_TUA)

    # ── Sub-judul ────────────────────────────────────────────────────────────
    def sub(self, teks):
        self.ln(2)
        self.set_fill_color(*BIRU_MUDA)
        self.set_text_color(*PUTIH)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 8, f"  {teks}",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L", fill=True)
        self.ln(2)
        self.set_text_color(*ABU_TUA)

    # ── Sub-sub-judul ────────────────────────────────────────────────────────
    def subsub(self, teks):
        self.ln(1)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*BIRU_TUA)
        self.set_draw_color(*BIRU_MUDA)
        self.set_line_width(0.5)
        x = self.get_x()
        y = self.get_y() + 4
        self.line(x, y, x + 4, y)
        self.set_x(x + 6)
        self.cell(0, 7, teks, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(*ABU_TUA)
        self.ln(1)

    # ── Paragraf justified ───────────────────────────────────────────────────
    def p(self, teks):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*ABU_TUA)
        self.multi_cell(0, 5.8, teks, align="J")
        self.ln(2)

    # ── Bullet ───────────────────────────────────────────────────────────────
    def li(self, teks):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*ABU_TUA)
        cx = self.get_x()
        # titik biru
        self.set_fill_color(*BIRU_MUDA)
        self.ellipse(cx + 1, self.get_y() + 3.5, 2.5, 2.5, "F")
        self.set_x(cx + 6)
        self.multi_cell(0, 5.8, teks, align="J")
        self.ln(0.5)

    # ── Tabel header ─────────────────────────────────────────────────────────
    def thead(self, cols, widths, color=None):
        fc = color if color else BIRU_TUA
        self.set_fill_color(*fc)
        self.set_draw_color(*fc)
        self.set_text_color(*PUTIH)
        self.set_font("Helvetica", "B", 9)
        self.set_line_width(0.1)
        for i, c in enumerate(cols):
            self.cell(widths[i], 8, c,
                      border=1, new_x=XPos.RIGHT, new_y=YPos.TOP,
                      align="C", fill=True)
        self.ln()
        self.set_text_color(*ABU_TUA)

    # ── Tabel baris ──────────────────────────────────────────────────────────
    def trow(self, data, widths, aligns=None, stripe=False):
        self.set_font("Helvetica", "", 9)
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.1)
        if stripe:
            self.set_fill_color(*ABU_MUDA)
        else:
            self.set_fill_color(*PUTIH)
        if aligns is None:
            aligns = ["C"] * len(data)
        self.set_text_color(*ABU_TUA)
        for i, d in enumerate(data):
            self.cell(widths[i], 7, str(d),
                      border=1, new_x=XPos.RIGHT, new_y=YPos.TOP,
                      align=aligns[i], fill=True)
        self.ln()

    # ── Gambar berframe dengan caption ──────────────────────────────────────
    def img_frame(self, path, caption, w=170):
        if not os.path.exists(path):
            return
        x0 = (210 - w) / 2
        # background abu frame
        self.set_fill_color(245, 247, 250)
        self.set_draw_color(*BIRU_TUA)
        self.set_line_width(0.4)
        y0 = self.get_y()
        self.rect(x0 - 2, y0 - 1, w + 4, 2, "F")   # top bar biru
        self.set_fill_color(*BIRU_TUA)
        self.rect(x0 - 2, y0 - 1, w + 4, 2, "F")
        # gambar
        self.image(path, x=x0, y=y0 + 2, w=w)
        # hitung tinggi gambar (proporsional)
        # pyrefly: ignore[missing-import]
        from PIL import Image as PILImage
        try:
            with PILImage.open(path) as im:
                iw, ih = im.size
            img_h = w * ih / iw
        except Exception:
            img_h = 55
        y_end = y0 + 2 + img_h
        # bingkai
        self.set_fill_color(245, 247, 250)
        self.rect(x0 - 2, y0 - 1, w + 4, img_h + 7, "D")
        self.ln(img_h + 7)
        # caption
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, caption, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_text_color(*ABU_TUA)
        self.ln(4)

    # ── Kotak info berwarna ───────────────────────────────────────────────────
    def infobox(self, teks, color=None):
        fc = color if color else (230, 243, 255)
        bc = BIRU_MUDA
        self.set_fill_color(*fc)
        self.set_draw_color(*bc)
        self.set_line_width(0.4)
        self.set_font("Helvetica", "I", 9.5)
        self.set_text_color(*ABU_TUA)
        y0 = self.get_y()
        self.rect(10, y0, 190, 1, "F")   # sisi kiri biru tipis
        self.set_fill_color(*bc)
        self.rect(10, y0, 2, 20, "F")
        self.set_x(14)
        self.multi_cell(184, 6, teks, fill=False, align="J")
        self.ln(2)


# ═════════════════════════════════════════════════════════════════════════════
def buat_laporan():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_margins(14, 18, 14)
    pdf.set_auto_page_break(auto=True, margin=18)

    # ═══════════════════════════════════════════════════════════════════════════
    # HALAMAN COVER
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.add_page()

    # Latar belakang atas biru
    pdf.set_fill_color(*BIRU_TUA)
    pdf.rect(0, 0, 210, 85, "F")

    # Logo
    if os.path.exists(LOGO):
        pdf.image(LOGO, x=83, y=10, w=44)

    pdf.set_y(58)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*PUTIH)
    for baris in ["UNIVERSITAS MUHAMMADIYAH PONTIANAK",
                  "FAKULTAS TEKNIK DAN ILMU KOMPUTER",
                  f"PROGRAM STUDI {PRODI.upper()}"]:
        pdf.cell(0, 7, baris, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # Area putih tengah
    pdf.set_fill_color(*PUTIH)
    pdf.rect(0, 85, 210, 100, "F")
    pdf.set_y(92)

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*BIRU_TUA)
    pdf.cell(0, 14, "LAPORAN UTS", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(*BIRU_MUDA)
    pdf.cell(0, 9, MK, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(5)

    # Badge tema
    pdf.set_fill_color(*BIRU_TUA)
    bw = 110
    pdf.set_x((210 - bw) / 2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*PUTIH)
    pdf.cell(bw, 10, '  Tema: "Toko Buku API"  ',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)
    pdf.ln(10)

    # Tabel identitas
    col_l, col_s, col_v = 42, 6, 100
    total_w = col_l + col_s + col_v
    start_x = (210 - total_w) / 2
    identitas = [
        ("Nama",        NAMA),
        ("NIM",         NIM),
        ("Program Studi", PRODI),
        ("Mata Kuliah", MK),
        ("Dosen",       DOSEN),
        ("Semester",    SEMESTER),
    ]
    for label, val in identitas:
        pdf.set_x(start_x)
        pdf.set_fill_color(*ABU_MUDA)
        pdf.set_draw_color(200, 210, 230)
        pdf.set_line_width(0.1)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*BIRU_TUA)
        pdf.cell(col_l, 7.5, label, border=1,
                 new_x=XPos.RIGHT, new_y=YPos.TOP, align="L", fill=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*ABU_TUA)
        pdf.set_fill_color(*PUTIH)
        pdf.cell(col_s, 7.5, ":", border=1,
                 new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
        pdf.cell(col_v, 7.5, val, border=1,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L", fill=True)

    # Latar belakang bawah
    pdf.set_fill_color(*BIRU_TUA)
    pdf.rect(0, 268, 210, 30, "F")
    pdf.set_y(274)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(*PUTIH)
    pdf.cell(0, 7, "Pontianak, November 2026", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # ═══════════════════════════════════════════════════════════════════════════
    # BAB 1 - DESKRIPSI APLIKASI
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.bab("1", "Deskripsi Aplikasi")

    pdf.sub("1.1  Tema Aplikasi")
    pdf.p(
        "Aplikasi yang dikembangkan adalah Toko Buku API, sebuah REST API untuk manajemen "
        "toko buku online. Aplikasi mengelola dua resource utama: Buku (resource utama dengan "
        "kolom stok) dan Transaksi Pembelian (resource transaksi). Dibangun menggunakan "
        "FastAPI (Python 3.10+) dengan SQLite yang diakses secara asinkron melalui aiosqlite."
    )

    pdf.sub("1.2  Fitur Utama")
    for f in [
        "CRUD lengkap untuk data buku: Create, Read, Update, Delete (hard delete)",
        "Transaksi pembelian buku dengan pemrosesan asinkron menggunakan BackgroundTasks FastAPI",
        "Alur status transaksi otomatis: pending  ->>  processing  ->>  completed / failed",
        "Pencegahan race condition pada pengurangan stok menggunakan asyncio.Lock",
        "Validasi request body menggunakan model Pydantic dengan pesan error deskriptif",
        "Pagination pada endpoint list (parameter ?skip=0&limit=10)",
        "Filter transaksi berdasarkan status (?status=pending / processing / completed / failed)",
    ]:
        pdf.li(f)

    pdf.sub("1.3  Batasan Sistem")
    for b in [
        "Hanya mendukung satu resource utama (buku) dan satu resource transaksi (pembelian)",
        "Tidak ada sistem autentikasi atau otorisasi pengguna",
        "SQLite bersifat file-based; file-level locking membatasi performa write pada multi-worker",
        "asyncio.Lock hanya efektif dalam satu proses worker; multi-worker membutuhkan distributed lock",
    ]:
        pdf.li(b)

    # ═══════════════════════════════════════════════════════════════════════════
    # BAB 2 - PEMAHAMAN KONSEP
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.bab("2", "Bagian A - Pemahaman Konsep")

    pdf.sub("A1 - Concurrency vs. Paralelisme")

    pdf.subsub("a.  Bagian sistem yang bersifat concurrent (I/O-bound)")
    pdf.p(
        "Seluruh operasi database pada Toko Buku API bersifat I/O-bound dan concurrent. "
        "Operasi SELECT, INSERT, UPDATE, DELETE pada tabel books dan transactions menggunakan "
        "aiosqlite secara asinkron. Ketika satu request menunggu respons database (await db.execute()), "
        "event loop asyncio dapat memproses request lain tanpa memblokir. Contoh: saat endpoint "
        "GET /books menunggu query SELECT, endpoint POST /transactions dari klien lain langsung "
        "diproses oleh event loop yang sama. BackgroundTasks pada POST /transactions juga I/O-bound, "
        "disimulasikan dengan await asyncio.sleep(3) sebagai representasi operasi I/O intensif."
    )

    pdf.subsub("b.  Bagian yang berpotensi membutuhkan paralelisme (CPU-bound)")
    pdf.p(
        "Aplikasi saat ini belum memiliki bagian CPU-bound yang intensif. Potensi CPU-bound "
        "muncul jika ditambahkan: pembuatan laporan penjualan dengan kalkulasi statistik kompleks, "
        "pemrosesan gambar cover buku (resize/watermark), atau analisis tren pembelian dengan "
        "machine learning. Bagian-bagian ini membutuhkan modul multiprocessing Python untuk "
        "paralelisme sejati lintas core CPU."
    )

    pdf.subsub("c.  Python GIL dan solusi multi-worker Uvicorn")
    pdf.p(
        "Python GIL (Global Interpreter Lock) adalah mutex yang memastikan hanya satu thread "
        "yang mengeksekusi bytecode Python pada satu waktu dalam satu proses. Akibatnya, "
        "threading tidak dapat mencapai paralelisme sejati untuk tugas CPU-bound."
    )
    pdf.p(
        "Multi-worker Uvicorn mengatasi GIL dengan menjalankan beberapa proses Python "
        "independen, bukan thread. Setiap worker memiliki GIL-nya sendiri. Dengan perintah "
        "'uvicorn main:app --workers 4', sistem membuat 4 proses yang berjalan paralel di "
        "core CPU berbeda. Masing-masing memiliki event loop asyncio untuk menangani "
        "I/O-bound concurrency, sehingga throughput meningkat signifikan pada beban tinggi."
    )

    pdf.add_page()
    pdf.sub("A2 - Arsitektur dan Alur Data")

    pdf.subsub("a.  Diagram Arsitektur Aplikasi")
    pdf.ln(2)
    pdf.set_font("Courier", "", 7)
    pdf.set_text_color(30, 30, 30)
    for baris in [
        "+------------------------------------------------------------------+",
        "|              CLIENT  (Browser / Postman / httpx)                |",
        "+------------------------------------------------------------------+",
        "         |  HTTP Request                    ^ HTTP Response        ",
        "         v                                  |                      ",
        "+------------------------------------------------------------------+",
        "|              FastAPI Application  (main.py)                     |",
        "|  +------------------------+  +--------------------------------+ |",
        "|  | routes/resource.py     |  | routes/transaction.py          | |",
        "|  |  GET    /books         |  |  POST  /transactions           | |",
        "|  |  GET    /books/{id}    |  |  GET   /transactions           | |",
        "|  |  POST   /books         |  |  GET   /transactions/{id}      | |",
        "|  |  PUT    /books/{id}    |  |                                | |",
        "|  |  DELETE /books/{id}    |  | +----------------------------+ | |",
        "|  +------------------------+  | | BackgroundTasks            | | |",
        "|                              | |  pending -> processing ->  | | |",
        "|  Validasi  Pydantic          | |  completed / failed        | | |",
        "|  - BookCreate / BookUpdate   | +----------------------------+ | |",
        "|  - TransactionCreate         | +----------------------------+ | |",
        "|                              | | asyncio.Lock               | | |",
        "|                              | | potong_stok_dengan_lock()  | | |",
        "|                              | | (mutual exclusion)         | | |",
        "|                              | +----------------------------+ | |",
        "|                              +--------------------------------+ |",
        "+------------------------------------------------------------------+",
        "         |  async / await  (non-blocking I/O via aiosqlite)        ",
        "         v                                                          ",
        "+------------------------------------------------------------------+",
        "|           SQLite Database  -  toko_buku.db                      |",
        "|  +-------------------------+  +--------------------------------+ |",
        "|  | Tabel: books            |  | Tabel: transactions            | |",
        "|  | id, judul, penulis,     |  | id, book_id, jumlah,           | |",
        "|  | penerbit, harga,        |  | total_harga, status,           | |",
        "|  | stok  INTEGER >= 0      |  | created_at                     | |",
        "|  +-------------------------+  +--------------------------------+ |",
        "+------------------------------------------------------------------+",
    ]:
        pdf.cell(0, 3.4, baris, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "Gambar 2.1 - Diagram Arsitektur Toko Buku API",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_text_color(*ABU_TUA)
    pdf.ln(4)

    pdf.subsub("b.  Alur Data Siklus Transaksi Lengkap")
    langkah = [
        ("1.",  "Client mengirim POST /transactions dengan body JSON {book_id, jumlah}."),
        ("2.",  "FastAPI menerima request; Pydantic memvalidasi format data secara otomatis."),
        ("3.",  "Endpoint memverifikasi keberadaan buku di database melalui aiosqlite."),
        ("4.",  "Transaksi disimpan ke tabel transactions dengan status awal 'pending'."),
        ("5.",  "BackgroundTasks FastAPI mendaftarkan fungsi proses_transaksi_background()."),
        ("6.",  "Response dikembalikan instan ke client {id, status:'pending'} tanpa blocking."),
        ("7.",  "Di latar belakang: status diperbarui menjadi 'processing'."),
        ("8.",  "Simulasi pemrosesan I/O intensif: await asyncio.sleep(3)."),
        ("9.",  "Fungsi potong_stok_dengan_lock() dipanggil dengan asyncio.Lock."),
        ("10.", "Critical section: hanya satu coroutine berjalan di dalam blok lock."),
        ("11.", "Stok dibaca, dicek, dan dikurangi secara atomik."),
        ("12.", "Jika stok cukup  ->> status 'completed', total_harga = harga x jumlah."),
        ("13.", "Jika stok habis  ->> status 'failed', stok tidak berubah."),
        ("14.", "Client memantau status terkini melalui GET /transactions/{id}."),
    ]
    for no, teks in langkah:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*BIRU_TUA)
        pdf.cell(10, 6, no, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*ABU_TUA)
        pdf.multi_cell(0, 6, teks, align="J")
        pdf.ln(0.5)

    # ═══════════════════════════════════════════════════════════════════════════
    # BAB 3 - TABEL ENDPOINT
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.bab("3", "Tabel Endpoint API")

    pdf.sub("3.1  Daftar Endpoint")
    W = [22, 50, 85, 25]
    pdf.thead(["Method", "Path", "Deskripsi Fungsi", "Status"], W)
    rows = [
        ("GET",    "/",                   "Root endpoint, menampilkan info API",           "200"),
        ("GET",    "/books",              "Daftar buku dengan paginasi (skip, limit)",     "200"),
        ("GET",    "/books/{id}",         "Detail satu buku berdasarkan ID",               "200/404"),
        ("POST",   "/books",              "Tambah buku baru, validasi Pydantic",           "201"),
        ("PUT",    "/books/{id}",         "Perbarui data buku, kembalikan data terbaru",   "200/404"),
        ("DELETE", "/books/{id}",         "Hapus permanen buku dari database (hard delete)","200/404"),
        ("POST",   "/transactions",       "Buat transaksi (async, response instan pending)","201"),
        ("GET",    "/transactions",       "Daftar transaksi; filter ?status=...",          "200"),
        ("GET",    "/transactions/{id}",  "Detail transaksi beserta status terkini",       "200/404"),
    ]
    for i, r in enumerate(rows):
        pdf.trow(r, W, aligns=["C","L","L","C"], stripe=(i%2==0))

    pdf.ln(5)
    pdf.sub("3.2  HTTP Status Code")
    kodes = [
        ("200 OK",                   "Operasi GET, PUT, DELETE berhasil"),
        ("201 Created",              "Resource baru berhasil dibuat (POST /books, POST /transactions)"),
        ("404 Not Found",            "Resource dengan ID yang diminta tidak ditemukan"),
        ("409 Conflict",             "Stok buku tidak mencukupi untuk transaksi"),
        ("422 Unprocessable Entity", "Request body tidak sesuai skema Pydantic"),
    ]
    WK = [60, 122]
    pdf.thead(["Status Code", "Keterangan"], WK)
    for i, (k, v) in enumerate(kodes):
        pdf.trow((k, v), WK, aligns=["C","L"], stripe=(i%2==0))

    # ═══════════════════════════════════════════════════════════════════════════
    # BAB 4 - BENCHMARK
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.bab("4", "Hasil Benchmark - 1 Worker vs 4 Worker")

    pdf.sub("4.1  Konfigurasi Pengujian")
    for k in [
        "Tool: script asyncio + httpx (benchmark_manual.py)",
        "Skenario Read  : GET /books?skip=0&limit=10 -- 100 request serentak",
        "Skenario Write : POST /transactions {book_id:3, jumlah:1} -- 50 request serentak",
        "Server 1 Worker: uvicorn main:app --workers 1 --port 8000",
        "Server 4 Worker: uvicorn main:app --workers 4 --port 8000",
        "Mesin pengujian: perangkat yang sama, tanpa beban proses lain",
    ]:
        pdf.li(k)
    pdf.ln(3)

    pdf.sub("4.2  Tabel Hasil Benchmark")
    WB = [42, 18, 32, 36, 36, 18]
    pdf.thead(["Skenario", "Worker", "Total Waktu", "Throughput", "Avg Latensi", "Sukses"], WB)
    bm = [
        ("GET /books",        "1", "0.97 detik", "103.3 req/s", "9.7 ms",  "100/100"),
        ("GET /books",        "4", "0.85 detik", "117.4 req/s", "8.5 ms",  "100/100"),
        ("POST /transactions","1", "2.89 detik", "17.3 req/s",  "57.7 ms", "50/50"),
        ("POST /transactions","4", "4.04 detik", "12.4 req/s",  "80.8 ms", "50/50"),
    ]
    ba = ["L","C","C","C","C","C"]
    for i, r in enumerate(bm):
        pdf.trow(r, WB, aligns=ba, stripe=(i%2==0))
    pdf.ln(4)

    pdf.sub("4.3  Tabel Perbandingan Peningkatan Performa")
    WC = [42, 36, 36, 32, 32, 4]
    # Header 2 baris: gunakan kolom multi-info
    WC2 = [42, 36, 36, 36, 32]
    pdf.thead(["Skenario", "Throughput 1W", "Throughput 4W", "Delta Throughput", "Delta Latensi"], WC2)
    cmp = [
        ("GET /books",         "103.3 req/s", "117.4 req/s", "+13.7%  (naik)",    "-1.2 ms"),
        ("POST /transactions", "17.3 req/s",  "12.4 req/s",  "-28.3%  (turun) *", "+23.1 ms"),
    ]
    for i, r in enumerate(cmp):
        pdf.trow(r, WC2, aligns=["L","C","C","C","C"], stripe=(i%2==0))
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(120, 60, 0)
    pdf.p("* Penurunan throughput write pada 4 worker disebabkan SQLite file-level locking "
          "dan overhead komunikasi antar proses yang lebih besar dari keuntungan parallelisme.")
    pdf.set_text_color(*ABU_TUA)

    # ═══════════════════════════════════════════════════════════════════════════
    # BAB 5 - ANALISIS PERFORMA
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.bab("5", "Analisis Performa")

    pdf.sub("5.1  Skenario Read - GET /books")
    pdf.p(
        "Throughput meningkat dari 103.3 menjadi 117.4 req/s (+13.7%), dan latensi turun "
        "dari 9.7 ms ke 8.5 ms dengan 4 worker. Endpoint GET /books bersifat murni I/O-bound "
        "(hanya SELECT tanpa write), sehingga 4 event loop paralel efektif mengurangi antrian "
        "request per worker. Peningkatan tidak linier karena overhead spawning proses, "
        "shared SQLite file I/O, dan 1 worker sudah cukup efisien untuk read-only berkat asyncio."
    )

    pdf.sub("5.2  Skenario Write - POST /transactions")
    pdf.p(
        "Throughput menurun dari 17.3 menjadi 12.4 req/s (-28.3%) dengan 4 worker, dan latensi "
        "naik dari 57.7 ms ke 80.8 ms. Faktor penyebab: (1) SQLite file-level locking -- saat "
        "INSERT, hanya satu writer yang diizinkan pada satu waktu, sehingga 4 worker "
        "mengantri secara serial; (2) asyncio.Lock bersifat per-proses dan tidak berkoordinasi "
        "antar worker, menambah potensi konflik; (3) overhead IPC (inter-process communication) "
        "dari Uvicorn parent ke child worker."
    )

    pdf.sub("5.3  Kesimpulan")
    pdf.p(
        "Multi-worker Uvicorn efektif untuk workload read-heavy. Untuk write-heavy dengan SQLite, "
        "penambahan worker justru menurunkan performa. Rekomendasi untuk skala produksi: "
        "gunakan PostgreSQL + asyncpg yang mendukung concurrent writes, dan Redis untuk "
        "distributed locking lintas worker (akan diimplementasikan pada UAS)."
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # BAB 6 - RACE CONDITION
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.bab("6", "Hasil Pengujian Race Condition (B3)")

    pdf.p(
        "Pengujian dilakukan dengan script test_race.py yang mengirimkan 2 request "
        "POST /transactions secara serentak dengan stok awal buku = 1. Dua kondisi diuji "
        "melalui toggle variabel USE_LOCK pada routes/transaction.py."
    )

    pdf.sub("6.1  Tabel Ringkasan Hasil Pengujian")
    WR = [38, 28, 28, 30, 58]
    pdf.thead(["Kondisi", "Request 1", "Request 2", "Stok Akhir", "Kesimpulan"], WR,
              color=BIRU_TUA)
    rc = [
        ("Tanpa Lock\n(USE_LOCK=False)", "completed", "completed", "-1 (negatif)", "RACE CONDITION / Overselling"),
        ("Dengan Lock\n(USE_LOCK=True)", "completed", "failed",    "0 (konsisten)", "AMAN / Data konsisten"),
    ]
    rca = ["C","C","C","C","L"]
    for i, r in enumerate(rc):
        pdf.trow(r, WR, aligns=rca, stripe=(i%2==0))
    pdf.ln(5)

    # Gambar tanpa lock
    pdf.sub("6.2  Tahap 1 - Tanpa Lock  (USE_LOCK = False)")
    pdf.p(
        "Tanpa asyncio.Lock, dua coroutine membaca stok=1 secara bersamaan, keduanya melewati "
        "pengecekan, dan keduanya mengurangi stok. Stok akhir menjadi -1 (overselling). "
        "Ini adalah race condition klasik pada operasi baca-ubah-tulis."
    )
    pdf.img_frame(IMG_NO, "Gambar 6.1 - Terminal output test_race.py TANPA asyncio.Lock "
                           "(stok = -1, kedua transaksi completed)", w=174)

    # Gambar dengan lock
    pdf.add_page()
    pdf.sub("6.3  Tahap 2 - Dengan Lock  (USE_LOCK = True)")
    pdf.p(
        "Dengan asyncio.Lock, blok 'async with stok_lock:' memastikan mutual exclusion. "
        "Coroutine pertama mendapat lock, membaca stok=1, mengurangi ke 0, lalu melepas lock. "
        "Coroutine kedua baru mendapat lock, membaca stok=0, menemukan stok habis, dan "
        "mengembalikan False. Hasil: 1 completed, 1 failed -- stok akhir = 0 (konsisten)."
    )
    pdf.img_frame(IMG_OK, "Gambar 6.2 - Terminal output test_race.py DENGAN asyncio.Lock "
                           "(stok = 0, 1 completed + 1 failed)", w=174)

    pdf.sub("6.4  Analisis Mekanisme asyncio.Lock")
    pdf.p(
        "asyncio.Lock bekerja sebagai mutex pada level coroutine dalam satu event loop. "
        "Ketika coroutine pertama mengakuisisi lock ('async with stok_lock:'), coroutine lain "
        "yang mencoba masuk akan di-suspend dan menunggu di queue internal asyncio. "
        "Setelah blok selesai, lock dilepas otomatis dan coroutine berikutnya masuk. "
        "Mekanisme ini memastikan operasi baca-cek-tulis stok bersifat atomik, mencegah "
        "dua coroutine membaca nilai stok yang sama sebelum salah satu memperbarui. "
        "Hasilnya: data inventory selalu konsisten meskipun ada request bersamaan."
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # BAB 7 - REFERENSI
    # ═══════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.bab("7", "Referensi")
    refs = [
        ("[1]", "FastAPI Documentation",           "https://fastapi.tiangolo.com"),
        ("[2]", "Python asyncio",                  "https://docs.python.org/3/library/asyncio.html"),
        ("[3]", "aiosqlite Documentation",         "https://aiosqlite.omnilib.dev"),
        ("[4]", "Uvicorn Documentation",           "https://www.uvicorn.org"),
        ("[5]", "Locust Load Testing",             "https://locust.io"),
        ("[6]", "Pydantic Documentation",          "https://docs.pydantic.dev"),
        ("[7]", "SQLite Documentation",            "https://www.sqlite.org/docs.html"),
        ("[8]", "Python multiprocessing",          "https://docs.python.org/3/library/multiprocessing.html"),
    ]
    WF = [12, 70, 100]
    pdf.thead(["No.", "Sumber", "URL"], WF)
    for i, (no, src, url) in enumerate(refs):
        pdf.trow((no, src, url), WF, aligns=["C","L","L"], stripe=(i%2==0))

    # Simpan
    out = os.path.join(BASE, "laporan_uts.pdf")
    pdf.output(out)
    print(f"PDF berhasil dibuat: {out}")


if __name__ == "__main__":
    buat_laporan()
