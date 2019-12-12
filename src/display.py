from __future__ import print_function
import pyqtgraph as pg
import psana
import numpy as np
from IPython import embed
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import argparse
import sys, signal

parser = argparse.ArgumentParser()
parser.add_argument("-e","--exp", help="experiment name (e.g. cxis0813)", type=str)
parser.add_argument("-r","--run", help="run number (e.g. 5)", type=int)
parser.add_argument("-d","--det", help="detector name (e.g. DscCsPad)", type=str)
parser.add_argument("-n","--evt", help="event number (e.g. 1), default=0",default=0, type=int)
parser.add_argument("--localCalib", help="use local calib directory, default=False", action='store_true')
args = parser.parse_args()

if args.localCalib:
    print("Using local calib directory")
    psana.setOption('psana.calib-dir','./calib')

print("Getting event: ", args.evt)
ds = psana.DataSource('exp='+args.exp+':run='+str(args.run)+':idx')
det = psana.Detector(args.det, ds.env())
run = next(ds.runs())
times = run.times()
evt = run.event(times[args.evt])

nda = det.calib(evt)
data = det.image(evt,nda)

pixelIndex = np.arange(1,nda.size+1)
minVal = np.min(pixelIndex)
maxVal = np.max(pixelIndex)
pixelIndex[-1] = minVal
pixelIndex[0] = maxVal
pixelIndex = pixelIndex.reshape(nda.shape)

pixelIndex = det.image(evt,pixelIndex)

###
print("Note: Pixel index order is from black to white. Except for better contrast, first pixel is in white and last pixel is in black.")
print("Note: The images are drawn with pyqtgraph. A matplotlib display will render pixels differently.")

class MainFrame(QtGui.QWidget):
    """
    The main frame of the application
    """
    def __init__(self, arg_list):
        super(MainFrame, self).__init__()

        self.win = QtGui.QMainWindow()
        self.area = DockArea()
        self.win.resize(1300,1300)
        self.win.setCentralWidget(self.area)
        self.win.setWindowTitle('ImageView')
        self.d1 = Dock("Assembled image", size=(800, 800))
        self.d2 = Dock("Pixel index (dark to light). Exception: First pixel is white, Last pixel is black", size=(800, 800))
        self.area.addDock(self.d1, 'left')
        self.area.addDock(self.d2, 'right')
        self.w1 = pg.ImageView()
        self.w1.setImage(data)
        self.d1.addWidget(self.w1)
        self.w2 = pg.ImageView()
        self.w2.setImage(pixelIndex)
        self.d2.addWidget(self.w2)
        self.win.show()

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    ex = MainFrame(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
