from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class CenterPanel(QWidget):

    def __init__(self):
        super().__init__()

        panel = QWidget()
        panel.setObjectName("panel")

        stack = QStackedLayout(panel)

        # ---------------- INFO

        info = QWidget()

        layout = QVBoxLayout(info)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 0)

        # ---------------- TITLE

        self.title = QLabel("")
        self.title.setObjectName("title")
        self.title.setWordWrap(False)
        self.title.setMaximumWidth(620)

        font = self.title.font()
        font.setPointSize(14)
        font.setBold(True)
        self.title.setFont(font)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 200))

        self.title.setGraphicsEffect(shadow)

        self.title_full = ""
        self.title_expanded = False

        self.title.mousePressEvent = self.toggle_title

        layout.addWidget(self.title)

        # ---------------- ROW

        row = QHBoxLayout()
        row.setSpacing(18)

        # ---------------- THUMBNAIL

        thumb_container = QWidget()
        thumb_container.setFixedSize(420, 236)

        self.thumb = QLabel(thumb_container)
        self.thumb.setGeometry(0, 0, 420, 236)
        self.thumb.setScaledContents(True)

        # duration badge

        self.duration = QLabel(thumb_container)
        self.duration.setStyleSheet("""
        background:rgba(0,0,0,150);
        padding:4px 8px;
        border-radius:6px;
        font-size:11px;
        """)

        # date badge

        self.date = QLabel(thumb_container)
        self.date.setStyleSheet("""
        background:rgba(0,0,0,150);
        padding:4px 8px;
        border-radius:6px;
        font-size:11px;
        """)

        row.addWidget(thumb_container)

        # ---------------- AUTHOR CARD

        self.author_card = QWidget()
        self.author_card.setObjectName("authorCard")
        self.author_card.setFixedWidth(190)

        author_layout = QVBoxLayout(self.author_card)
        author_layout.setSpacing(6)
        author_layout.setContentsMargins(16, 16, 16, 16)
        author_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.avatar = QLabel()
        self.avatar.setFixedSize(110, 110)
        self.avatar.setAlignment(Qt.AlignCenter)

        self.author = QLabel("")
        self.author.setObjectName("author")
        self.author.setAlignment(Qt.AlignCenter)

        font = self.author.font()
        font.setPointSize(11)
        font.setBold(True)
        self.author.setFont(font)

        author_layout.addWidget(self.avatar)
        author_layout.addWidget(self.author)

        row.addWidget(self.author_card)
        row.addStretch()

        layout.addLayout(row)
        layout.addStretch()

        # ---------------- LOADING

        loading = QWidget()

        lv = QVBoxLayout(loading)
        lv.addStretch()

        self.spinner = QLabel()

        pix = QPixmap("assets/loading_circle.png")

        pix = pix.scaled(
            int(pix.width() * 0.35),
            int(pix.height() * 0.35),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.spinner_pixmap = pix

        self.spinner.setPixmap(pix)
        self.spinner.setAlignment(Qt.AlignCenter)

        lv.addWidget(self.spinner)
        lv.addStretch()

        stack.addWidget(info)
        stack.addWidget(loading)

        self.center_stack = stack

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(panel)

        # hidden before fetch

        self.author_card.hide()
        self.avatar.hide()
        self.author.hide()
        self.duration.hide()
        self.date.hide()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # ---------------- BADGE POSITION

    def update_badge_positions(self):

        padding = 10
        thumb_w = 420
        thumb_h = 236

        self.duration.adjustSize()
        self.date.adjustSize()

        # prawa dolna
        self.duration.move(
            thumb_w - self.duration.width() - padding,
            thumb_h - self.duration.height() - padding
        )

        # lewa dolna
        self.date.move(
            padding,
            thumb_h - self.date.height() - padding
        )

    # ---------------- TITLE

    def set_title(self, text):

        self.title_full = text

        fm = self.title.fontMetrics()

        elided = fm.elidedText(
            text,
            Qt.ElideRight,
            600
        )

        self.title.setText(elided)

    def toggle_title(self, event):

        if not self.title_full:
            return

        if self.title_expanded:

            fm = self.title.fontMetrics()

            elided = fm.elidedText(
                self.title_full,
                Qt.ElideRight,
                600
            )

            self.title.setWordWrap(False)
            self.title.setText(elided)

            self.title_expanded = False

        else:

            self.title.setWordWrap(True)
            self.title.setText(self.title_full)

            self.title_expanded = True

    def set_blur_pixmap(self, path):
        pass