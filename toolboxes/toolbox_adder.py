import uuid

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QSizePolicy, QFrame

import constants

from ui_components.DarkComboBox import DarkComboBox


class ToolboxAdder(QWidget):
    """ A toolbox that allows the user to add new toolboxes. """

    # Signal to communicate with the main application
    trigger = Signal(str)

    def __init__(self):
        super().__init__()

        # generate a unique id for the toolbox
        self.id = str(uuid.uuid4())                     

        # make the widget fixed size
        self.setFixedWidth(200)
        
        # set a font size variable
        self.font = QFont()              
        self.font.setPointSize(10)  

        # set the layout for the widget
        mainLayout = QVBoxLayout(self) 
        mainLayout.setContentsMargins(0, 0, 0, 0)

        # create a frame to hold the content
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("QFrame#Frame { border: 2px solid gray; border-radius: 10px; }")
        frame.setObjectName("Frame")
        frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        frame.setFixedWidth(200)
        mainLayout.addWidget(frame)     

        # create a layout inside the frame
        self.frameLayout = QVBoxLayout(frame)
        self.frameLayout.setContentsMargins(10, 10, 10, 10)

        # create a title label
        label = QLabel(constants.ADD_TOOLBOX_TITLE)
        label.setFont(self.font)
        label.setAlignment(Qt.AlignHCenter)
        self.frameLayout.addWidget(label)
        
        # Create a combo box to select the toolbox
        self.combo = DarkComboBox([toolbox['NAME'] for toolbox in constants.TOOLBOXES.values()])
        self.combo.setFont(self.font)
        self.frameLayout.addWidget(self.combo, alignment=Qt.AlignVCenter)

        # Create a button to add a new method
        newBtn = QPushButton("+")
        font = QFont()              
        font.setPointSize(20)  
        newBtn.setFont(font) 
        newBtn.setStyleSheet("padding-top: 5px; padding-bottom: 10px;")     
        newBtn.clicked.connect(lambda: self.trigger.emit(self.combo.currentText()))  
        self.frameLayout.addWidget(newBtn, alignment=Qt.AlignVCenter)

