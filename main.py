# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox, QHeaderView, QTableWidget, \
    QTableWidgetItem
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtCore
from numpy import append

from powell import *


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.loaded = self.load_ui()
        self.powellInstance = PowellInstance(self)
        self.init_connections()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, False)
        self.xPlot = []
        self.yPlot = []
        self.zPlot = []

    def init_connections(self):
        self.loaded.swanButton.clicked.connect(self.getSettingforSwan)
        self.loaded.solve_button.clicked.connect(self.getSettingWithoutSwan)

    def tempSlot(self, data):
        #print("Iam here - data received: " + str(data["x"]))
        x = data["x"]
        print(len(x))
        self.xPlot.append(x[0])
        self.yPlot.append(x[1])
        self.zPlot.append(data["fmin"])

        row = [str(data["stop"]), str(data["fmin"]), str(data["x"])]
        self.addTableRow(row)


    def draw(self):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        X, Y = np.meshgrid(np.array(self.xPlot), np.array(self.yPlot))
        X = np.asarray(self.xPlot)
        Y = np.asarray(self.yPlot)
        Z = np.asarray(self.zPlot)

        #surf = ax.plot_trisurf(X, Y, Z, linewidth=0, antialiased=False)

        ax.plot_trisurf(X, Y, Z, color='green')
        ax.set_title('wireframe geeks for geeks')
        plt.show()


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

    def getSettins(self):
        set_x0 = self.loaded.startPoint.text()      #Pobranie punktu startowego
        x0 = [float(x) for x in set_x0.split(',')]

        L=self.loaded.iteration.text()
        numbOfIteration=int(L)      #Pobranie liczby iteracji


        estimation = self.loaded.accuracy.text()
        epsilon = eval(estimation.replace("^", "**"))  # Pobranie dokładności

        formula = self.loaded.function.text()           #Pobranie funckji
        set_formula = formula.replace("^", "**")
        functionToPowell = parser.expr(set_formula).compile()

        if len(formula) == 0 or len(estimation) == 0 or len(set_x0) == 0 or len(L) == 0:
            self._show_error('Fild allll')
        else:
            return x0,numbOfIteration,epsilon,functionToPowell,formula



    @QtCore.Slot()
    def solution(self):
        solv = self.loaded.function.text()
        self.loaded.solution.setText(solv)

    @QtCore.Slot()
    def getSettingforSwan(self):

        x0, numbOfIteration, epsilon, functionToPowell,formula = self.getSettins()
        minimumPoint = self.powellInstance.powellMethodA(functionToPowell, x0, numbOfIteration, epsilon, h=0.1)

        for i in range(1, len(minimumPoint[0]) + 1):
            locals()['x%s' % i] = minimumPoint[0][i - 1]

        minimalizedFunction = eval(functionToPowell)

        #minimumPoint[0]


        finalMinimalizedFunction = str(minimalizedFunction)
        self.loaded.f_min.setText(finalMinimalizedFunction)

        finalMinimalPoint = str(minimumPoint[0])
        self.loaded.x_min.setText(finalMinimalPoint)

        krytStop = str(minimumPoint[1])
        self.loaded.epsilon.setText(krytStop)

        print("Minimum -> ", minimumPoint[0])
        print("KrytStop -> ", minimumPoint[1])
        print("F(minimum) = :", minimalizedFunction)

        self.draw()


        # msgBox = QMessageBox()
        # msgBox.setText("Liczymy Swonem!")
        # msgBox.exec()

    def addTableRow(self, row_data):
            row = self.loaded.tableWidget.rowCount()
            self.loaded.tableWidget.setRowCount(row+1)
            col = 0
            for item in row_data:
                cell = QTableWidgetItem(str(item))
                self.loaded.tableWidget.setItem(row, col, cell)
                col += 1

    @QtCore.Slot()
    def getSettingWithoutSwan(self):
        for i in range (20):
            row_2 = ['002', 'Lily', 32]
            self.addTableRow(row_2)
            self.loaded.tableWidget.scrollToBottom()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = mainWindow()
    widget.show()
    sys.exit(app.exec())