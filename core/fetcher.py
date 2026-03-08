import subprocess
import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from PySide6.QtCore import QObject, Signal


BASE_DIR = Path(__file__).resolve().parent.parent
BIN_DIR = BASE_DIR / "bin"


class FetchWorker(QObject):

    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = self.clean_url(url)

    # ---------------- CLEAN URL

    def clean_url(self, url):

        # youtube watch link
        if "youtube.com/watch" in url:

            parsed = urlparse(url)
            query = parse_qs(parsed.query)

            vid = query.get("v")

            if vid:
                return f"https://youtu.be/{vid[0]}"

        return url

    # ---------------- RUN

    def run(self):

        try:

            yt = str(BIN_DIR / "yt-dlp.exe")

            # FAST FETCH

            cmd = [
                yt,
                "--dump-json",
                "--no-playlist",
                "--no-warnings",
                "--skip-download",
                self.url
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise Exception("Invalid URL")

            data = json.loads(result.stdout)

            # ---------------- AVATAR

            avatar = data.get("channel_thumbnail")

            if not avatar:

                uploader_url = data.get("uploader_url")

                if uploader_url:

                    cmd_channel = [
                        yt,
                        "--dump-single-json",
                        "--skip-download",
                        "--playlist-items",
                        "0",
                        uploader_url
                    ]

                    ch = subprocess.run(
                        cmd_channel,
                        capture_output=True,
                        text=True
                    )

                    if ch.returncode == 0:

                        ch_data = json.loads(ch.stdout)

                        thumbs = ch_data.get("thumbnails")

                        if thumbs:
                            avatar = thumbs[-1].get("url")

            # ---------------- RESULT

            info = {

                "title": data["title"],

                "author": data.get("uploader", ""),

                "duration": data.get("duration", 0),

                "upload_date": data.get("upload_date", ""),

                "thumbnail": data.get("thumbnail"),

                "channel_avatar": avatar,

                "formats": data.get("formats", [])
            }

            self.finished.emit(info)

        except Exception as e:

            self.error.emit(str(e))