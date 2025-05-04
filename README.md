# AC&ECC - Automatic Coupling & Electrical Connection Control

## 🇮🇩 Bahasa Indonesia

**AC&ECC** adalah perangkat lunak kontrol **penyambungan otomatis dan pengaktifan kelistrikan** untuk rangkaian KRL yang memungkinkan dua unit EMU dari lokasi berbeda **bertemu di stasiun tertentu dan terhubung tanpa campur tangan manusia**. Proses ini berjalan **real-time** dan sepenuhnya otomatis.

### 🔧 Fitur Utama
- Mengatur **jadwal coupling otomatis** berdasarkan data lokal atau server (API).
- Deteksi posisi via GPS atau server lokasi.
- **Penyambungan fisik (coupling)** dilakukan otomatis jika dua EMU sudah berada dalam jarak dekat.
- **Kelistrikan antar rangkaian diaktifkan otomatis** setelah coupling sukses.
- Kompatibel dan **tidak mengganggu sistem TIMS** (Train Integrated Management System).
- Mendukung integrasi dengan sistem **ATC (Automatic Train Controller)** dan **ATO (Automatic Train Operation)**.
- **Implementasi saat ini hanya untuk Multiple Unit (MU).**

### 📌 Catatan Pengembangan
- Sistem ini **bersifat eksperimental** dan **masih dalam tahap alpha**.
- Saya **tidak berniat mematenkan sistem ini**, dan membukanya untuk kontribusi komunitas.
- Jika Anda berkenan membantu mengembangkan proyek ini, **silakan hubungi saya melalui email: raafidbenz@gmail.com**.

---

## 🇯🇵 日本語

**AC&ECC（自動連結および電力接続制御）**は、異なる場所にあるEMU（電車）が指定された駅で**自動的に連結および電気接続を行うリアルタイム制御システム**です。すべては人の介入なしに行われます。

### 🔧 主な機能
- ローカルまたはAPIスケジュールに基づく**自動連結スケジューリング**。
- GPSまたはサーバーからの位置情報の取得。
- 近接検出により**自動連結をトリガー**。
- 連結成功後に**自動で電気接続を開始**。
- **TIMS（列車統合管理システム）との互換性あり**。
- **ATC（自動列車制御）およびATO（自動列車運転）との統合をサポート**。
- **現在の実装はMultiple Unit（MU）専用です。**

### 📌 開発メモ
- このシステムは**実験的であり、アルファ段階にあります**。
- 私はこのシステムを**特許化するつもりはありません**。
- 開発協力に興味がある方は、ぜひご連絡ください。
  **メール: raafidbenz@gmail.com**

---

## 🇬🇧 English

**AC&ECC (Automatic Coupling & Electrical Connection Control)** is a software system that enables two EMU units from different locations to **automatically couple and connect their electrical systems at a designated station in real-time**, without human intervention.

### 🔧 Key Features
- Automated coupling scheduling based on local JSON or remote API.
- Position detection via GPS or server-based location.
- Initiates **automatic coupling** when both units are nearby.
- **Electrical connection is activated automatically** post-coupling.
- **Fully compatible with TIMS (Train Integrated Management System)**.
- Supports integration with **ATC (Automatic Train Controller)** and **ATO (Automatic Train Operation)** systems.
- **Current implementation is only for Multiple Unit (MU) types.**

### 📌 Development Notes
- This system is **experimental and currently in alpha stage**.
- I have **no intention of patenting this system**.
- If you'd like to help develop this further, please contact me.
  **Email: raafidbenz@gmail.com**
