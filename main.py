# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QApplication, QMainWindow, QErrorMessage, QMessageBox, QHeaderView, QTableWidget, \
    QTableWidgetItem
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from math import *
from PySide6 import QtCore
from numpy import *
from casadi import *
from powell import *
from matplotlib.colors import LogNorm


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
        self.loaded.swanButton.clicked.connect(self.clearData)
        self.loaded.solve_button.clicked.connect(self.getSettingWithoutSwan)
        self.loaded.diagramButton.clicked.connect(self.diagramshow)

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




    def tempSlot(self, data):
        #print("Iam here - data received: " + str(data["x"]))
        x = data["x"]
        if len(x) < 3:
            self.xPlot.append(x[0])
            self.yPlot.append(x[1])
            self.zPlot.append(data["fmin"])

        row = [str(data["stop"]), str(data["fmin"]), str(data["x"])]
        self.addTableRow(row)

    def errorSlot(self, mgs):
        self._show_error(mgs)

    def _show_error(self, msg):
        error_dialog = QErrorMessage(self)
        error_dialog.setWindowTitle("Errors")
        error_dialog.showMessage(msg)


# FUNCTIONS TO DRAW

    def drawPoint(self):
        fig = plt.figure()
        # ax = plt.axes(projection='3d')

        X = np.asarray(self.xPlot)
        Y = np.asarray(self.yPlot)
        Z = np.asarray(self.zPlot)

        # X, Y = np.meshgrid(np.array(self.xPlot), np.array(self.yPlot))
        #surf = ax.plot_trisurf(X, Y, Z, linewidth=0, antialiased=False)

        # ax.plot_trisurf(X, Y, Z, color='green')
        # ax.set_title('wireframe geeks for geeks')
        plt.scatter(X, Y, c=Z, s = 20, cmap='plasma')

        #plt.ylim(-0.25,1.25)
        plt.colorbar(label='Wartość funkcji')
        plt.title('Punkty w kierunku minimalizacji')
        plt.xlabel('x1')
        plt.ylabel('x2')

        #plt.show()

    def drawlinePoint(self):
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        X = np.asarray(self.xPlot)
        Y = np.asarray(self.yPlot)
        Z = np.asarray(self.zPlot)

        #X, Y = np.meshgrid(np.array(self.xPlot), np.array(self.yPlot))
        # surf = ax.plot_trisurf(X, Y, Z, linewidth=0, antialiased=False)


        ax.plot3D(X, Y, Z, 'red')
        ax.set_title('Punty w kierunku minimalizacji')
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.set_zlabel('Wartość funckji')

        #plt.show()


    def draw3D(self,func):

        set_formula = func.replace("x1", "x")
        formula = set_formula.replace("x2", "y")

        formula = formula.replace('cos', 'np.cos')
        formula = formula.replace('sin', 'np.sin')
        formula = formula.replace('exp', 'np.exp')
        formula = formula.replace('pi', 'np.pi')
        formula = formula.replace('sqrt', 'np.sqrt')
        formula = formula.replace('log', 'np.log')

        def fuu(x, y, funct):
            return eval(funct)

        # x and y axis
        x = np.linspace(-1, 3, 100)
        y = np.linspace(-2, 3, 100)

        X, Y = np.meshgrid(x, y)
        Z = fuu(X, Y, formula)

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.plot_surface(X, Y, Z, cmap='plasma', edgecolor='none')  # cmap ='viridis'

        ax.set_title('Badana funkcja: ' + func)
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.set_zlabel('Wartość funckji')
        #plt.show()

    def draw2D(self,funct):

        set_formula = funct.replace("x1", "x")
        formula = set_formula.replace("x2", "y")

        formula = formula.replace('cos', 'np.cos')
        formula = formula.replace('sin', 'np.sin')
        formula = formula.replace('exp', 'np.exp')
        formula = formula.replace('pi', 'np.pi')
        formula = formula.replace('sqrt', 'np.sqrt')
        formula = formula.replace('log', 'np.log')



        # function for z axea
        def f(x, y, funct):
            return eval(funct)

        # x and y axis
        x = np.linspace(-1, 3, 100)
        y = np.linspace(-2, 3, 100)

        X, Y = np.meshgrid(x, y)
        Z = f(X, Y, formula)

        fig = plt.figure()

        plt.scatter(X, Y, c=Z, cmap='plasma')

        plt.colorbar(label='Wartość funkcji')
        plt.title('Badana funkcja: ' + funct)
        plt.xlabel('x1')
        plt.ylabel('x2')


    def drawCorrect(self,funct):

        set_formula = funct.replace("x1", "x")
        formula = set_formula.replace("x2", "y")

        formula = formula.replace('cos', 'np.cos')
        formula = formula.replace('sin', 'np.sin')
        formula = formula.replace('exp', 'np.exp')
        formula = formula.replace('pi', 'np.pi')
        formula = formula.replace('sqrt', 'np.sqrt')
        formula = formula.replace('log', 'np.log')


        XT = np.asarray(self.xPlot)
        YT = np.asarray(self.yPlot)
        ZT = np.asarray(self.zPlot)

        a1 = min(XT)
        a2 = min(YT)

        b1 = max(XT)
        b2 = max(YT)

        xmin = XT[-1]
        ymin = YT[-1]

        # function for z axea
        def f(x, y, funct):
            return eval(funct)

        # x and y axis
        x = np.linspace(a1-0.1, b1+0.1, 100)
        y = np.linspace(a2-0.1, b2+0.1, 100)

        X, Y = np.meshgrid(x, y)
        Z = f(X, Y, formula)

        # fig = plt.figure()
        #
        # plt.scatter(X, Y, c=Z, cmap='plasma')

        fig, ax = plt.subplots(1, 1)
        cp = ax.contourf(X, Y, Z, norm=LogNorm(), cmap='rainbow')

        plt.scatter(XT, YT, marker='o', c='b', s=5, zorder=10)

        plt.scatter(xmin, ymin, marker='x', c='r', s=100)

        fig.colorbar(cp, label='Wartość funkcji')

        # plt.colorbar(label='Wartość funkcji')
        plt.title('Badana funkcja: ' + funct)
        plt.xlabel('x1')
        plt.ylabel('x2')


# FUNCTION TO ADD ROW IN TABLE
    def addTableRow(self, row_data):
            row = self.loaded.tableWidget.rowCount()
            self.loaded.tableWidget.setRowCount(row+1)
            col = 0
            for item in row_data:
                cell = QTableWidgetItem(str(item))
                self.loaded.tableWidget.setItem(row, col, cell)
                col += 1


# FUNCTIONS TO GET SETTINGS
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

        if "x1" in formula:
            zerosPoint=1

        if "x2" in formula:
            zerosPoint = 2

        if "x3" in formula:
            zerosPoint = 3

        if "x4" in formula:
            zerosPoint=4

        if "x5" in formula:
            zerosPoint=5



        if len(formula) == 0 or len(estimation) == 0 or len(set_x0) == 0 or len(L) == 0 or len(x0) != zerosPoint:
            self._show_error('The required fields have not been completed or invalid zero point')
        else:
            return x0,numbOfIteration,epsilon,functionToPowell,set_formula


    def getSectionToGRM(self):
        a = self.loaded.sectionA.text()
        b = self.loaded.sectionB.text()

        if len(a) == 0 or len(b) == 0:
            self._show_error('The required fields have not been completed')
        else:
            return a, b

    @QtCore.Slot()
    def getSettingWithoutSwan(self):

        sectionAB = self.getSectionToGRM()
        a = float(sectionAB[0])
        b = float(sectionAB[1])
        x0, numbOfIteration, epsilon, functionToPowell, formula = self.getSettins()
        minimumPoint = self.powellInstance.powellMethodB(functionToPowell, x0, numbOfIteration, epsilon, a, b)

        for i in range(1, len(minimumPoint[0]) + 1):
            locals()['x%s' % i] = minimumPoint[0][i - 1]

        minimalizedFunction = eval(functionToPowell)

        # minimumPoint[0]

        finalMinimalizedFunction = str(minimalizedFunction)
        self.loaded.f_min.setText(finalMinimalizedFunction)

        finalMinimalPoint = str(minimumPoint[0])
        self.loaded.x_min.setText(finalMinimalPoint)

        krytStop = str(minimumPoint[1])
        self.loaded.epsilon.setText(krytStop)

        print("Minimum -> ", minimumPoint[0])
        print("KrytStop -> ", minimumPoint[1])
        print("F(minimum) = :", minimalizedFunction)

        if len(minimumPoint[0]) < 3:

            # self.draw3D(formula)
            #
            # self.draw2D(formula)
            #
            # self.drawPoint()
            # self.drawlinePoint()

            self.drawCorrect(formula)

        else:
            self.loaded.diagramButton.setEnabled(False)



        # msgBox = QMessageBox()
        # msgBox.setText("Liczymy Swonem!")
        # msgBox.exec()

    def clearData(self):

        ile = self.loaded.tableWidget.rowCount()
        #print(ile)
        for i in range (1,ile+1) :
            self.loaded.tableWidget.removeRow(ile-i)

        self.xPlot = []
        self.yPlot = []
        self.zPlot = []

        self.loaded.f_min.clear()
        self.loaded.x_min.clear()
        self.loaded.epsilon.clear()

        self.loaded.diagramButton.setEnabled(True)
        plt.close('all')

    def diagramshow(self):
        plt.show()


# MAIN FUNCTION
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = mainWindow()
    widget.show()
    sys.exit(app.exec())