from PySide6.QtWidgets import QVBoxLayout, QPushButton, QDialog, QHBoxLayout, QLabel

class EncodingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Encoding")
        
        self.selected_encoding = None
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)   
        layout.setSpacing(15)   
        label = QLabel("Choose an encoding:")
        layout.addWidget(label)
        
        # Buttons for encoding options
        encodings = ["utf-8", "utf-16-le", "utf-16-be", "utf-32-le", "utf-32-be"]
        
        buttons_layout = QHBoxLayout()
        for enc in encodings:
            btn = QPushButton(enc)
            btn.clicked.connect(lambda checked, e=enc: self.select_encoding(e))
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
    
    def select_encoding(self, encoding):
        self.selected_encoding = encoding
        self.accept()   # Close the dialog