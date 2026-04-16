import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QTabWidget
)
from PySide6.QtGui import QFont

from getenv import set_api_key
from worker import Worker

from ai_tab import AITab
from format_tab import FormatTab


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OCR Tool")
        self.resize(1400, 800)

        layout = QVBoxLayout()

        # ===== API =====
        api_layout = QHBoxLayout()
        self.api_input = QLineEdit(os.getenv("API_KEY", ""))
        save_btn = QPushButton("Save API Key")
        save_btn.clicked.connect(self.save_api)

        api_layout.addWidget(QLabel("API Key:"))
        api_layout.addWidget(self.api_input)
        api_layout.addWidget(save_btn)

        # ===== Tabs =====
        self.tabs = QTabWidget()

        self.ai_tab = AITab()
        self.format_tab = FormatTab()

        self.tabs.addTab(self.ai_tab, "AI")
        self.tabs.addTab(self.format_tab, "Format")

        # ===== Run Button =====
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_task)

        layout.addLayout(api_layout)
        layout.addWidget(self.tabs)
        layout.addWidget(self.run_button)

        self.setLayout(layout)
        self.set_dark_theme()

    def save_api(self):
        key = self.api_input.text().strip()
        set_api_key(key)
        QMessageBox.information(self, "Saved", "API key saved")

    def run_task(self):
        api_key = self.api_input.text().strip()

        if not api_key:
            QMessageBox.warning(self, "Error", "Missing API Key")
            return

        current_tab = self.tabs.currentWidget()

        # ===== AI Tab =====
        if current_tab == self.ai_tab:
            payload = self.ai_tab.get_payload_data()
            payload["api_key"] = api_key

        # ===== Format Tab =====
        elif current_tab == self.format_tab:
            payload = self.format_tab.get_payload_data()
            payload["api_key"] = api_key

        else:
            return

        self.run_button.setEnabled(False)

        self.worker = Worker(payload)
        self.worker.finished.connect(self.task_finished)
        self.worker.start()

    def task_finished(self):
        QMessageBox.information(self, "Done", "Completed")
        self.run_button.setEnabled(True)

    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget { background:#1e1e1e; color:#ddd; }
            QPushButton { background:#444; padding:6px; }
            QPushButton:hover { background:#666; }
            QLineEdit { background:#2d2d2d; }
        """)