from PySide6.QtCore import QRunnable, QObject, Signal
from PySide6.QtGui import QPixmap

from ui.utils.cache import cache_thumb


class ImageSignals(QObject):

    finished = Signal(str, QPixmap)


class ImageLoader(QRunnable):

    def __init__(self, url, key):
        super().__init__()

        self.url = url
        self.key = key

        self.signals = ImageSignals()

    def run(self):

        try:

            path = cache_thumb(self.url)

            pix = QPixmap(path)

            self.signals.finished.emit(self.key, pix)

        except:
            pass