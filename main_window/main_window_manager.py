from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialog
from PySide6.QtCore import QObject, Signal
from ui_components.encoding_dialog import EncodingDialog

class MainWindowManager(QObject):
    update_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = self.parent()
        self.pipeline = []


    def open_file(self):
        # open a dialog to select encoding
        dialog = EncodingDialog()
        if dialog.exec() == QDialog.Accepted:
            encoding = dialog.selected_encoding
        else:
            return  # canceled
    
        filePath, _ = QFileDialog.getOpenFileName(None, "Select an input file")

        if filePath:
            with open(filePath, "r", encoding=encoding) as f:
                data = f.read()
                return filePath, data

                
    def save_file(self):
        # open a dialog to select encoding
        dialog = EncodingDialog()
        if dialog.exec() == QDialog.Accepted:
            encoding = dialog.selected_encoding
        else:
            return  # canceled
        
        filePath, _ = QFileDialog.getSaveFileName(None, "Save the file")
        
        if filePath:
            try:
                with open(filePath, "w", encoding=encoding) as f:
                    f.write(self.main_window.output_data)
            except Exception as e:
                QMessageBox.information(None, "Error", f"Failed to save the image.\n{str(e)}")


    def dragEnterEvent(self, event):
        if event.mimeData():
            event.acceptProposedAction()


    def dropEvent(self, event):
        pos = event.position().toPoint()                
        source = event.source()                         
        index = self.find_insert_index(pos)             

        # Check if the source is a valid FunctionBox
        if source and isinstance(source, self.Toolbox):
            self.pipeline.move_step(source, index)              
            self.contentLayout.removeWidget(source)             
            self.contentLayout.insertWidget(index, source)      

            event.acceptProposedAction()            
            self.pipeline_on_change()                     


    def find_insert_index(self, pos):
        for i in range(self.contentLayout.count()):
            widget = self.contentLayout.itemAt(i).widget()
            if widget and widget != self.add_new_box:
                if widget.geometry().contains(pos):
                    return i
        return self.contentLayout.count() - 1


    def execute_pipeline(self):
        data = self.main_window.input_data
        for step in self.pipeline:
            data = step.execute(data)
        self.update_signal.emit(data)
        

    def pipeline_add_step(self, step):
        self.pipeline.append(step)
        self.execute_pipeline()
