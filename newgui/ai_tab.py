from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLineEdit, QTextEdit, QComboBox, QCheckBox, QFileDialog, QListWidgetItem
)
from PySide6.QtCore import Qt
from pathlib import Path
from getprompt import get_prompt_titles
from getenv import get_models


class AITab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_output_folder = ""
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        # Left
        left_layout = QVBoxLayout()
        self.source_list = QListWidget()
        
        # --- 樣式設定：來源檔案清單 ---
        self.source_list.setStyleSheet("""
            QListWidget {
                background-color: #2B2B2B; /* 深灰色背景 */
                color: #DDDDDD;            /* 淺灰色文字 */
                border: 1px solid #444444; /* 深色邊框 */
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #444444; /* 選取時的顏色 */
                color: #FFFFFF;
            }
        """)

        btn_add = QPushButton("新增檔案")
        btn_remove = QPushButton("移除選取")
        btn_add.clicked.connect(self.add_files)
        btn_remove.clicked.connect(self.remove_selected)

        file_btn_layout = QHBoxLayout()
        file_btn_layout.addWidget(btn_add)
        file_btn_layout.addWidget(btn_remove)

        left_layout.addWidget(QLabel("來源檔案"))
        left_layout.addWidget(self.source_list)
        left_layout.addLayout(file_btn_layout)

        # Right
        right_layout = QVBoxLayout()
        self.model_combo = QComboBox()
        self.model_combo.addItems(get_models())
        self.accuracy_checkbox = QCheckBox("提高格式精準度")
        self.feature_list = QListWidget()
        self.feature_list.setSelectionMode(QListWidget.MultiSelection)
        self.feature_list.addItems(get_prompt_titles())

        self.output_input = QLineEdit()
        self.output_input.textChanged.connect(self.update_output_folder)
        btn_output = QPushButton("選擇輸出資料夾")
        btn_output.clicked.connect(self.select_output_folder)

        self.prompt_input = QTextEdit()
        self.prompt_input.setFixedHeight(60)

        right_layout.addWidget(QLabel("模型"))
        right_layout.addWidget(self.model_combo)
        right_layout.addWidget(self.accuracy_checkbox)
        right_layout.addWidget(QLabel("功能"))
        right_layout.addWidget(self.feature_list)
        right_layout.addWidget(QLabel("輸出資料夾"))
        right_layout.addWidget(self.output_input)
        right_layout.addWidget(btn_output)
        right_layout.addWidget(QLabel("額外需求"))
        right_layout.addWidget(self.prompt_input)

        top_layout.addLayout(left_layout, 2)
        top_layout.addLayout(right_layout, 3)

        # Log
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlaceholderText("等待執行...")
        
        # --- 樣式設定：下方執行狀態 ---
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #242424; 
                color: #A0FFA0;           
                border: 1px solid #333333;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
        """)

        log_layout.addWidget(QLabel("執行狀態"))
        log_layout.addWidget(self.log_text)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(log_layout)

        self.setLayout(main_layout)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "選擇檔案")

        if files:
            for f in files:
                name = Path(f).name

                item = QListWidgetItem(name)
                item.setData(Qt.UserRole, f)

                self.source_list.addItem(item)

            # only first time
            if not self.current_output_folder:
                self.current_output_folder = str(Path(files[0]).parent)

            self.output_input.setText(self.current_output_folder)

    def remove_selected(self):
        for item in self.source_list.selectedItems():
            self.source_list.takeItem(self.source_list.row(item))

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "選擇輸出資料夾",
            self.current_output_folder or str(Path.home())
        )
        if folder:
            self.current_output_folder = folder
            self.output_input.setText(folder)

    def update_output_folder(self, text):
        self.current_output_folder = text

    def append_log(self, text):
        self.log_text.append(text)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def get_payload_data(self):
        files = [
            self.source_list.item(i).data(Qt.UserRole)
            for i in range(self.source_list.count())
        ]

        return {
            "model": self.model_combo.currentText(),
            "selected_features": [item.text() for item in self.feature_list.selectedItems()],
            "pdf_list": [f for f in files if f.lower().endswith(".pdf")],
            "image_list": [f for f in files if not f.lower().endswith(".pdf")],
            "output_folder": self.current_output_folder,
            "extra_prompt": self.prompt_input.toPlainText(),
            "use_accuracy": self.accuracy_checkbox.isChecked()
        }