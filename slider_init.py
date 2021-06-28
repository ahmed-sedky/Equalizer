from PyQt5 import QtCore, QtGui, QtWidgets
class slider(object):
    def set_range(self,fmin,fmax):
        self.fmin=fmin
        self.fmax=fmax
    def setupUi(self, Mainwindow,groupBox):
        self.fmin=0
        self.fmax=0
        self.slider1 = QtWidgets.QSlider(groupBox)
        self.slider1.setMouseTracking(False)
        self.slider1.setMaximum(5)
        self.slider1.setOrientation(QtCore.Qt.Vertical)
        self.slider1.setObjectName("slider1")
        self.slider1.setValue(1)
        self.slider1.valueChanged[int].connect(lambda value:Mainwindow.gain(value,self.fmin,self.fmax))
        #self.gridLayout.addWidget(self.slider1, 1, 1, 7, 1)