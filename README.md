🦖 Dinopedia

A modern desktop application to manage and explore dinosaur data with a clean Card UI, built using Python OOP + PySide6.

✨ Features:
  🧠 OOP Architecture (Clean Code)
  💾 Local JSON Database
  🦖 Add / Edit / Delete Dinosaur
  🔍 Real-time Search
  🖼️ Image Upload & Preview
  🧾 Description Support (Wikipedia-style)
  🎴 Card UI Layout (Modern Look)
  🌑 Dark Mode UI
  🪟 Popup Detail View (with animation)
  🔍 Click Image → Fullscreen Viewer
  🎨 Hover Effect (Shadow Glow)

📁 Project Structure
dinopedia/
│
├── data/
│   └── dinosaurs.json
│
├── models/
│   └── dinosaur.py
│
├── ui/
│   └── gui.py
│
├── utils/
│   └── database.py
│
└── main.py

🧠 How It Works
  🔹 Database
  Uses local JSON file (data/dinosaurs.json)
  Auto-created if not exists
  Managed via Database class
  🔹 Model
  Dinosaur class handles:
  name
  period
  diet
  image
  description
  🔹 UI
  Built with PySide6
  Uses:
  QGridLayout → Card system
  QScrollArea → Scrollable UI
  QDialog → Detail popup
  QGraphicsDropShadowEffect → Hover effect

🛠️ Future Improvements
  🌐 Auto Image Fetch (API)
  🧠 AI-generated description
  📊 Sorting & Filtering
  🧾 Export to PDF
  🗂️ Category system (Carnivore, Herbivore, etc.)
  🌍 Multi-language support
  ☁️ Cloud database (Firebase / Supabase)

👨‍💻 Author
Rafa Ramadhan
📌 Student Developer | Python Enthusiast

📜 License
This project is licensed under the MIT License.

⭐ Support
If you like this project:
  ⭐ Star this repo
  🍴 Fork it
  💡 Suggest new features
