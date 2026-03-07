import sys
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtGui import QFont
from newgui import OCRTool

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    font = QFont("Arial", 12)
    font.setBold(True)
    app.setFont(font)
    window = OCRTool()
    window.show()
    sys.exit(app.exec())
