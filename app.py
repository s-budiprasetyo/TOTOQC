"""SATU APLIKASI, DUA HALAMAN (halaman utama + halaman admin).
Jalankan: streamlit run app.py
Halaman admin dibuka lewat tombol "HALAMAN ADMIN" (muncul hanya setelah admin login di halaman utama)
atau lewat alamat ...?hal=admin (tetap dijaga user + password admin)."""
import os

from core import nav

nav.jalankan(os.path.dirname(os.path.abspath(__file__)))
