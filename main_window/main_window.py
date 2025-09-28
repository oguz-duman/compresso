from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QTextEdit, QComboBox
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont

import constants
import colors

from main_window.main_window_manager import MainWindowManager

from toolboxes.toolbox_adder import ToolboxAdder
from toolboxes.to_hex_toolbox import ToHexToolBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()  
        
        self.input_data = ""
        self.output_data = ""
        self.input_filepath = ""

        # Create main layout
        self.main_layout = QVBoxLayout(self) 
        self.main_layout.setContentsMargins(*constants.MAIN_WINDOW_MARGINS) 
        self.main_layout.setSpacing(constants.MAIN_WINDOW_SPACING)

        self.manager = MainWindowManager(self)
        self.manager.update_signal.connect(self.update_ui)

        # init top, mid and bottom layouts
        self.init_top_layout()
        self.init_midLayout()
        self.init_bottomLayout()


    def init_top_layout(self):
        # Top Layout
        top_layout = QHBoxLayout()
        self.main_layout.addLayout(top_layout, constants.VERTICAL_LAYOUT_RATIOS[0])  

        # Left Layout 
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
        self.left_text = QTextEdit()  
        self.left_text.textChanged.connect(self.on_input_text_changed)
        left_layout.addWidget(self.left_text)

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
        self.right_text = QTextEdit()
        self.left_text.textChanged.connect(self.on_output_text_changed)
        right_layout.addWidget(self.right_text)


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
        self.add_new_box.trigger.connect(self.insert_toolbox)  # connect click event to 'add_new_toolbox' method

        # drag and drop functionality
        contentWidget.setAcceptDrops(True)
        contentWidget.dragEnterEvent = self.manager.dragEnterEvent
        contentWidget.dropEvent = self.manager.dropEvent


    def open_file(self):
        self.input_filepath, text = self.manager.open_file()
        self.input_data = text
        self.output_data = text
        self.left_text.setText(text)
        self.right_text.setText(text)


    def insert_toolbox(self, toolbox_name):
        # Create a new method box based on the selected method name
        for toolbox in constants.TOOLBOXES.values():
            if toolbox_name == toolbox['NAME']:
                toolbox_class = globals()[toolbox['CLASS']]  
                #toolbox_class = getattr(self, toolbox['CLASS'])  
                new_toolbox = toolbox_class()  # create an instance of the toolbox class
                break

        # connect the toolbox signals
        new_toolbox.updateTrigger.connect(self.manager.execute_pipeline)   
        new_toolbox.removeTrigger.connect(self.remove_toolbox) 

        self.manager.pipeline_add_step(new_toolbox)                  

        # move special footer toolbox to the end of the scroll view
        self.contentLayout.removeWidget(self.add_new_box)      
        self.add_new_box.setParent(None)           
        self.contentLayout.addWidget(new_toolbox)                 
        self.contentLayout.addWidget(self.add_new_box)         


    def remove_toolbox(self):
        print("remove")
        pass

    @Slot(str)
    def update_ui(self, data):
        self.output_data = data
        self.right_text.setText(self.output_data)


    def on_input_text_changed(self):
        self.input_data = self.left_text.toPlainText()
        self.manager.execute_pipeline()


    def on_output_text_changed(self):
        self.output_data = self.right_text.toPlainText()
