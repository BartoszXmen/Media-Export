import subprocess
import json
from urllib.parse import urlparse, parse_qs
from PySide6.QtCore import QObject, Signal
from utils.paths import resource_path

CREATE_NO_WINDOW = 0x08000000


class FetchWorker(QObject):

    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = self.clean_url(url)

    # ---------------- CLEAN URL

    def clean_url(self, url):

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

            yt = resource_path("bin/yt-dlp.exe")

            cmd = [
                yt,
                "--dump-single-json",
                "--no-playlist",
                "--no-warnings",
                "--skip-download",
                "--no-call-home",
                "--no-check-certificates",
                self.url
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                creationflags=CREATE_NO_WINDOW
            )

            if result.returncode != 0:
                raise Exception("Invalid URL")

            data = json.loads(result.stdout)

            # avatar kanału
            avatar = None

            if data.get("channel_thumbnail"):
                avatar = data["channel_thumbnail"]

            else:
                thumbs = data.get("thumbnails")
                if thumbs:
                    avatar = thumbs[-1].get("url")

            info = {

                "title": data.get("title", ""),

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