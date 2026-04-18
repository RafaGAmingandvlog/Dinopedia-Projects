#The Gui (Pyside6) for dinopedia

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QMessageBox,
    QFileDialog, QScrollArea, QGridLayout, QDialog, QGraphicsDropShadowEffect
)

import requests
from PySide6.QtCore import QPropertyAnimation, QThread, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


from models.dinosaur import Dinosaur


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
        self.image_label = QLabel()
        self.image_label.setFixedHeight(120)
        self.image_label.setAlignment(Qt.AlignCenter)

        if dino.image:
            pixmap = QPixmap(dino.image).scaled(
                160, 120,
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("No Image")
    

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

        dino = Dinosaur(name, period, diet, self.image_path, description)
        self.db.add(dino)

        self.name_input.clear()
        self.period_input.clear()
        self.diet_input.clear()
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

        self.setWindowTitle("🦖 Detail Dinosaur")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        # 🖼️ IMAGE BESAR
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)

        if dino.image:
            pixmap = QPixmap(dino.image).scaled(
                300, 250,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("No Image")

        # 📄 INFO
        name_label = QLabel(f"🦖 {dino.name}")
        name_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        period_label = QLabel(f"⏳ Periode: {dino.period}")
        diet_label = QLabel(f"🍖 Diet: {dino.diet}")

        # STYLE
        period_label.setStyleSheet("color: gray;")
        diet_label.setStyleSheet("color: gray;")

        # ADD
        layout.addWidget(image_label)
        layout.addWidget(name_label)
        layout.addWidget(period_label)
        layout.addWidget(diet_label)

        # Fade-in animation
        self.setWindowOpacity(0)

        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

        self.setLayout(layout)

        # 🎨 STYLE
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
        """)

        desc_label = QLabel(f"📖 {dino.description}")
        desc_label.setWordWrap(True)

        layout.addWidget(desc_label)

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