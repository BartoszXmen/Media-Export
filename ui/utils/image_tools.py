from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen
from PySide6.QtCore import Qt
from PIL import Image, ImageStat
import colorsys
import re


# ---------------- ACCENT COLOR


def get_accent_color(image_path):

    img = Image.open(image_path)
    img = img.resize((80, 80))

    stat = ImageStat.Stat(img)

    r, g, b = stat.mean[:3]

    r /= 255
    g /= 255
    b /= 255

    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    s = min(1, s * 1.4)
    v = min(1, v * 1.2)

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return f"rgb({r},{g},{b})"


# ---------------- COLOR PARSER


def parse_color(color):

    if isinstance(color, QColor):
        return color

    if isinstance(color, str) and color.startswith("rgb"):

        nums = re.findall(r"\d+", color)

        if len(nums) >= 3:
            return QColor(int(nums[0]), int(nums[1]), int(nums[2]))

    return QColor(color)


# ---------------- ROUNDED + GLOW


def make_rounded(pixmap: QPixmap, width: int, height: int, radius: int, glow_color=None):

    if pixmap.isNull():
        return QPixmap()

    scaled = pixmap.scaled(
        width,
        height,
        Qt.KeepAspectRatioByExpanding,
        Qt.SmoothTransformation
    )

    x = (scaled.width() - width) // 2
    y = (scaled.height() - height) // 2

    cropped = scaled.copy(x, y, width, height)

    result = QPixmap(width, height)
    result.fill(Qt.transparent)

    painter = QPainter(result)
    painter.setRenderHint(QPainter.Antialiasing)

    # ---------------- glow INSIDE

    if glow_color:

        glow = parse_color(glow_color)

        for i in range(12):

            c = QColor(glow)
            c.setAlpha(12 - i)

            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(c, 3))

            painter.drawRoundedRect(
                i,
                i,
                width - i * 2,
                height - i * 2,
                radius,
                radius
            )

    # ---------------- image

    path = QPainterPath()
    path.addRoundedRect(0, 0, width, height, radius, radius)

    painter.setClipPath(path)
    painter.drawPixmap(0, 0, cropped)

    painter.end()

    return result