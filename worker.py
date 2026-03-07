from PySide6.QtCore import QThread
from processfile import processfile

class Worker(QThread):
    def __init__(self, payload):
        super().__init__()
        self.payload = payload

    def run(self):
        processfile(self.payload)