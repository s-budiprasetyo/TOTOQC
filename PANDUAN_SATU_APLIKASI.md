# Satu aplikasi, dua halaman — cara pasang

## Cara kerja singkat
Satu alamat web. Halaman utama terbuka seperti biasa. Setelah admin login, muncul tombol **⚙ HALAMAN ADMIN** di pojok kiri atas.
Di halaman admin ada tombol **← HALAMAN UTAMA**. Setiap pindah halaman, jendela/isian/unggahan halaman lama dibersihkan,
hanya status login yang terbawa. Alamat `...?hal=admin` membuka halaman admin langsung (tetap minta user + password admin).

## Pasang di Streamlit Cloud (tanpa mengubah pengaturan Google Login)
1. Ekstrak zip, unggah isi folder ke GitHub (timpa), Commit. (File baru: `app.py`, `core/nav.py`, `PANDUAN_SATU_APLIKASI.md`.)
2. Buka **Secrets app utama** (alamat yang dipakai karyawan). Tambahkan di **PALING ATAS**, sebelum baris `[auth]` / `[gcp_service_account]` / `[admin]`:
   ```
   satu_app = true
   drive_folder_id = "ISI_DARI_SECRETS_APP_ADMIN"
   ```
   PENTING: kunci tanpa kurung siku harus di atas semua `[...]`. Kalau ditaruh di bawah, ia ikut masuk tabel di atasnya dan tidak terbaca.
3. Pastikan bagian `[admin]` (user, password) ada di Secrets app utama. Salin dari Secrets app admin bila belum ada.
   Bila `emails = [...]` diisi dan `[auth]` aktif, admin juga harus login Google dengan email itu; bila kosong, cukup user + password.
4. **Reboot** app utama. Login sebagai admin → tombol ⚙ HALAMAN ADMIN muncul.
5. Setelah yakin, app admin lama boleh dibiarkan sebagai cadangan atau dihapus. Untuk kembali ke dua app: hapus baris `satu_app = true` lalu Reboot.

## Uji di komputer sendiri
`pip install -r requirements.txt` lalu `streamlit run app.py` (tanpa `sheet_id` di secrets, data disimpan di folder `data/`).
