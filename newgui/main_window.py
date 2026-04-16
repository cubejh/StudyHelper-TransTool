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
from newgui.scai_tab import ScreenshotAITab
from newgui.intro_tab import Intro_Tab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("轉換工具v4")
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
        self.scai_tab = ScreenshotAITab()
        self.intro_tab = Intro_Tab()

        self.tabs.addTab(self.ai_tab, "文件分析")
        self.tabs.addTab(self.scai_tab, "快速分析")
        self.tabs.addTab(self.intro_tab, "工具簡介")

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

        # Get active tab and its index
        current_tab = self.tabs.currentWidget()
        current_index = self.tabs.currentIndex()
        if current_index == 2 :
            return
        # Redirect logs to the current tab if it supports append_log
        # This fixes missing info for both AI Tab and Screenshot Tab
        if hasattr(current_tab, "append_log"):
            sys.stdout = EmittingStream(text_written=current_tab.append_log)
            sys.stderr = EmittingStream(text_written=current_tab.append_log)

        self.run_btn.setEnabled(False)

        # Check if tab supports data collection
        if hasattr(current_tab, "get_payload_data"):
            try:
                # Prepare data
                payload = current_tab.get_payload_data()
                payload["api_key"] = api_key

                # Initialize and start Worker
                self.worker = Worker(payload, current_index)
                self.worker.finished_ok.connect(self.task_finished)
                self.worker.error.connect(self.task_error) 
                self.worker.start()
                
            except Exception as e:
                # Restore UI on immediate failure
                self.run_btn.setEnabled(True)
                self.task_error(f"Failed to start task: {str(e)}")
        else:
            # If tab doesn't support get_payload_data
            self.run_btn.setEnabled(True)
    
    def task_finished(self,result_text):
        """Handle successful completion and display result"""
        current_tab = self.tabs.currentWidget()
        
        # If the tab has a result display (like SCAI TAB), send the text there
        if hasattr(current_tab, "display_result"):
            current_tab.display_result(result_text)
        else :
            opf = self.worker.payload.get("output_folder")
            self.open_folder(opf)
        QMessageBox.information(self, "Done", "Completed")
        self.run_btn.setEnabled(True)


    def task_error(self, e):
        QMessageBox.critical(self, "Error", str(e))
        self.run_btn.setEnabled(True)    

    def open_folder(self, path):
        if not path:
            return
        os.startfile(path)