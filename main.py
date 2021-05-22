# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtCore

class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        self.loaded = self.load_ui()
        self.init_connections()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, False)

    def init_connections(self):
        self.loaded.swanButton.clicked.connect(self.getSettingforSwan)
        self.loaded.solve_button.clicked.connect(self.getSettingWithoutSwan)
        self.loaded.pushButton_2.clicked.connect(self.solution)


    def show(self):
        self.loaded.show()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loaded = loader.load(ui_file, self)
        ui_file.close()
        return loaded

    def _show_error(self, msg):
        error_dialog = QErrorMessage(self)
        error_dialog.setWindowTitle("Errors")
        error_dialog.showMessage(msg)

    @QtCore.Slot()
    def solution(self):
        powell = self.loaded.function.text()
        self.loaded.solution.setText(powell)

    @QtCore.Slot()
    def getSettingforSwan(self):
        functionToPowell = self.loaded.function.text()
        epsilon = self.loaded.accuracy.text()
        starPoint = self.loaded.startPoint.text()
        numbOfIteration = self.loaded.iteration.text()

        if len(functionToPowell) == 0 or len(epsilon) == 0 or len(starPoint) == 0 or len(numbOfIteration) == 0:
            self._show_error('Fild allll')
        else:
            msgBox = QMessageBox()
            msgBox.setText("Liczymy Swonem!")
            msgBox.exec()

    @QtCore.Slot()
    def getSettingWithoutSwan(self):
        functionToPowell = self.loaded.function.text()
        epsilon = self.loaded.accuracy.text()
        starPoint = self.loaded.startPoint.text()
        numbOfIteration = self.loaded.iteration.text()
        setA = self.loaded.sectionA.text()
        setB = self.loaded.sectionB.text()

        if len(functionToPowell) == 0 or len(epsilon) == 0 or len(starPoint) == 0 or len(numbOfIteration) == 0 or len(setA) == 0 or len(setB) == 0:
            self.loaded.QErrorMessage.showMessage('Fill in all fields to calculate!')
        else:
            msgBox = QMessageBox()
            msgBox.setText("Liczymy bez Swonna!")
            msgBox.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = main()
    widget.show()
    sys.exit(app.exec())