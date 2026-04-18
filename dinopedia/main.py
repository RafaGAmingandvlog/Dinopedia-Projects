# The Main Program for Dinopedia
from PySide6.QtWidgets import QApplication
import sys

from utils.database import Database
from ui.gui import DinopediaGUI

def main():
    app = QApplication(sys.argv)

    db = Database()
    window = DinopediaGUI(db)  
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
