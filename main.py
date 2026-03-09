import ctypes
import sys
from utils.paths import resource_path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase, QIcon

from ui.main_window import MainWindow
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("youtube.downloader.app")

app = QApplication(sys.argv)

QFontDatabase.addApplicationFont(resource_path("fonts/circular-std-medium.ttf"))

font = QFont("Circular Std Medium")
font.setPointSize(10)

icon = QIcon(resource_path("assets/icon.ico"))
app.setWindowIcon(icon)

window = MainWindow()
window.setWindowIcon(icon)
window.show()

sys.exit(app.exec())