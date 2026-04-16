import io
import sys
import tempfile
from pathlib import Path
from PIL import Image, ImageGrab
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLineEdit, QTextEdit, QComboBox, QCheckBox, 
    QScrollArea, QSplitter
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from getprompt import get_prompt_titles
from getenv import get_models

class ScreenshotAITab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_image_obj = None 
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Vertical)

        # Upper section: Preview and Settings
        upper_widget = QWidget()
        upper_layout = QHBoxLayout(upper_widget)

        # Left: Image Preview Area
        left_box = QVBoxLayout()
        self.image_preview = QLabel("\n尚未加入圖片，可用 (Win+Shift+S) 截圖")
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setStyleSheet("""
            QLabel {
                border: 2px dashed #555; 
                background: #2d2d2d; 
                color: #888;
                font-size: 14px;
            }
        """)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_preview)
        self.scroll_area.setWidgetResizable(True)

        self.btn_grab = QPushButton("📋 從剪貼簿取得圖片")
        self.btn_grab.setFixedHeight(40)
        self.btn_grab.clicked.connect(self.grab_image)
        
        left_box.addWidget(self.scroll_area)
        left_box.addWidget(self.btn_grab)

        # Right: AI Settings Area
        right_box = QVBoxLayout()
        self.model_combo = QComboBox()
        self.model_combo.addItems(get_models())
        
        self.accuracy_checkbox = QCheckBox("增加精準度")
        self.feature_list = QListWidget()
        self.feature_list.setSelectionMode(QListWidget.MultiSelection)
        self.feature_list.addItems(get_prompt_titles())

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("額外需求")
        self.prompt_input.setFixedHeight(80)

        right_box.addWidget(QLabel("選擇模型"))
        right_box.addWidget(self.model_combo)
        right_box.addWidget(self.accuracy_checkbox)
        right_box.addWidget(QLabel("額外功能(可複選)"))
        right_box.addWidget(self.feature_list)
        right_box.addWidget(QLabel("額外指令"))
        right_box.addWidget(self.prompt_input)
        right_box.addStretch()

        upper_layout.addLayout(left_box, 2)
        upper_layout.addLayout(right_box, 1)

        # Lower section: AI Response Display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont("Consolas", 11))
        self.result_display.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #e0e0e0;
                border: 1px solid #333;
                padding: 10px;
            }
        """)

        splitter.addWidget(upper_widget)
        splitter.addWidget(self.result_display)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        layout.addWidget(splitter)

    def display_result(self, text):
        """Called by MainWindow to show AI response"""
        self.result_display.clear()
        self.result_display.setPlainText(text)

    def append_log(self, text):
        """Show log in the result display instead of a black hole"""
        if text.strip():
            self.result_display.append(text)
            sys.__stdout__.write(text)

    def grab_image(self):
        """Fetch image from clipboard and display correctly"""
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            self.current_image_obj = img
            # Use BytesIO to avoid color/stride issues
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            
            self.image_preview.setPixmap(
                pixmap.scaled(self.image_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            self.image_preview.setText("")
        else:
            self.result_display.setPlainText("⚠️ 剪貼簿中沒有圖片.")

    def get_payload_data(self):
        image_path_list = []
        if self.current_image_obj:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                self.current_image_obj.save(tmp.name, format="PNG")
                image_path_list.append(tmp.name)

        return {
            "model": self.model_combo.currentText(),
            "selected_features": [item.text() for item in self.feature_list.selectedItems()],
            "pdf_list": [],                
            "image_list": image_path_list,  
            "output_folder": self.current_output_folder if hasattr(self, 'current_output_folder') else "",
            "extra_prompt": self.prompt_input.toPlainText(),
            "use_accuracy": self.accuracy_checkbox.isChecked()
        }