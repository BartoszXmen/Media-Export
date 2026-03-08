import subprocess
from pathlib import Path
from PySide6.QtCore import QObject, Signal


BASE_DIR = Path(__file__).resolve().parent.parent
BIN_DIR = BASE_DIR / "bin"


class DownloadWorker(QObject):

    progress = Signal(float, str, str)
    status = Signal(str)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url, folder, fmt, quality):
        super().__init__()

        self.url = url
        self.folder = folder
        self.fmt = fmt
        self.quality = quality

    def run(self):

        try:

            yt = str(BIN_DIR / "yt-dlp.exe")

            output = f"{self.folder}/%(title)s.%(ext)s"

            if self.fmt == "MP4":

                if self.quality == "Best":

                    format_string = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"

                else:

                    h = self.quality.replace("p", "")

                    format_string = f"bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/best"

                cmd = [
                    yt,
                    "-f",
                    format_string,
                    "--merge-output-format",
                    "mp4",
                    "-o",
                    output,
                    self.url
                ]

            elif self.fmt == "MP3":

                cmd = [
                    yt,
                    "-f",
                    "bestaudio",
                    "--extract-audio",
                    "--audio-format",
                    "mp3",
                    "-o",
                    output,
                    self.url
                ]

            else:

                cmd = [
                    yt,
                    "-f",
                    "bestaudio",
                    "--extract-audio",
                    "--audio-format",
                    "wav",
                    "-o",
                    output,
                    self.url
                ]

            self.status.emit("Starting download...")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:

                if "%" in line and "ETA" in line:

                    try:

                        percent = float(line.split("%")[0].split()[-1])

                        self.progress.emit(percent, "", "")

                    except:
                        pass

                if "Merging formats" in line:
                    self.status.emit("Merging streams...")

            process.wait()

            self.finished.emit("done")

        except Exception as e:

            self.error.emit(str(e))