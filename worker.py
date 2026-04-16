from PySide6.QtCore import QThread, Signal
from processfile import processfile

class Worker(QThread):
    finished_ok = Signal()
    error = Signal(str)

    def __init__(self, payload):
        super().__init__()
        self.payload = payload

    def run(self):
        try:
            processfile(self.payload)

            self.finished_ok.emit()

        except Exception as e:
            print("error:", e)
            self.error.emit(str(e))