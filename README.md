# 🦖 Dinopedia

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)
![PRs](https://img.shields.io/badge/PRs-Welcome-orange.svg)

Dinopedia adalah aplikasi desktop berbasis **PySide6 (Qt)** yang menampilkan koleksi dinosaurus dalam bentuk **interactive card UI** dengan data ilmiah nyata.

Project ini menggabungkan:

* 🎴 UI modern seperti kartu game
* 📡 Data ilmiah nyata (Paleobiology Database & Wikidata)
* 🧠 Deskripsi otomatis (AI / rule-based)
* 🌍 Visualisasi habitat & fossil discovery

---

## ✨ Features

### 🎴 Card-Based UI

* Tampilan dinosaurus seperti kartu koleksi
* Hover animation + shadow effect
* Klik kartu → buka detail lengkap

### 📡 Real Scientific Data

* Integrasi dengan:

  * Paleobiology Database (PBDB)
  * Wikidata
* Data mencakup:

  * Periode hidup
  * Diet
  * Lokasi fossil ditemukan
  * Jumlah record fossil

### 🧬 Taxonomy Lengkap

Menampilkan klasifikasi:

* Kingdom → Species
* Contoh:

  * Animalia
  * Chordata
  * Reptilia
  * Dinosauria
  * Theropoda / Sauropoda / Ornithischia

### 🌍 Habitat & Fossil Map

* Data lokasi fossil real (latitude & longitude)
* Siap dikembangkan ke visual map dunia

### 🖼️ Auto Image System

* Ambil gambar otomatis dari internet
* Cache ke local storage
* Auto crop & resize (card ratio)

### ⚡ Async Loading

* Image fetch tidak membuat UI freeze
* Menggunakan QThread

### 🧠 AI Description (Optional)

* Generate deskripsi dinosaurus
* Bisa:

  * Rule-based (default)
  * Offline AI (GGUF / ONNX) [opsional]

---

## 🏗️ Project Structure

```
dinopedia/
│
├── main.py
├── dinopedia.json
│
├── models/
│   └── dinosaur.py
│
├── ui/
│   └── gui.py
│
├── utils/
│   ├── database.py
│   └── image_service.py
│
└── data/
    └── images/
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/RafaGAmingandvlog/Dinopedia-Projects.git
cd Dinopedia-Projects
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
python main.py
```

---

## 🧪 Example Dinosaurs

* Tyrannosaurus Rex
* Velociraptor
* Triceratops
* Spinosaurus
* Brachiosaurus

---

## 🧠 AI (Optional Setup)

Jika ingin menggunakan AI offline:

### Install:

```bash
pip install ctransformers
```

### Model:

* Gunakan model `.gguf` ringan (1B–3B)
* Simpan di folder:

```
models/ai/
```

---

## 📡 Data Sources

* Paleobiology Database (PBDB)
* Wikidata
* Wikipedia (image fallback)

---

## 🚀 Roadmap

* [ ] 🌍 Real world map visualization
* [ ] 🧠 Full offline AI integration (GGUF)
* [ ] 📊 Statistik ilmiah lebih detail
* [ ] 🧬 Evolution & lineage tree
* [ ] 🎮 Gamification system

---

## ⚠️ Notes

* Python yang direkomendasikan:
  👉 **3.10 / 3.11 (lebih stabil)**
* Python 3.13 masih bleeding edge (beberapa library belum support)

---

## 👨‍💻 Author

Rafa Ramadhan
GitHub: https://github.com/RafaGAmingandvlog

---

## 📜 License

MIT License

---

## ⭐ Support

Jika kamu suka project ini:

* ⭐ Star repo ini
* 🍴 Fork dan kembangkan
* 💡 Berikan ide fitur baru

