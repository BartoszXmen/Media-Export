import os

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from core.fetcher import FetchWorker
from core.downloader import DownloadWorker

from ui.panels.left_panel import LeftPanel
from ui.panels.center_panel import CenterPanel

from ui.utils.formatters import format_duration, format_date
from ui.utils.cache import cache_thumb
from ui.utils.image_tools import get_accent_color, make_rounded
from ui.utils.styles import build_styles

from ui.components.spinner import Spinner
from ui.workers.image_loader import ImageLoader

from ui.services.folder_manager import FolderManager


CACHE = os.path.join(os.getcwd(), "cache", "thumbs")

os.makedirs(CACHE, exist_ok=True)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.threadpool = QThreadPool.globalInstance()
        self.threadpool.setMaxThreadCount(8)

        self.setWindowTitle("Media Export")
        self.resize(850, 400)

        self.video = None
        self.folder = os.path.expanduser("~/Downloads")

        self.fetch_thread = None
        self.download_thread = None

        self.accent = "#8b5cf6"

        self.fetch_timer = QTimer()
        self.fetch_timer.setSingleShot(True)
        self.fetch_timer.timeout.connect(self.start_fetch)

        self.folder_manager = FolderManager()
        self.folder = self.folder_manager.get_folder()

        self.setAcceptDrops(True)

        self.build_ui()

        # auto clipboard detect
        QTimer.singleShot(0, self.detect_clipboard)

    # ---------------- UI

    def build_ui(self):

        container = QWidget()
        container.setObjectName("app")

        self.setCentralWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)

        # TOP

        top = QHBoxLayout()

        self.url = QLineEdit()
        self.url.setPlaceholderText("Paste URL")
        self.url.textChanged.connect(self.on_url_changed)

        paste = QPushButton("Paste")
        paste.clicked.connect(self.paste)

        top.addWidget(self.url)
        top.addWidget(paste)

        layout.addLayout(top)

        # MAIN

        main = QHBoxLayout()

        self.left_panel = LeftPanel()
        self.left_panel.format.currentTextChanged.connect(self.load_qualities)
        self.left_panel.download_btn.clicked.connect(self.download)

        self.left_panel.change_folder_clicked.connect(self.change_folder)
        self.left_panel.open_folder_clicked.connect(self.open_folder)

        self.left_panel.set_folder_path(
            self.folder_manager.shorten_path(self.folder)
        )

        main.addWidget(self.left_panel, 2)

        self.center_panel = CenterPanel()

        main.addWidget(self.center_panel, 4)

        layout.addLayout(main)

        # BOTTOM

        bottom = QHBoxLayout()

        self.version = QLabel("v1.0.0 BartizeR")
        self.status = QLabel("Ready")

        self.progress = QProgressBar()
        self.progress.hide()

        bottom.addWidget(self.version)
        bottom.addStretch()
        bottom.addWidget(self.progress)
        bottom.addWidget(self.status)

        layout.addLayout(bottom)

        self.spinner = Spinner(
            self.center_panel.spinner,
            self.center_panel.spinner_pixmap
        )

        self.setStyleSheet(build_styles(self.accent))

        self.reset_ui()

    def change_folder(self):

        folder = self.folder_manager.change_folder(self)

        self.folder = folder

        self.left_panel.set_folder_path(
            self.folder_manager.shorten_path(folder)
        )

    def open_folder(self):

        self.folder_manager.open_folder()

    # ---------------- CLIPBOARD

    def detect_clipboard(self):

        text = QApplication.clipboard().text()

        if "youtube.com" in text or "youtu.be" in text:
            self.url.setText(text)

    # ---------------- DRAG DROP

    def dragEnterEvent(self, event):

        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):

        text = event.mimeData().text()

        if "youtube.com" in text or "youtu.be" in text:
            self.url.setText(text)

    # ---------------- URL CHANGE

    def on_url_changed(self):

        text = self.url.text()

        if "http" not in text:
            self.reset_ui()
            return

        self.fetch_timer.start(400)

    # ---------------- RESET UI

    def reset_ui(self):

        self.video = None

        self.center_panel.title.setText("")
        self.center_panel.author.setText("")
        self.center_panel.thumb.clear()

        self.center_panel.avatar.clear()

        self.center_panel.duration.hide()
        self.center_panel.date.hide()

        self.center_panel.author_card.hide()
        self.center_panel.avatar.hide()
        self.center_panel.author.hide()

        self.left_panel.hide_controls()

        self.status.setText("Ready")

    # ---------------- FETCH

    def start_fetch(self):

        if self.fetch_thread:
            self.fetch_thread.quit()
            self.fetch_thread.deleteLater()
            self.fetch_thread = None

        self.reset_ui()

        self.center_panel.center_stack.setCurrentIndex(1)

        self.spinner.start()

        self.status.setText("Fetching video info...")

        self.fetch_thread = QThread()

        self.fetch_worker = FetchWorker(self.url.text())
        self.fetch_worker.moveToThread(self.fetch_thread)

        self.fetch_thread.started.connect(self.fetch_worker.run)

        self.fetch_worker.finished.connect(self.video_loaded)
        self.fetch_worker.error.connect(self.fetch_error)

        self.fetch_worker.finished.connect(self.cleanup_fetch)
        self.fetch_worker.error.connect(self.cleanup_fetch)

        self.fetch_thread.start()

    def cleanup_fetch(self):

        self.spinner.stop()

        if self.fetch_thread:
            self.fetch_thread.quit()
            self.fetch_thread.deleteLater()
            self.fetch_thread = None

    def fetch_error(self, msg):

        self.center_panel.center_stack.setCurrentIndex(0)

        self.status.setText("Failed to fetch video")

    # ---------------- VIDEO LOADED

    def video_loaded(self, data):

        self.video = data

        self.spinner.stop()

        # TITLE

        self.center_panel.set_title(data["title"])

        # AUTHOR

        self.center_panel.author.setText(data["author"])

        self.center_panel.author_card.show()
        self.center_panel.avatar.show()
        self.center_panel.author.show()

        # META

        dur = format_duration(data["duration"])
        date = format_date(data["upload_date"])

        self.center_panel.duration.setText(dur)
        self.center_panel.date.setText(date)

        self.center_panel.update_badge_positions()

        self.center_panel.duration.show()
        self.center_panel.date.show()

        # ASYNC IMAGES

        self.load_image(data["thumbnail"], "thumb")

        if data.get("channel_avatar"):
            self.load_image(data["channel_avatar"], "avatar")

        self.left_panel.show_controls()

        self.load_qualities()

        self.center_panel.center_stack.setCurrentIndex(0)

        self.status.setText("Video loaded")

    # ---------------- IMAGE LOADER

    def load_image(self, url, key):

        worker = ImageLoader(url, key)

        worker.signals.finished.connect(self.image_loaded)

        self.threadpool.start(worker)

    def image_loaded(self, key, pix):

        if pix.isNull():
            return

        if key == "thumb":

            self.center_panel.thumb.setPixmap(
                make_rounded(pix, 420, 236, 14)
            )

            accent = get_accent_color(cache_thumb(self.video["thumbnail"]))
            self.accent = accent
            self.setStyleSheet(build_styles(self.accent))
        elif key == "avatar":

            self.center_panel.avatar.setPixmap(
                make_rounded(pix, 110, 110, 55)
            )

    # ---------------- QUALITY

    def load_qualities(self):

        if not self.video:
            return

        self.left_panel.quality.clear()

        fmt = self.left_panel.format.currentText()

        if fmt == "MP4":

            qualities = {}

            for f in self.video["formats"]:

                h = f.get("height")

                if not h:
                    continue

                label = f"{h}p"
                qualities[h] = label

            self.left_panel.quality.addItem("Best")

            for h in sorted(qualities.keys(), reverse=True):
                self.left_panel.quality.addItem(qualities[h])

        else:

            bitrates = set()

            for f in self.video["formats"]:

                abr = f.get("abr")

                if abr:
                    bitrates.add(int(abr))

            self.left_panel.quality.addItem("Best")

            for b in sorted(bitrates, reverse=True):
                self.left_panel.quality.addItem(f"{b} kbps")

    # ---------------- DOWNLOAD

    def download(self):

        if not self.video:
            return

        if self.download_thread:
            return

        self.progress.setValue(0)
        self.progress.show()

        self.status.setText("Starting download...")

        self.download_thread = QThread()

        self.worker = DownloadWorker(
            self.url.text(),
            self.folder,
            self.left_panel.format.currentText(),
            self.left_panel.quality.currentText()
        )

        self.worker.moveToThread(self.download_thread)

        self.download_thread.started.connect(self.worker.run)

        self.worker.progress.connect(self.update_progress)

        self.worker.finished.connect(self.download_done)

        self.download_thread.start()

    def update_progress(self, p, _, __):

        self.progress.setValue(int(p))

        self.status.setText(f"Downloading... {int(p)}%")

    def download_done(self, _):

        self.progress.hide()
        self.progress.setValue(0)

        self.status.setText("Download completed")

        self.download_thread.quit()
        self.download_thread.wait()

        self.download_thread = None

    # ---------------- ACCENT

    def apply_accent(self, img):

        self.accent = get_accent_color(img)

        self.setStyleSheet(build_styles(self.accent))

    # ---------------- MISC

    def paste(self):

        self.url.setText(QApplication.clipboard().text())