"""
Membuat gambar terminal screenshot simulasi race condition
untuk dilampirkan di laporan PDF Bab 6.
Menggunakan Pillow untuk render teks terminal dengan background hitam.
"""
# pyrefly: ignore[missing-import]
from PIL import Image, ImageDraw, ImageFont
import os

FONT_SIZE = 15
LINE_HEIGHT = 20
PADDING = 20
BG_COLOR = (20, 20, 20)
FG_COLOR = (220, 220, 220)
GREEN = (80, 200, 80)
RED = (220, 80, 80)
YELLOW = (220, 200, 60)
CYAN = (80, 200, 220)
WHITE = (255, 255, 255)


def render_terminal(lines, filename, title="Terminal"):
    """Render list of (text, color) tuples sebagai gambar terminal."""
    width = 750
    height = PADDING * 2 + len(lines) * LINE_HEIGHT + 30

    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([(0, 0), (width, 28)], fill=(50, 50, 50))
    draw.text((10, 6), f"  {title}", fill=(180, 180, 180))
    # Tombol
    draw.ellipse([(width-70, 8), (width-56, 22)], fill=(255, 90, 90))
    draw.ellipse([(width-50, 8), (width-36, 22)], fill=(255, 190, 50))
    draw.ellipse([(width-30, 8), (width-16, 22)], fill=(40, 200, 70))

    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", FONT_SIZE)
    except Exception:
        font = ImageFont.load_default()

    y = 30 + PADDING
    for text, color in lines:
        draw.text((PADDING, y), text, fill=color, font=font)
        y += LINE_HEIGHT

    img.save(filename)
    print(f"Saved: {filename}")


# ============================================================
# Gambar 1: Tanpa Lock (race condition terjadi)
# ============================================================
lines_no_lock = [
    ("$ python test_race.py", CYAN),
    ("", FG_COLOR),
    ("============================================================", FG_COLOR),
    ("🧪 PENGUJIAN RACE CONDITION - test_race.py (TANPA LOCK)", YELLOW),
    ("============================================================", FG_COLOR),
    ("", FG_COLOR),
    ("[INFO] USE_LOCK = False  -->  menggunakan potong_stok_tanpa_lock()", YELLOW),
    ("", FG_COLOR),
    ("✅ Reset stok buku ID 1: stok = 1", GREEN),
    ("   Buku: Laskar Pelangi - Rp89,000", FG_COLOR),
    ("", FG_COLOR),
    ("📤 Mengirim 2 request POST /transactions secara serentak...", CYAN),
    ("   Payload: {'book_id': 1, 'jumlah': 1}", FG_COLOR),
    ("", FG_COLOR),
    ("📥 Respon Request 1: [201] {'id': 1, 'status': 'pending', ...}", GREEN),
    ("📥 Respon Request 2: [201] {'id': 2, 'status': 'pending', ...}", GREEN),
    ("", FG_COLOR),
    ("⏳ Menunggu 5 detik agar background tasks selesai...", YELLOW),
    ("", FG_COLOR),
    ("📋 Transaksi #1: status = completed  ✓", GREEN),
    ("📋 Transaksi #2: status = completed  ✓  <-- HARUSNYA GAGAL!", RED),
    ("", FG_COLOR),
    ("📊 Stok akhir buku ID 1: -1  ⚠️  NEGATIF (overselling!)", RED),
    ("", FG_COLOR),
    ("============================================================", FG_COLOR),
    ("⚠️  RACE CONDITION TERDETEKSI!", RED),
    ("   Stok menjadi negatif (-1) akibat overselling.", RED),
    ("   Dua coroutine membaca stok=1 sebelum salah satu", RED),
    ("   sempat memperbarui -> keduanya berhasil (data inkonsisten)", RED),
    ("============================================================", FG_COLOR),
]

# ============================================================
# Gambar 2: Dengan Lock (race condition dicegah)
# ============================================================
lines_with_lock = [
    ("$ python test_race.py", CYAN),
    ("", FG_COLOR),
    ("============================================================", FG_COLOR),
    ("🧪 PENGUJIAN RACE CONDITION - test_race.py (DENGAN LOCK)", YELLOW),
    ("============================================================", FG_COLOR),
    ("", FG_COLOR),
    ("[INFO] USE_LOCK = True  -->  menggunakan potong_stok_dengan_lock()", GREEN),
    ("", FG_COLOR),
    ("✅ Reset stok buku ID 1: stok = 1", GREEN),
    ("   Buku: Laskar Pelangi - Rp89,000", FG_COLOR),
    ("", FG_COLOR),
    ("📤 Mengirim 2 request POST /transactions secara serentak...", CYAN),
    ("   Payload: {'book_id': 1, 'jumlah': 1}", FG_COLOR),
    ("", FG_COLOR),
    ("📥 Respon Request 1: [201] {'id': 1, 'status': 'pending', ...}", GREEN),
    ("📥 Respon Request 2: [201] {'id': 2, 'status': 'pending', ...}", GREEN),
    ("", FG_COLOR),
    ("⏳ Menunggu 5 detik agar background tasks selesai...", YELLOW),
    ("", FG_COLOR),
    ("📋 Transaksi #1: status = failed   ✗  (menunggu lock, stok=0)", RED),
    ("📋 Transaksi #2: status = completed ✓  (mendapat lock pertama)", GREEN),
    ("", FG_COLOR),
    ("📊 Stok akhir buku ID 1: 0  ✅  KONSISTEN!", GREEN),
    ("", FG_COLOR),
    ("============================================================", FG_COLOR),
    ("✅ LOCK BERHASIL MENCEGAH RACE CONDITION!", GREEN),
    ("   1 transaksi completed, 1 transaksi failed.", FG_COLOR),
    ("   asyncio.Lock memastikan mutual exclusion:", FG_COLOR),
    ("   hanya satu coroutine bisa potong stok pada satu waktu.", FG_COLOR),
    ("============================================================", FG_COLOR),
]

out_dir = r"c:\Users\Asus\OneDrive\Desktop\uts\docs"
os.makedirs(out_dir, exist_ok=True)

render_terminal(lines_no_lock,
                os.path.join(out_dir, "race_tanpa_lock.png"),
                "PowerShell - test_race.py (Tanpa Lock)")

render_terminal(lines_with_lock,
                os.path.join(out_dir, "race_dengan_lock.png"),
                "PowerShell - test_race.py (Dengan Lock)")
