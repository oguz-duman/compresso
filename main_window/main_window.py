from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QTextEdit, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import constants
import colors

from main_window.main_window_manager import MainWindowManager
from toolboxes.toolbox_adder import ToolboxAdder

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()  

        # Create main layout
        self.main_layout = QVBoxLayout(self) 
        self.main_layout.setContentsMargins(*constants.MAIN_WINDOW_MARGINS) 
        self.main_layout.setSpacing(constants.MAIN_WINDOW_SPACING)

        self.manager = MainWindowManager()

        # init top, mid and bottom layouts
        self.init_top_layout()
        self.init_midLayout()
        self.init_bottomLayout()


    def init_top_layout(self):
        # Top Layout
        top_layout = QHBoxLayout()
        self.main_layout.addLayout(top_layout, constants.VERTICAL_LAYOUT_RATIOS[0])  

        # Lef Layout 
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        top_layout.addLayout(left_layout, 50)

        # Left Title
        self.left_title = QLabel("")
        self.left_title.setText("Channel")
        left_layout.addWidget(self.left_title, alignment=Qt.AlignCenter)
        self.left_title.hide()

        # Left Textedit
        self.in_im_canvas = QTextEdit()  
        left_layout.addWidget(self.in_im_canvas)

        # Right Layout
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        top_layout.addLayout(right_layout, 50)

        # Right Title
        self.right_title = QLabel("")
        right_layout.addWidget(self.right_title, alignment=Qt.AlignCenter)
        self.right_title.hide()

        # Right Textedit
        self.out_im_canvas = QTextEdit()
        right_layout.addWidget(self.out_im_canvas)


    def init_midLayout(self):
        # CMid Layout
        midLayout = QHBoxLayout()
        self.main_layout.addLayout(midLayout, constants.VERTICAL_LAYOUT_RATIOS[1]) 
        font = QFont()              
        font.setPointSize(10)  
        
        # Button 1 
        btn = QPushButton(constants.OPEN_BUTTON)
        midLayout.addWidget(btn, 1)      
        btn.clicked.connect(self.open_file)   
        btn.setFlat(True)
        btn.setFont(font) 
        btn.setStyleSheet(f"""
            QPushButton {{
                padding-top: 10px;
                padding-bottom: 10px;
            }}
            QPushButton:hover {{
                background-color: {colors.COMBO_HOVER};
            }}
        """)

        # QomboBox 1
        self.vis_mod_list = QComboBox()
        midLayout.addWidget(self.vis_mod_list, 1)
        self.vis_mod_list.setFont(font)
        self.vis_mod_list.currentTextChanged.connect(lambda: self.switch_view(self.vis_mod_list.currentText()))  

        # QomboBox 2
        self.color_chan_list = QComboBox()
        midLayout.addWidget(self.color_chan_list, 1)
        self.color_chan_list.setFont(font)
        self.color_chan_list.currentTextChanged.connect(lambda: self.switch_color_chan(self.color_chan_list.currentText())) 

        # Button 2
        btn = QPushButton(constants.SAVE_BUTTON)
        midLayout.addWidget(btn, 1)   
        btn.clicked.connect(lambda: self.manager.save_file())   
        btn.setStyleSheet("padding-top: 10px; padding-bottom: 10px;")
        btn.setFont(font) 
        btn.setStyleSheet(f"""
            QPushButton {{
                padding-top: 10px;
                padding-bottom: 10px;
            }}
            QPushButton:hover {{
                background-color: {colors.COMBO_HOVER};
            }}
        """)


    def init_bottomLayout(self):
        # Bottom Layout
        bottomLayout = QHBoxLayout()
        self.main_layout.addLayout(bottomLayout, constants.VERTICAL_LAYOUT_RATIOS[2])
          
        # Scroll Area
        scrollArea = QScrollArea()         
        scrollArea.setWidgetResizable(True)        
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
        bottomLayout.addWidget(scrollArea)        
        
        # Content Widget
        contentWidget = QWidget()  
        scrollArea.setWidget(contentWidget)  

        # Content Layout
        self.contentLayout = QHBoxLayout(contentWidget)
        self.contentLayout.setAlignment(Qt.AlignLeft)
                
        # New Function
        self.add_new_box = ToolboxAdder()
        self.contentLayout.addWidget(self.add_new_box)
        #self.add_new_box.trigger.connect(self.insert_toolbox)  # connect click event to 'add_new_toolbox' method

        # drag and drop functionality
        contentWidget.setAcceptDrops(True)
        contentWidget.dragEnterEvent = self.manager.dragEnterEvent
        contentWidget.dropEvent = self.manager.dropEvent


    def open_file(self):
        text = self.manager.open_file()
        self.in_im_canvas.setText(text)

