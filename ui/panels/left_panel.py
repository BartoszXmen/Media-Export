from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from utils.paths import resource_path


class LeftPanel(QWidget):

    change_folder_clicked = Signal()
    open_folder_clicked = Signal()

    def __init__(self):

        super().__init__()

        panel = QWidget()
        panel.setObjectName("panel")

        box = QVBoxLayout(panel)

        # -------- FORMAT

        self.format_label = QLabel("Format")

        self.format = QComboBox()
        self.format.addItems(["MP4", "MP3", "WAV"])

        self.quality_label = QLabel("Quality")

        self.quality = QComboBox()

        self.download_btn = QPushButton("Download")

        for w in [
            self.format_label,
            self.format,
            self.quality_label,
            self.quality,
            self.download_btn
        ]:
            w.hide()

        box.addWidget(self.format_label)
        box.addWidget(self.format)

        box.addWidget(self.quality_label)
        box.addWidget(self.quality)

        box.addSpacing(20)

        box.addWidget(self.download_btn)

        box.addStretch()

        # ---------- FOLDER SECTION

        folder_layout = QVBoxLayout()
        folder_layout.setSpacing(8)

        font = QFont()
        font.setPointSize(11)

        # -------- CHANGE FOLDER

        change_row = QHBoxLayout()
        change_row.setAlignment(Qt.AlignVCenter)

        change_text = QLabel("Change folder")
        change_text.setFont(font)
        change_text.setAlignment(Qt.AlignVCenter)

        change_btn = QPushButton()
        change_btn.setObjectName("folderBtn")
        change_btn.setIcon(QIcon(resource_path("assets/change_folder.png")))
        change_btn.setFixedSize(56, 28)

        change_btn.clicked.connect(self.change_folder_clicked.emit)

        change_row.addWidget(change_text)
        change_row.addStretch()
        change_row.addWidget(change_btn)

        # -------- OPEN FOLDER

        open_row = QHBoxLayout()
        open_row.setAlignment(Qt.AlignVCenter)

        open_text = QLabel("Open folder")
        open_text.setFont(font)
        open_text.setAlignment(Qt.AlignVCenter)

        open_btn = QPushButton()
        open_btn.setObjectName("folderBtn")
        open_btn.setIcon(QIcon(resource_path("assets/open_folder.png")))
        open_btn.setFixedSize(56, 28)

        open_btn.clicked.connect(self.open_folder_clicked.emit)

        open_row.addWidget(open_text)
        open_row.addStretch()
        open_row.addWidget(open_btn)

        # -------- PATH

        self.folder_path = QLabel("")
        self.folder_path.setWordWrap(False)
        self.folder_path.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.folder_path.setStyleSheet("color:#888;font-size:11px;")

        folder_layout.addLayout(change_row)
        folder_layout.addLayout(open_row)
        folder_layout.addWidget(self.folder_path)

        box.addLayout(folder_layout)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(panel)

        self.setMaximumWidth(200)
        self.setMinimumWidth(200)

    def set_folder_path(self, path):

        fm = self.folder_path.fontMetrics()

        elided = fm.elidedText(
            path,
            Qt.ElideMiddle,
            220
        )

        self.folder_path.setText(elided)

    def show_controls(self):

        for w in [
            self.format_label,
            self.format,
            self.quality_label,
            self.quality,
            self.download_btn
        ]:
            w.show()

    def hide_controls(self):

        for w in [
            self.format_label,
            self.format,
            self.quality_label,
            self.quality,
            self.download_btn
        ]:
            w.hide()