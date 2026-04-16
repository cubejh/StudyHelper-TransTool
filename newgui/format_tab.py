from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog

class FormatTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.file_input = QLineEdit()
        self.output_input = QLineEdit()

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["AI修正", "程式修正"])

        btn_file = QPushButton("選擇檔案")
        btn_output = QPushButton("選擇輸出資料夾")

        btn_file.clicked.connect(self.select_file)
        btn_output.clicked.connect(self.select_folder)

        layout.addWidget(QLabel("檔案"))
        layout.addWidget(self.file_input)
        layout.addWidget(btn_file)

        layout.addWidget(QLabel("輸出"))
        layout.addWidget(self.output_input)
        layout.addWidget(btn_output)

        layout.addWidget(QLabel("模式"))
        layout.addWidget(self.mode_combo)

        self.setLayout(layout)

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "選擇檔案")
        if file:
            self.file_input.setText(file)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "選擇資料夾")
        if folder:
            self.output_input.setText(folder)

    def get_payload_data(self):
        return {
            "file": self.file_input.text(),
            "output": self.output_input.text(),
            "mode": self.mode_combo.currentText()
        }