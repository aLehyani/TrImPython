### some pre-made functions ###
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as figureCanvas
import matplotlib.pyplot as plt
from PyQt5 import QtGui, QtWidgets
import sys
import os
import cv2 as cv
import numpy as np

# add figure widget to a layout
def makeFigure(axes):
    fig = Figure()
    addImage(fig, axes)
    return fig

# function to add image/graph to widget
def addImage(fig, view):
    canvas = figureCanvas(fig)
    view.addWidget(canvas)
    canvas.draw()

# calculate image histogram
def imHist(img, ch = 0):
    return cv.calcHist([img], [ch], None, [256], [0, 256])
