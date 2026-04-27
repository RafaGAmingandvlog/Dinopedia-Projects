#The Gui (Pyside6) for dinopedia

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QMessageBox,
    QFileDialog, QScrollArea, QGridLayout, QDialog, QGraphicsDropShadowEffect
)

import os
import random
import requests
from PySide6.QtCore import QPropertyAnimation, QThread, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from utils.image_service import ImageService


from models.dinosaur import Dinosaur

# ======================
# THREAD FETCH IMAGE
# ======================
class ImageFetcher(QThread):
    finished = Signal(str)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        path = ImageService.fetch_dino_image(self.name)
        self.finished.emit(path if path else "")

# ======================
# AI SCIENCE ENGINE
# ======================
class DinoScience:
    @staticmethod
    def classify(name):
        n = name.lower()

        if any(x in n for x in ["rex", "raptor", "allosaurus", "carnotaurus"]):
            return "Theropoda (Carnivorous Bipedal Dinosaurs)"
        elif any(x in n for x in ["brachio", "diplodocus", "apatosaurus"]):
            return "Sauropoda (Long-neck Herbivores)"
        elif any(x in n for x in ["triceratops", "stegosaurus", "ankylosaurus"]):
            return "Ornithischia (Armored / Horned Dinosaurs)"
        else:
            return "Dinosauria (Uncertain Classification)"


    @staticmethod
    def estimate_size(name):
        n = name.lower()

        if "rex" in n:
            return "≈ 12–13 m length", "≈ 8–9 tons"
        elif "brachio" in n:
            return "≈ 25 m length", "≈ 50–60 tons"
        elif "velociraptor" in n:
            return "≈ 2 m length", "≈ 15 kg"
        else:
            return "Unknown (insufficient fossil data)", "Unknown"


    @staticmethod
    def natural_description(dino, fossils):
        base = f"{dino.name} lived during the {dino.period} period."

        if fossils:
            place = fossils[0].get("cc", "various regions")
            extra = f" Fossils have been discovered in {place}."
        else:
            extra = " Fossil evidence is limited."

        diet = ""
        if dino.diet:
            diet = f" It is generally considered a {dino.diet.lower()} species."

        return base + extra + diet

# ======================
# PALEOBIOLOGY API
# ======================
class FossilAPI:

    @staticmethod
    def get_fossil_data(name):
        try:
            url = f"https://paleobiodb.org/data1.2/occs/list.json?base_name={name}&limit=10"
            res = requests.get(url, timeout=5)

            if res.status_code != 200:
                return []

            data = res.json()
            return data.get("records", [])

        except:
            return []

# ======================
# MINI MAP
# ======================
class FossilMap(QWidget):
    def __init__(self, fossils):
        super().__init__()
        self.fossils = fossils
        self.setMinimumHeight(140)

    def paintEvent(self, event):
        from PySide6.QtGui import QPainter, QColor

        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#101820"))

        painter.setBrush(QColor("#00ffaa"))

        for f in self.fossils:
            try:
                x = int(float(f.get("lng", 0)) * 2) % self.width()
                y = int(float(f.get("lat", 0)) * 2) % self.height()
                painter.drawEllipse(x, y, 4, 4)
            except:
                pass

# ======================
# CARD COMPONENT
# ======================
class DinoCard(QWidget):
    def __init__(self, dino, db, refresh_callback):
        super().__init__()
        self.dino = dino
        self.db = db
        self.refresh = refresh_callback

        layout = QVBoxLayout()

        # 🖼️ IMAGE
        self.image_label = QLabel("Loading...")
        self.image_label.setStyleSheet("color: gray;")
        self.image_label.setFixedHeight(120)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.load_image()


        # 📄 INFO
        self.name_label = QLabel(f"🦖 {dino.name}")
        self.period_label = QLabel(f"⏳ {dino.period}")
        self.diet_label = QLabel(f"🍖 {dino.diet}")

        # 🔘 BUTTONS
        btn_layout = QHBoxLayout()

        self.edit_btn = QPushButton("✏️ Edit")
        self.edit_btn.clicked.connect(self.edit_dino)

        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.clicked.connect(self.delete_dino)

        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)

        # ADD TO LAYOUT
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.period_label)
        layout.addWidget(self.diet_label)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Shadow Effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)

        # Clickable
        self.image_label.mousePressEvent = self.open_image

        # 🎨 STYLE
        self.setStyleSheet("""
            QWidget {
                border-radius: 12px;
                background-color: #2b2b2b;
                padding: 10px;
            }
            QWidget:hover {
                background-color: #353535;
            }
        """)

        self.edit_btn.setStyleSheet("background: transparent;")
        self.delete_btn.setStyleSheet("background: transparent;")

        self.setCursor(Qt.PointingHandCursor)

        layout.setAlignment(Qt.AlignTop)
    # ======================
    # LOAD IMAGE (ASYNC)
    # ======================
    def load_image(self):
        if self.dino.image and os.path.exists(self.dino.image):
            self.set_image(self.dino.image)
        else:
            self.thread = ImageFetcher(self.dino.name)
            self.thread.finished.connect(self.set_image)
            self.thread.start()


    # ======================
    # SET IMAGE + AUTO CROP
    # ======================
    def set_image(self, path):
        if not path or not os.path.exists(path):
            self.image_label.setText("No Image")
            return

        pixmap = QPixmap(path)

        if pixmap.isNull():
            self.image_label.setText("Invalid Image")
            return

        # 🔥 AUTO CROP CENTER (biar rapi)
        w, h = pixmap.width(), pixmap.height()
        size = min(w, h)

        cropped = pixmap.copy(
            (w - size) // 2,
            (h - size) // 2,
            size,
            size
        )

        self.image_label.setPixmap(cropped.scaled(
            160, 120,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        ))

        # simpan hasil ke object
        self.dino.image = path


    def delete_dino(self):
        self.db.delete(self.dino.name)
        self.refresh()

    def edit_dino(self):
        QMessageBox.information(
            self,
            "Edit",
            "Gunakan form di atas untuk edit data."
        )
    def show_detail(self):
        dialog = DinoDetailDialog(self.dino)
        dialog.exec()

    def mousePressEvent(self, event):
        self.show_detail()
    
    def enterEvent(self, event):
        self.shadow.setBlurRadius(25)

    def leaveEvent(self, event):
        self.shadow.setBlurRadius(10)
    
    def open_image(self, event):
        if self.dino.image:
            viewer = ImageViewer(self.dino.image)
            viewer.exec()

# ======================
# MAIN GUI
# ======================
class DinopediaGUI(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

        self.setWindowTitle("🦖 Dinopedia Card UI")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # ======================
        # FORM INPUT
        # ======================
        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nama")

        self.period_input = QLineEdit()
        self.period_input.setPlaceholderText("Periode")

        self.diet_input = QLineEdit()
        self.diet_input.setPlaceholderText("Diet")

        self.image_path = ""

        self.image_btn = QPushButton("📷 Gambar")
        self.image_btn.clicked.connect(self.select_image)

        self.add_btn = QPushButton("➕ Tambah")
        self.add_btn.clicked.connect(self.add_dino)

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.period_input)
        form_layout.addWidget(self.diet_input)
        form_layout.addWidget(self.image_btn)
        form_layout.addWidget(self.add_btn)

        main_layout.addLayout(form_layout)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Deskripsi singkat...")
        self.desc_input.clear()

        form_layout.addWidget(self.desc_input)

        # ======================
        # SEARCH
        # ======================
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search...")
        self.search_input.textChanged.connect(self.search_dino)

        main_layout.addWidget(self.search_input)

        # ======================
        # CARD AREA
        # ======================
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.grid = QGridLayout()

        self.container.setLayout(self.grid)
        self.scroll.setWidget(self.container)

        main_layout.addWidget(self.scroll)

        self.setLayout(main_layout)

        self.load_data()

    # ======================
    # LOAD DATA
    # ======================
    def load_data(self):
        self.clear_grid()

        data = self.db.get_all()

        row, col = 0, 0

        for d in data:
            card = DinoCard(d, self.db, self.load_data)
            self.grid.addWidget(card, row, col)

            col += 1
            if col == 3:
                col = 0
                row += 1

    # ======================
    # SEARCH
    # ======================
    def search_dino(self):
        keyword = self.search_input.text()
        data = self.db.search(keyword)

        self.clear_grid()

        row, col = 0, 0

        for d in data:
            card = DinoCard(d, self.db, self.load_data)
            self.grid.addWidget(card, row, col)

            col += 1
            if col == 3:
                col = 0
                row += 1

    # ======================
    # ADD
    # ======================
    def add_dino(self):
        name = self.name_input.text()
        period = self.period_input.text()
        diet = self.diet_input.text()
        description = self.desc_input.text()

        if not name:
            QMessageBox.warning(self, "Error", "Nama wajib diisi")
            return

        image_path = self.image_path

        # 🔥 AUTO IMAGE kalau user tidak pilih manual
        if not image_path:
            image_path = ImageService.fetch_dino_image(name)

        dino = Dinosaur(name, period, diet, image_path, description)
        self.db.add(dino)
        # reset form
        self.name_input.clear()
        self.period_input.clear()
        self.diet_input.clear()
        self.desc_input.clear()
        self.image_path = ""

        self.load_data()
        
    # ======================
    # IMAGE SELECT
    # ======================
    def select_image(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih Gambar",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )
        if file:
            self.image_path = file

    # ======================
    # CLEAR GRID
    # ======================
    def clear_grid(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

# ========
# POP-UP Details
# ========
class DinoDetailDialog(QDialog):
     def __init__(self, dino):
        super().__init__()

        self.setWindowTitle("🦖 Dinosaur Detail")
        self.setFixedSize(450, 620)

        layout = QVBoxLayout()

        # 📡 DATA
        fossils = FossilAPI.get_fossil_data(dino.name)
        classification = DinoScience.classify(dino.name)
        size, weight = DinoScience.estimate_size(dino.name)
        description = DinoScience.natural_description(dino, fossils)

        # 🖼️ IMAGE
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)

        if dino.image:
            pixmap = QPixmap(dino.image).scaled(
                320, 220,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("No Image")

        # 🧾 TITLE
        name_label = QLabel(dino.name)
        name_label.setStyleSheet("font-size:20px; font-weight:bold;")

        class_label = QLabel(f"🧬 {classification}")
        class_label.setStyleSheet("color: #00ffaa;")

        # 📊 SCIENTIFIC DATA
        stats_label = QLabel(f"""
📏 Estimated Size: {size}
⚖ Estimated Weight: {weight}
⏳ Period: {dino.period}
🍖 Diet: {dino.diet}
🦴 Fossil Records: {len(fossils)}
""")
        stats_label.setStyleSheet("font-family: monospace;")

        # 🧠 DESCRIPTION
        desc_label = QLabel(f"📖 {description}")
        desc_label.setWordWrap(True)

        # 🌍 MAP
        map_widget = FossilMap(fossils)

        # ADD
        layout.addWidget(image_label)
        layout.addWidget(name_label)
        layout.addWidget(class_label)
        layout.addWidget(stats_label)
        layout.addWidget(desc_label)
        layout.addWidget(map_widget)

        self.setLayout(layout)

        # 🎨 CLEAN SCIENTIFIC STYLE
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: white;
                border-radius: 12px;
            }
        """)

class ImageViewer(QDialog):
    def __init__(self, image_path):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.showFullScreen()

        layout = QVBoxLayout()

        label = QLabel()
        label.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            label.setText("Image not found")
        else:
            label.setPixmap(pixmap.scaled(
                self.width(),
                self.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

        layout.addWidget(label)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.close()