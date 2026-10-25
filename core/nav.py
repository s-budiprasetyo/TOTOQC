"""Satu aplikasi, dua halaman — TANPA st.navigation.

Cara kerja:
- Halaman aktif disimpan di st.session_state["halaman"] ("utama" atau "admin").
- Setiap halaman tetap berupa file sendiri (app_publik.py dan app_admin.py) yang dijalankan
  APA ADANYA, satu per satu, dalam "modul" bernama sendiri. Isi kedua file tidak digabung.
- Saat pindah halaman, semua state milik halaman lama dibersihkan (kecuali status login),
  sehingga jendela, unggahan, tabel isian, dan klik yang tertunda tidak bocor ke halaman lain.
"""
import sys
import types

import streamlit as st

HALAMAN = {"utama": "app_publik.py", "admin": "app_admin.py"}
JUDUL = "Monitoring QC TOTO"

# Satu-satunya state yang boleh terbawa antar halaman: siapa yang login + halaman aktif.
PERTAHAN = {"halaman", "_pindah", "me", "me_nama", "adm", "admin_ok", "gagal"}


def aktif():
    """True bila halaman dijalankan lewat app.py (satu aplikasi)."""
    return "halaman" in st.session_state


def ke(tujuan):
    """Dipakai sebagai on_click: minta pindah halaman pada run berikutnya."""
    st.session_state["_pindah"] = tujuan


def _bersihkan():
    for k in list(st.session_state.keys()):
        if k not in PERTAHAN:
            try:
                del st.session_state[k]
            except Exception:
                pass


def _jalankan_file(nama_modul, path):
    """Menjalankan satu file halaman seperti Streamlit menjalankan skrip, tapi di modul bernama sendiri."""
    with open(path, encoding="utf-8") as f:
        kode = compile(f.read(), path, "exec")
    modul = types.ModuleType(nama_modul)
    modul.__file__ = path
    sys.modules[nama_modul] = modul
    exec(kode, modul.__dict__)


_CSS_BAR = """<style>
/* tombol pindah halaman melayang di pojok kiri atas (bidang header kosong): tata letak kedua halaman tidak bergeser */
.st-key-navbar{position:fixed;top:10px;left:16px;z-index:999995;width:auto !important}
.st-key-navbar button{min-height:36px;height:36px;padding:0 .9rem;white-space:nowrap;background:#fff;border:1px solid #00B0F0;font-weight:600}
.st-key-navbar button:hover{background:#e8f6fd;border-color:#00B0F0}
.st-key-navbar button p{font-size:.85rem}
</style>"""


def _bar(hal):
    """Tombol pindah halaman (melayang di pojok kiri atas)."""
    if hal == "utama" and not st.session_state.get("adm"):
        return  # hanya admin yang melihat tombol menuju halaman admin
    st.markdown(_CSS_BAR, unsafe_allow_html=True)
    with st.container(key="navbar"):
        if hal == "utama":
            st.button("⚙ HALAMAN ADMIN", key="nav_admin", on_click=ke, args=("admin",), width="content")
        else:
            st.button("← HALAMAN UTAMA", key="nav_utama", on_click=ke, args=("utama",), width="content")


def jalankan(folder):
    """Titik masuk satu aplikasi. folder = folder tempat app_publik.py dan app_admin.py berada."""
    import os

    st.set_page_config(page_title=JUDUL, layout="wide")
    if "halaman" not in st.session_state:
        st.session_state["halaman"] = "admin" if st.query_params.get("hal") == "admin" else "utama"
    tujuan = st.session_state.pop("_pindah", None)
    if tujuan in HALAMAN and tujuan != st.session_state["halaman"]:
        _bersihkan()
        st.session_state["halaman"] = tujuan
    hal = st.session_state["halaman"]
    if not (hal == "utama" and st.query_params.get("privasi") is not None):  # halaman privasi tanpa tombol
        _bar(hal)
    _jalankan_file(f"halaman_{hal}", os.path.join(folder, HALAMAN[hal]))
