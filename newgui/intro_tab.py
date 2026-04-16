from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class Intro_Tab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Overall background
        self.setStyleSheet("background-color: #0F0F0F;")
        
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Style definition for cards
        card_style = """
            QFrame {
                background-color: #1A1A1A;
                border: 1px solid #333333;
                border-radius: 12px;
            }
            QLabel {
                color: #E0E0E0;
                background-color: transparent;
                font-family: 'Segoe UI', '微軟正黑體';
            }
        """

        # --- Top Section (Horizontal Layout) ---
        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)

        # Left Block: Program Introduction
        self.left_card = QFrame()
        self.left_card.setStyleSheet(card_style)
        left_layout = QVBoxLayout(self.left_card)
        left_layout.setContentsMargins(25, 25, 25, 25)
        left_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop) # Force top-left alignment
        
        l_title = QLabel("程式介紹")
        l_title.setStyleSheet("color: #00D1FF; font-weight: bold; font-size: 25px; letter-spacing: 1px;")
        
        # Removed leading spaces from string
        intro_text = (
            "• 名稱: Trans-tool\n"
            "• 版本: v4.0\n"
            "• 最後更新: 2026/04/17\n"
            "• 作者: JHcube\n"
            "• 聯絡: cuberjhcubing@gmail.com"
        )
        l_content = QLabel(intro_text)
        l_content.setStyleSheet("color: #AAAAAA; font-size: 18px; line-height: 2.0;")
        
        left_layout.addWidget(l_title)
        left_layout.addWidget(l_content)
        left_layout.addStretch()

        # Right Block: Operation Guidelines
        self.right_card = QFrame()
        self.right_card.setStyleSheet(card_style)
        right_layout = QVBoxLayout(self.right_card)
        right_layout.setContentsMargins(25, 25, 25, 25)
        right_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        r_title = QLabel("操作說明")
        r_title.setStyleSheet("color: #FFB800; font-weight: bold; font-size: 25px; letter-spacing: 1px;")
        
        # Simplified sentences to prevent unwanted line breaks
        guide_text = (
            "• 檔案分析: 選擇資料夾，PDF 視為單份，其餘圖片合併處理。\n"
            "• 快速分析: 支援截圖後直接點選「貼上」即可提取文字內容。\n"
            "• 移植須知: 須包含執行檔、.env 與 promptLib 資料夾始可運作。\n"
            "• 模型維護: 可至 https://ai.google.dev/gemini-api/docs/models 取得模型代碼並修改.env。\n"
            "• 模型用量限制: 可至 https://aistudio.google.com/rate-limit 參考\n"
            "• 精準模式: 用於高精準模式的模型，有需求可調整.env中其他模型欄位。\n"
            "• 功能新增: 於 /promptLib/supportprompt 依格式添加名稱與描述。\n"
            "• 提示調整: 修改 /promptLib/mainprompt 內文，請勿變動格式結構。"
        )
        r_content = QLabel(guide_text)
        r_content.setWordWrap(True)
        r_content.setStyleSheet("color: #AAAAAA; font-size: 18px; line-height: 1.8;")

        right_layout.addWidget(r_title)
        right_layout.addWidget(r_content)
        right_layout.addStretch()

        # Add cards to top layout
        top_layout.addWidget(self.left_card, 1) # Ratio 1
        top_layout.addWidget(self.right_card, 2) # Ratio 2 (Right side is wider for more text)

        # --- Bottom Section (Terminal/Console) ---
        self.bottom_console = QTextEdit()
        self.bottom_console.setReadOnly(True)
        terminal_text = (
            ">> [SYSTEM]: Initializing Trans-tool v4.0...\n"
            ">> [BOOT]: Software started. Hope it doesn't crash.\n"
            ">> [INFO]: 99% of bugs are hidden by the dark mode.\n"
            ">> [WARN]: Execution speed depends on your internet and luck.\n"
            ">> [READY]: Feed me some files before I fall asleep.\n"
            ">> \n"
            ">> [MOTD]: ------------------------------------------\n"
            ">> Q: Why do programmers always mix up Halloween and Christmas?\n"
            ">> A: Because Oct 31 == Dec 25.\n"
            ">> --------------------------------------------------\n"
            ">> \n"
            ">> [STATUS]: System ready. Don't worry, the bugs are features.\n"
            ">> [PROMPT]: Awaiting user input..."
        )
        self.bottom_console.setText(terminal_text)
        
        self.bottom_console.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #33FF33;
                border: 1px solid #1A551A;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)

        # Main vertical structure: Top (3) vs Bottom (2)
        main_layout.addLayout(top_layout, 3)
        main_layout.addWidget(self.bottom_console, 2)

        self.setLayout(main_layout)