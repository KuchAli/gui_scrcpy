# GUI SCRCPY

Antarmuka grafis (GUI) sederhana untuk [scrcpy](https://github.com/Genymobile/scrcpy), dibuat dengan Python dan PyQt6. Tampilkan dan kontrol layar HP Android dari PC Windows tanpa perlu mengetik perintah di terminal.

> Build 1.0 oleh Mister K

<img src="assets/icons/logos.png" alt="Icon GUISCRCPY"  width="450" >

<!-- Tambahkan screenshot aplikasi di sini, contoh:
![Screenshot](assets/screenshot.png)
-->

## Fitur

- Mulai dan hentikan scrcpy dengan satu tombol
- Opsi cepat: Fullscreen, Keep display off, Show touches, Record screen, Lock rotation
- Pengaturan rotasi layar dan bitrate (dial atau input manual)
- Kolom flag tambahan untuk argumen scrcpy kustom
- Kontrol volume HP (naik, turun, mute)
- Restart ADB server dan cek perangkat yang terhubung

## Download dan Install

1. Buka halaman [Releases](https://github.com/KuchAli/gui_scrcpy/releases/latest).
2. Unduh `GUIScrcpy_Setup_1.0.exe`.
3. Jalankan installer dan ikuti wizard sampai selesai.

Installer tidak membutuhkan hak admin dan terpasang di profil pengguna. Adb dan scrcpy sudah disertakan, jadi tidak perlu install apa pun lagi.

### Peringatan Windows SmartScreen

Aplikasi ini belum ditandatangani dengan code signing certificate, jadi Windows mungkin menampilkan peringatan "Unknown publisher". Klik **More info → Run anyway** untuk melanjutkan.

Kamu bisa memverifikasi keaslian file dengan membandingkan hash SHA-256 yang tertera di halaman rilis:

```
certutil -hashfile GUIScrcpy_Setup_1.0.exe SHA256
```

## Persiapan di HP

1. Buka **Pengaturan → Tentang ponsel**, ketuk **Nomor build** 7 kali untuk mengaktifkan Opsi Developer.
2. Buka **Opsi Developer** dan aktifkan **USB debugging**.

## Cara Pakai

### Lewat USB

1. Colok HP ke PC dan izinkan USB debugging di layar HP.
2. Klik ikon Android untuk mengecek perangkat terdeteksi.
3. Pilih opsi yang diinginkan, lalu klik **START SCRCPY**.

<!-- ### Lewat Wi-Fi (Wireless Debugging)

Klik ikon Wi-Fi, lalu pilih salah satu metode:

| Metode | Kapan dipakai |
|---|---|
| Pairing via QR Code | Pertama kali, HP dan PC di jaringan yang sama |
| Pairing via Kode | Kalau QR tidak terdeteksi (mDNS sering diblokir hotspot) |
| Connect Langsung | HP sudah pernah di-pair, tinggal masukkan IP:Port |
| Aktifkan Wireless via USB | Cara paling stabil: colok USB sekali, lalu cabut kabel |

Catatan penting:

- Port **pairing** dan port **connect** itu berbeda. Port connect ada di layar utama menu Wireless debugging.
- Di jaringan hotspot atau router dengan client isolation, QR sering gagal. Pakai metode kode atau metode USB.
- Kalau USB dan Wi-Fi tersambung bersamaan, aplikasi otomatis memilih perangkat wireless. -->

<!-- ## Menjalankan dari Source

Disarankan Python 3.12 atau 3.13.

```
git clone https://github.com/KuchAli/gui_scrcpy.git
cd gui_scrcpy
python -m venv env
env\Scripts\activate
pip install PyQt6 "qrcode[pil]"
python main.py
```

Letakkan `scrcpy.exe` dan `adb.exe` di folder `scrcpy/`. Kalau folder itu tidak ada, aplikasi akan memakai `scrcpy` dan `adb` dari PATH sistem. Binary scrcpy bisa diunduh dari [halaman rilis scrcpy](https://github.com/Genymobile/scrcpy/releases).

### Struktur proyek

```
gui_scrcpy/
├── main.py
├── src/
│   ├── __init__.py
│   └── utils.py        # helper path, ADB, dan Wireless Debugging
├── assets/
│   ├── icons/
│   └── style.qss
└── scrcpy/             # scrcpy.exe dan adb.exe
```

## Build Exe dan Installer

```
pip install pyinstaller
python -m PyInstaller --noconfirm --clean GUIScrcpy.spec
```

Hasil build ada di `dist\GUIScrcpy\`. Untuk membuat installer, buka `installer.iss` dengan [Inno Setup](https://jrsoftware.org/isinfo.php) 6.x dan compile (Ctrl+F9). Installer keluar di `installer_output\`. -->

<!-- ## Troubleshooting

- **Perangkat tidak terdeteksi:** pastikan USB debugging aktif dan layar HP sudah menyetujui koneksi. Coba tombol restart ADB.
- **Gagal connect wireless:** pastikan sudah pairing, port yang dipakai adalah port connect, dan HP serta PC di jaringan yang sama.
- **Error "more than one device":** cabut salah satu koneksi, atau gunakan aplikasi ini yang otomatis memilih perangkat wireless.
- **Opsi rotasi tidak jalan:** di scrcpy 3.x flag `--lock-video-orientation` diganti `--capture-orientation`. Sesuaikan versi scrcpy yang kamu pakai.
- **Antivirus menandai file:** ini false positive yang umum untuk aplikasi buatan PyInstaller. Kamu bisa membangun sendiri dari source. -->

## Kredit dan Lisensi

- [scrcpy](https://github.com/Genymobile/scrcpy) oleh Genymobile, dilisensikan di bawah Apache License 2.0. Binary-nya disertakan beserta lisensinya.
- [GUIScrcpy](https://github.com/KuchAli/gui_scrcpy) oleh Mister K, dilisensikan di bawah MIT. Oktober 2026.
<!-- - [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) untuk antarmuka.
- [python-qrcode](https://github.com/lincolnloop/python-qrcode) untuk pembuatan QR pairing. -->

Lisensi proyek ini: MIT LICENSE - Mister K 2026
