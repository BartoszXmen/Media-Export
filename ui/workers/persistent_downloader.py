import subprocess
import queue
from PySide6.QtCore import QObject, Signal


class PersistentDownloader(QObject):

    progress = Signal(float)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, yt_path):
        super().__init__()

        self.yt_path = yt_path
        self.tasks = queue.Queue()
        self.running = True

    def add_task(self, url, output, format_string):

        self.tasks.put((url, output, format_string))

    def run(self):

        while self.running:

            url, output, format_string = self.tasks.get()

            try:

                cmd = [
                    self.yt_path,
                    "--no-playlist",
                    "-f",
                    format_string,
                    "-N",
                    "8",
                    "-o",
                    output,
                    url
                ]

                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                for line in process.stdout:

                    if "%" in line:

                        try:
                            percent = float(line.split("%")[0].split()[-1])
                            self.progress.emit(percent)
                        except:
                            pass

                process.wait()

                self.finished.emit(url)

            except Exception as e:

                self.error.emit(str(e))