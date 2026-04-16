from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTabWidget, QMessageBox, QApplication
)
import os
from getenv import set_api_key
from worker import Worker
from gui_logger import EmittingStream
import sys

from newgui.ai_tab import AITab
from newgui.format_tab import FormatTab


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("題目輔助工具")
        self.resize(1400, 800)

        main_layout = QVBoxLayout()  

        # ===== API  =====
        api_layout = QHBoxLayout()
        self.api_input = QLineEdit(os.getenv("API_KEY", ""))
        save_btn = QPushButton("儲存 API KEY")
        save_btn.clicked.connect(self.save_api)

        api_layout.addWidget(QLabel("API Key:"))
        api_layout.addWidget(self.api_input)
        api_layout.addWidget(save_btn)

        # ===== Tabs =====
        self.tabs = QTabWidget()
        self.ai_tab = AITab()
        self.format_tab = FormatTab()

        self.tabs.addTab(self.ai_tab, "AI解析")
        self.tabs.addTab(self.format_tab, "格式修正")

        # ===== button =====
        btn_layout = QHBoxLayout()

        self.run_btn = QPushButton("執行")
        self.run_btn.clicked.connect(self.run_task)

        self.exit_btn = QPushButton("離開")
        self.exit_btn.clicked.connect(QApplication.quit)  # 或 self.close

        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.exit_btn)

        # ===== combine =====
        main_layout.addLayout(api_layout)
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(btn_layout)  

        self.setLayout(main_layout)

    # ===== function =====
    def save_api(self):
        set_api_key(self.api_input.text().strip())
        QMessageBox.information(self, "Saved", "成功儲存API_KEY")

    def run_task(self):
        api_key = self.api_input.text().strip()

        if not api_key:
            QMessageBox.warning(self, "Error", "目前沒有 API Key")
            return

        # stdout redirect
        sys.stdout = EmittingStream(text_written=self.ai_tab.append_log)
        sys.stderr = EmittingStream(text_written=self.ai_tab.append_log)

        self.run_btn.setEnabled(False)

        # ===== AI TAB =====
        if self.tabs.currentIndex() == 0:
            payload = self.ai_tab.get_payload_data()
            payload["api_key"] = api_key

            self.worker = Worker(payload)

            self.worker.finished_ok.connect(self.task_finished)
            self.worker.error.connect(self.task_error) 

            self.worker.start()

        # ===== FORMAT TAB =====
        elif self.tabs.currentIndex() == 1:
            payload = self.format_tab.get_payload_data()
            payload["api_key"] = api_key

            try:
                print("Format Payload:", payload)
                QMessageBox.information(self, "Done", "Format completed")
            except Exception as e:
                self.task_error(str(e))

            self.run_btn.setEnabled(True)
    
    def task_finished(self):
        opf = self.worker.payload.get("output_folder")
        QMessageBox.information(self, "Done", "Completed")
        self.run_btn.setEnabled(True)
        self.open_folder(opf)

    def task_error(self, e):
        QMessageBox.critical(self, "Error", str(e))
        self.run_btn.setEnabled(True)    

    def open_folder(self, path):
        if not path:
            return
        os.startfile(path)