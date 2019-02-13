from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as figureCanvas
import matplotlib.pyplot as plt
from PyQt5 import QtGui, QtWidgets
import sys
import os
import cv2 as cv
import numpy as np

# import the pre-made functions file as fn
import functions as fn

# import the interface created by qt designer
import design

class designWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super(designWindow, self).__init__()
        self.setupUi(self)

        ######## Start #########

        self.fig1 = fn.makeFigure(self.axes1)
        self.fig2 = fn.makeFigure(self.axes2)
        self.fig3 = fn.makeFigure(self.axes3)
        self.fig4 = fn.makeFigure(self.axes4)

        # connect graphic elements with their functions here
        self.btnBrowse.clicked.connect(self.getImage)
        self.btnShow.clicked.connect(self.showGraph)
        self.btnShow2.clicked.connect(self.showGraph2)

        radio = [self.btn8, self.btn16, self.btn32, self.btn64, self.btn256]
        self.group = QtWidgets.QButtonGroup()
        for btn in radio:
            self.group.addButton(btn)
        self.group.buttonClicked.connect(self.updateImage)

    # create custom functions here
    def getImage(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "choose image", "", "image files (*.jpg)")
        print(file[0])
        if file[0]:
            self.img = cv.imread(file[0])
            self.img = self.img[:, :, ::-1]

            self.fig1.clf()
            ax = self.fig1.add_subplot(111)
            ax.imshow(self.img)
            ax.axis("off")
            self.fig1.canvas.draw()

            self.img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
            self.updateImage()

    def showGraph(self):
        self.fig2.clf()
        ax = self.fig2.add_subplot(111)
        for i, ch in enumerate(['r', 'g', 'b']):
            hist = fn.imHist(self.img, i)
            ax.plot(hist, color=ch)
        self.fig2.canvas.draw()

    def getLevel(self):
        value = self.group.checkedButton().text()
        lvl = 256
        if (value.isdigit()):
            lvl = int(value)
        # print(lvl)
        return lvl

    def updateImage(self):
        self.fig3.clf()
        lvl = self.getLevel()
        new_img = np.copy(self.img_gray)
        new_img = np.rint(new_img/(256/lvl))*(256/lvl)
        ax = self.fig3.add_subplot(111)
        ax.imshow(new_img, cmap='gray')
        ax.axis("off")
        self.fig3.canvas.draw()

    def showGraph2(self):
        self.fig4.clf()
        lvl = self.getLevel()
        new_img = np.copy(self.img_gray)
        new_img[:, :] = np.rint(new_img[:, :] / (256 / lvl)) * (256 / lvl)
        hist = fn.imHist(new_img)
        ax = self.fig4.add_subplot(111)
        ax.plot(hist)
        self.fig4.canvas.draw()


     ######### End ##########

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = designWindow()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()