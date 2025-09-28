import uuid

from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QFont, QDrag
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QCheckBox


class Toolbox(QWidget):
    """ A base class for all toolboxes. It provides a common interface. """

    # Signals to communicate with the main application
    updateTrigger = Signal()
    removeTrigger = Signal(str)
   

    def __init__(self, title="Toolbox"):
        super().__init__()

        self.contentLayout = QVBoxLayout()              # create a layout to hold the content of the toolbox

        self.title = title                      
        self.id = str(uuid.uuid4())             
        self.initiate_ui()                      


    def initiate_ui(self):
        self.setFixedWidth(200)             
        
        self.font = QFont()              
        self.font.setPointSize(10)  

        mainLayout = QVBoxLayout(self) 
        mainLayout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("QFrame#Frame { border: 2px solid gray; border-radius: 10px; }")
        frame.setObjectName("Frame")
        frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        frame.setFixedWidth(200)
        mainLayout.addWidget(frame)     

        frameLayout = QVBoxLayout(frame)
        frameLayout.setContentsMargins(10, 10, 10, 10)

        # create a horizontal layout for the title and remove button
        titleLayout = QHBoxLayout()
        frameLayout.addLayout(titleLayout, 1)
        titleLayout.setAlignment(Qt.AlignTop)

        # create a title label
        label = QLabel(self.title)
        label.setFont(self.font)
        titleLayout.addWidget(label)

        # create a button to remove the toolbox
        removeBtn = QPushButton("X")
        removeBtn.setFont(self.font)
        removeBtn.setFixedWidth(30)
        removeBtn.clicked.connect(lambda: self.removeTrigger.emit(self.id))
        titleLayout.addWidget(removeBtn,1)
        
        # create a layout for the ON/OFF switch
        switchLayout = QHBoxLayout()
        frameLayout.addLayout(switchLayout, 1)

        # create ON/OFF switch
        self.switch = QCheckBox("On/Off")
        self.switch.setChecked(True)
        self.switch.setFont(self.font)
        self.switch.stateChanged.connect(lambda: self.updateTrigger.emit())
        self.switch.setFixedHeight(30)
        switchLayout.addWidget(self.switch, alignment=Qt.AlignTop)

        # add the content layout to the frame layout
        frameLayout.addLayout(self.contentLayout, 4)

        # add a dummy widget to fill the space
        dummy = QWidget()
        dummy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.contentLayout.addWidget(dummy)
    

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStartPosition = event.position()


    def mouseMoveEvent(self, event):
        # Check if the left mouse button is pressed
        if not event.buttons() & Qt.LeftButton:
            return
        # Check if the mouse has moved beyond a small threshold
        if (event.position() - self.dragStartPosition).manhattanLength() < 10:
            return

        drag = QDrag(self)                              # Create a QDrag object to handle the drag operation
        mimeData = QMimeData()                          # Create a QMimeData object to store data for the drag
        drag.setMimeData(mimeData)                      
        drag.setHotSpot(event.position().toPoint())     # Set the hotspot for the drag operation
        drag.setPixmap(self.grab())                     # # Set the pixmap for the drag operation (visual representation)
        drag.exec(Qt.MoveAction)                        # Execute the drag operation with a move action

