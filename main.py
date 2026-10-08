import sys
from PyQt6.QtWidgets import QApplication
from src.ui import ScrpycpyApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrpycpyApp()
    window.show()
    sys.exit(app.exec())