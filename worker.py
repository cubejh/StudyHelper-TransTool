from PySide6.QtCore import QThread, Signal
from processfile import processfile
from utils.analyzefile import analyze_images
class Worker(QThread):
    finished_ok = Signal(str)
    error = Signal(str)

    def __init__(self, payload, tabmode):
        super().__init__()
        self.payload = payload
        self.tabmode = tabmode

    def run(self):
        try:
            if self.tabmode == 0 :
                processfile(self.payload,0)
                self.finished_ok.emit("")
            else :
                rt = processfile(self.payload,1)
                self.finished_ok.emit(rt)

        except Exception as e:
            print("error:", e)
            self.error.emit(str(e))