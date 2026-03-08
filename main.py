import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase

from ui.main_window import MainWindow


app = QApplication(sys.argv)

QFontDatabase.addApplicationFont("fonts/circular-std-medium.ttf")

font = QFont("Circular Std Medium")
font.setPointSize(10)

app.setFont(font)

window = MainWindow()
window.show()

sys.exit(app.exec())