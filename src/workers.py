import time

from PyQt5.QtCore import QObject, pyqtSignal


class Timer(QObject):
    """Worker class that emits clock signal"""

    sgl_update_timer = pyqtSignal(int)
    sgl_start_cleanup = pyqtSignal()

    def __init__(self, increment: int = 1):
        super().__init__()

        self.increment = increment
        self.running = True
        self.time = 0

    def run(self):
        while self.running:
            time.sleep(self.increment)
            self.time += self.increment
            self.sgl_update_timer.emit(self.time)
        self.sgl_start_cleanup.emit()
