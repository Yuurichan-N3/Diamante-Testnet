# ⚡ Diamante Testnet Farming Script by Yuurisandesu (佐賀県産 YUURI)

## 📌 Overview  
Dua script Python ini (`tx_V1.py` dan `tx_V2.py`) dirancang untuk mengotomatisasi **farming poin/XP** di **[Diamante Network Campaign Testnet](https://campaign.diamante.io)**.  
**Tujuan utama:** Meningkatkan transaksi, XP, peringkat leaderboard, dan klaim mystery box untuk potensi airdrop/reward.  

Kedua script dibuat oleh author yang sama dengan tampilan banner dan logging yang identik, tetapi memiliki **strategi farming yang berbeda**.

---

## 🔍 Persamaan Kedua Script  
✅ Mengambil private key dari file `.env` (format: `PRIVATEKEY_1=...`, `PRIVATEKEY_2=...`, dst.)  
✅ Mensimulasikan device fingerprint (lokasi Jepang, deviceId unik, variasi IP, latitude/longitude)  
✅ Menggunakan header `access-token` dari `.env` (default: `"key"`)  
✅ Logging berwarna + banner ASCII **"Yuurisandesu"**  
✅ Connect wallet → mendapatkan `userId` → melakukan transfer berulang  
✅ Menangani rate limit (429), token invalid (401/403), serta mekanisme retry  
✅ Berjalan dalam **infinite loop** hingga dihentikan manual (**Ctrl+C**)

---

## ⚖️ Perbedaan Utama

### 🚨 tx_V1.py (Versi 1 – **Kurang Direkomendasikan tapi hemat faucet**)
- **Strategi:** Agresif – membuat akun dummy baru setiap cycle, register dengan referral `"RO5-BL18"`, claim faucet, transfer kecil ke dummy, lalu kirim balik ke fixed address (`0x222306e34a54455aa10c215b26aaad3d6037dbf8`)  
- **Multi Wallet:** Ada, tetapi kurang optimal karena infinite loop di dalam wallet pertama  
- **Input Transfer:** Tidak ada (hardcode, infinite per wallet)  
- **Fitur Tambahan:** Register akun dummy + fake Twitter handle + referral spam  
- **Monitoring:** Basic (balance + leaderboard sekali per wallet)  
- **Cooldown:** Fixed 60 detik  
- **Risiko:** Tinggi – mudah terdeteksi sebagai spam referral dan syphon faucet  
- **Rekomendasi:** ❌ Kurang direkomendasikan (sudah outdated dan campaign semakin ketat)

---

### ✅ tx_V2.py (Versi 2 – **Direkomendasikan**)
- **Strategi:** Aman & sederhana – farming langsung di wallet utama, transfer 1 token ke address random baru (buang token)  
- **Multi Wallet:** Optimal – setiap cycle memproses semua wallet secara bergiliran  
- **Input Transfer:** Ada – user diminta input jumlah transfer per wallet per cycle (rekomendasi: **10**)  
- **Fitur Tambahan:** Login dengan signature, cookie support, monitoring lengkap (user status, mystery box progress tiap transfer, leaderboard tiap 5 transfer, badge info)  
- **Cooldown:** Random 58–60 detik  
- **Risiko:** Rendah – mirip aktivitas user normal  
- **Rekomendasi:** ✅ **Gunakan versi ini saja** – lebih stabil dan aman

**🎯 Kesimpulan:** Gunakan **tx_V2.py** saja. V1 sudah berisiko tinggi dan kurang efektif untuk multi wallet.

---

## 🛠️ Tutorial Penggunaan (Fokus tx_V2.py)

### 1. 📦 Persiapan
- Install **Python 3.10** atau lebih baru
- Install dependencies:
  ```bash
  pip install python-dotenv eth-account colorama pyfiglet faker curl-cffi
  ```

### 2. 📁 Buat file `.env` (di folder yang sama dengan script)
  ```env
  PRIVATEKEY_1=0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
  PRIVATEKEY_2=0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
  # Tambah sebanyak yang kamu mau: PRIVATEKEY_3, PRIVATEKEY_4, dst.
  ```

### 3. ▶️ Jalankan script
  ```bash
  python tx_V2.py
  ```

### 4. 📊 Saat dijalankan
- Script akan menampilkan banner dan meminta **input jumlah transfer per wallet per cycle**
- **Rekomendasi input:** `10` (cukup aman untuk jalan lama tanpa terlalu agresif)
- **Proses yang dilakukan:**
  - Connect semua wallet
  - Login dengan signature
  - Check balance, status, dan leaderboard
  - Lakukan transfer sesuai jumlah yang diinput
  - Claim mystery box otomatis jika eligible
  - Update leaderboard tiap 5 transfer sukses
  - Setelah semua wallet selesai → sleep 60 detik → ulang cycle selamanya

### 5. ⏹️ Menghentikan script
Tekan **Ctrl + C** (akan keluar dengan rapi)

---

## ⚠️ Jika Tetap Ingin Pakai tx_V1.py
Ganti fixed address di baris berikut:
```python
fixed = "0x222306e34a54455aa10c215b26aaad3d6037dbf7"
```
Menjadi:
```python
fixed = "0xYourOwnWalletAddressHere"  # Ganti dengan address web milikmu sendiri
```

**⚠️ Peringatan:** Tetap tidak direkomendasikan karena risiko ban tinggi dan multi-wallet tidak berjalan efektif.

---

## 📝 Catatan Penting
- Script ini dibuat untuk tujuan **edukasi dan testing di jaringan testnet**
- Penulis tidak bertanggung jawab atas kerugian atau konsekuensi yang timbul dari penggunaan script ini
- **Selalu patuhi Terms of Service dari platform yang digunakan**


---
**🚀 Happy Farming & Good Luck on the Leaderboard!**
