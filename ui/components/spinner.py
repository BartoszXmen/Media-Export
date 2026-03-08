from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QTransform


class Spinner:

    def __init__(self, label, pixmap):

        self.label = label
        self.pixmap = pixmap

        self.angle = 0

        self.timer = QTimer()

        self.timer.timeout.connect(self.rotate)

    def start(self):

        self.timer.start(16)

    def stop(self):

        self.timer.stop()

    def rotate(self):

        self.angle += 5

        t = QTransform().rotate(self.angle)

        r = self.pixmap.transformed(t, Qt.SmoothTransformation)

        self.label.setPixmap(r)