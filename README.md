✋ Gesture AI Project (Hand Tracking)

Project ini menggunakan MediaPipe + OpenCV untuk mendeteksi gesture tangan secara realtime dari kamera dan menerjemahkannya menjadi teks di layar.

---

🎯 Fitur

- Deteksi tangan realtime (webcam)
- Hitung jumlah jari
- Gesture → teks (AKU, MAU, MAKAN, dll)
- Bisa gabung jadi kalimat sederhana
- Support 1–2 tangan

---

🧠 Contoh Gesture

Gesture| Arti
👍| AKU
✋| MAU
🤏 (jempol + telunjuk)| MAKAN
☝️| NUNJUK

---

⚙️ Requirements

Install dulu:

pip install opencv-python mediapipe

Disarankan pakai:

- Python 3.10 / 3.11

---

▶️ Cara Menjalankan

Masuk ke folder project:

cd nama_folder_project

Jalankan:

py -3.11 gesture_advanced.py

atau:

py -3.11 gesture_translate.py

---

🎮 Cara Pakai

1. Nyalakan kamera
2. Arahkan tangan ke kamera
3. Lakukan gesture
4. Teks akan muncul di layar

---

⚠️ Tips

- Gunakan pencahayaan yang terang
- Jangan terlalu jauh dari kamera
- Tahan gesture ±1 detik agar terbaca stabil

---

📁 Struktur Project

gesture-project/
│
├── gesture.py
├── gesture_translate.py
├── gesture_advanced.py
└── README.md

---

🚀 Pengembangan Selanjutnya

- Gesture → kalimat otomatis
- Gesture → kontrol PC (volume, play, dll)
- Gesture → kontrol game
- Integrasi dengan Blender (3D object control)

---

📌 Catatan

Project ini masih menggunakan metode rule-based (belum AI training), jadi akurasi tergantung posisi tangan dan pencahayaan.

---

👤 Author

Dibuat untuk eksperimen Computer Vision menggunakan Python.
