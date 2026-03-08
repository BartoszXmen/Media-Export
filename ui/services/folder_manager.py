from PySide6.QtCore import QSettings, QUrl
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QDesktopServices
import os


class FolderManager:

    def __init__(self):

        self.settings = QSettings("Media Export", "Media Export")

        self.folder = self.settings.value(
            "download_folder",
            os.path.expanduser("~/Downloads")
        )

    def get_folder(self):

        return self.folder

    def change_folder(self, parent=None):

        folder = QFileDialog.getExistingDirectory(
            parent,
            "Choose download folder",
            self.folder
        )

        if folder:

            self.folder = folder
            self.settings.setValue("download_folder", folder)

        return self.folder

    def open_folder(self):

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(self.folder)
        )

    # UX: skrócona ścieżka
    def shorten_path(self, path, max_len=40):

        if len(path) <= max_len:
            return path

        parts = path.split(os.sep)

        if len(parts) <= 2:
            return path

        return "..." + os.sep + os.sep.join(parts[-2:])