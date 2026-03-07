import os
import re
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog, QMessageBox,
    QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PyPDF2 import PdfReader
from getprompt import get_prompt_titles
from getenv import get_models,set_api_key
from processfile import processfile
from gui_logger import EmittingStream
from worker import Worker

class OCRTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("題目輔助工具")
        self.resize(1500, 800)

        # API Key and Save button in same row
        self.api_label = QLabel("API Key:")
        self.api_input = QLineEdit()
        self.api_input.setText(os.getenv("API_KEY", ""))  # load .env API_KEY

        self.save_api_button = QPushButton("儲存API_KEY")
        self.save_api_button.clicked.connect(self.save_api_key)

        api_layout = QHBoxLayout()
        api_layout.addWidget(self.api_label)
        api_layout.addWidget(self.api_input)
        api_layout.addWidget(self.save_api_button)

        # MODEL Selection (single choice)
        model_layout = QHBoxLayout()
        model_layout.setAlignment(Qt.AlignLeft)
        self.model_label = QLabel("選擇模型:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(get_models())
        model_layout.addWidget(self.model_label)
        model_layout.addWidget(self.model_combo)

        # Prompt / Feature selection (multi choice)
        self.feature_label = QLabel("額外功能(可選):")
        self.feature_list = QListWidget()
        self.feature_list.setSelectionMode(QListWidget.MultiSelection)
        self.feature_list.addItems(get_prompt_titles())
        self.feature_list.setFixedHeight(150)

        # Source files
        self.source_label = QLabel("來源檔案(PDF / Images):")
        self.source_list = QListWidget()
        self.source_list.setFixedHeight(180)
        self.add_button = QPushButton("新增檔案")
        self.add_button.clicked.connect(self.add_files)
        self.remove_button = QPushButton("移除所選檔案")
        self.remove_button.clicked.connect(self.remove_selected)
        source_button_layout = QVBoxLayout()
        source_button_layout.addWidget(self.add_button)
        source_button_layout.addWidget(self.remove_button)
        source_layout = QHBoxLayout()
        source_layout.addWidget(self.source_list)
        source_layout.addLayout(source_button_layout)

        # Output folder
        output_layout = QHBoxLayout()
        output_layout.setAlignment(Qt.AlignLeft)
        self.output_label = QLabel("輸出路徑:")
        self.output_input = QLineEdit()
        self.output_button = QPushButton("選擇輸出位置")
        self.output_button.clicked.connect(self.select_output_folder)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_input)
        output_layout.addWidget(self.output_button)

        # Extra prompt
        extra_prompt_layout = QHBoxLayout()
        extra_prompt_layout.setAlignment(Qt.AlignLeft)
        self.prompt_label = QLabel("額外需求:")
        self.prompt_input = QTextEdit()
        self.prompt_input.setFixedHeight(40)
        extra_prompt_layout.addWidget(self.prompt_label)
        extra_prompt_layout.addWidget(self.prompt_input)

        # Run / Cancel
        self.run_button = QPushButton("執行")
        self.cancel_button = QPushButton("離開")
        self.run_button.clicked.connect(self.run_action)
        self.cancel_button.clicked.connect(self.cancel_action)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.cancel_button)

        # log Output
        self.log_label = QLabel("目前進度:")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 12))
        #self.log_text.setMaximumWidth(600)

        # stdout / stderr
        sys.stdout = EmittingStream(text_written=self.append_log)
        sys.stderr = EmittingStream(text_written=self.append_log)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(api_layout)  # API key row
        layout.addLayout(model_layout)
        layout.addWidget(self.feature_label)
        layout.addWidget(self.feature_list)
        layout.addWidget(self.source_label)
        layout.addLayout(source_layout)
        layout.addLayout(output_layout)
        layout.addLayout(extra_prompt_layout)
        layout.addWidget(self.log_label)
        layout.addWidget(self.log_text)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_api_key(self):
        key = self.api_input.text().strip()
        set_api_key(key)
        QMessageBox.information(self, "Saved", "成功儲存API_KEY")

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Source Files",
            "",
            "PDF and Images (*.pdf *.png *.jpg *.jpeg *.bmp)"
        )
        if files:
            for file in files:
                display_name = Path(file).name
                if file.lower().endswith(".pdf"):
                    try:
                        reader = PdfReader(file)
                        pages = len(reader.pages)
                        display_name += f" (共 {pages} 頁)"
                    except Exception:
                        display_name += " (PDF)"
                else:
                    display_name += " (Image)"
                self.source_list.addItem(f"{display_name} | {file}")

            if not self.output_input.text():
                self.output_input.setText(str(Path(files[0]).parent))

    def remove_selected(self):
        for item in self.source_list.selectedItems():
            self.source_list.takeItem(self.source_list.row(item))

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            self.output_input.text() or str(Path.home())
        )
        if folder:
            self.output_input.setText(folder)
    def validate_inputs(self, api_key, pdf_list, image_list, output_folder):
        if not api_key:
            QMessageBox.warning(self, "Missing API Key", "請輸入API_KEY")
            return False

        if not pdf_list and not image_list:
            QMessageBox.warning(self, "No Input Files", "目前沒有任何檔案")
            return False

        if not output_folder:
            QMessageBox.warning(self, "Invalid Output Folder", "請選擇輸出路徑")
            return False

        if not os.path.exists(output_folder):
            QMessageBox.warning(self, "Invalid Output Folder", "輸出路徑不存在，請重新選擇")
            return False

        if not os.path.isdir(output_folder):
            QMessageBox.warning(self, "Invalid Output Folder", "輸出路徑必須是資料夾")
            return False

        return True

    def run_action(self):
        api_key = self.api_input.text().strip()
        model = self.model_combo.currentText()
        selected_features = [item.text() for item in self.feature_list.selectedItems()]

        pdf_list = []
        image_list = []

        for i in range(self.source_list.count()):
            text = self.source_list.item(i).text()
            file_path = text.split(" | ")[1]
            if file_path.lower().endswith(".pdf"):
                pdf_list.append(file_path)
            else:
                image_list.append(file_path)

        output_folder = self.output_input.text()

        if not self.validate_inputs(api_key, pdf_list, image_list, output_folder):
            return

        payload = {
            "api_key": api_key,
            "model": model,
            "selected_features": selected_features,
            "pdf_list": pdf_list,
            "image_list": image_list,
            "output_folder": output_folder,
            "extra_prompt": self.prompt_input.toPlainText()
        }

        self.run_button.setEnabled(False)
        self.worker = Worker(payload)
        self.worker.finished.connect(self.process_finished)
        self.worker.start()

    def process_finished(self):
        QMessageBox.information(self, "OCR Complete", "執行完成!")
        import os
        os.startfile(self.output_input.text())
        self.run_button.setEnabled(True)

    def cancel_action(self):
        self.close()

    def append_log(self, text):
        self.log_text.append(text)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )