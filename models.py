# models.py: Skema Pydantic untuk validasi request dan serialisasi response
# Pydantic digunakan untuk memastikan data yang masuk sesuai format yang diharapkan

# pyrefly: ignore[missing-import]
from pydantic import BaseModel, Field
from typing import Optional


# ==================== Skema Buku (Resource Utama) ====================

class BookCreate(BaseModel):
    """Skema untuk membuat buku baru. Semua field wajib diisi."""
    judul: str = Field(..., min_length=1, description="Judul buku")
    penulis: str = Field(..., min_length=1, description="Nama penulis")
    penerbit: str = Field(..., min_length=1, description="Nama penerbit")
    harga: float = Field(..., gt=0, description="Harga buku (harus positif)")
    stok: int = Field(..., ge=0, description="Jumlah stok buku")


class BookUpdate(BaseModel):
    """Skema untuk memperbarui data buku. Semua field opsional."""
    judul: Optional[str] = Field(None, min_length=1, description="Judul buku")
    penulis: Optional[str] = Field(None, min_length=1, description="Nama penulis")
    penerbit: Optional[str] = Field(None, min_length=1, description="Nama penerbit")
    harga: Optional[float] = Field(None, gt=0, description="Harga buku")
    stok: Optional[int] = Field(None, ge=0, description="Jumlah stok buku")


class BookResponse(BaseModel):
    """Skema response untuk data buku."""
    id: int
    judul: str
    penulis: str
    penerbit: str
    harga: float
    stok: int


# ==================== Skema Transaksi ====================

class TransactionCreate(BaseModel):
    """Skema untuk membuat transaksi baru."""
    book_id: int = Field(..., description="ID buku yang dibeli")
    jumlah: int = Field(..., gt=0, description="Jumlah buku yang dibeli")


class TransactionResponse(BaseModel):
    """Skema response untuk data transaksi."""
    id: int
    book_id: int
    jumlah: int
    total_harga: float
    status: str
    created_at: Optional[str] = None
