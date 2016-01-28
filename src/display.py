import pyqtgraph as pg
import psana
import numpy as np
from IPython import embed
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e","--exp", help="experiment name (e.g. cxis0813)", type=str)
parser.add_argument("-r","--run", help="run number (e.g. 5)", type=int)
parser.add_argument("-d","--det", help="detector name (e.g. DscCsPad)", type=str)
parser.add_argument("-n","--evt", help="event number (e.g. 1), default=0",default=0, type=int)
parser.add_argument("--localCalib", help="use local calib directory, default=False", action='store_true')
args = parser.parse_args()

if args.localCalib:
    print "Using local calib directory"
    psana.setOption('psana.calib-dir','./calib')

ds = psana.DataSource('exp='+args.exp+':run='+str(args.run)+':idx')
det = psana.Detector(args.det, ds.env())
run = ds.runs().next()
times = run.times()
evt = run.event(times[args.evt])

nda = det.calib(evt)
data = det.image(evt,nda)

pixelIndex = np.arange(1,nda.size+1)
pixelIndex[0] = np.max(pixelIndex)
pixelIndex[-1] = np.min(pixelIndex)
pixelIndex.reshape(nda.shape)
pixelIndex = det.image(evt,pixelIndex)

###
print "Note: Pixel index order is from black to white. Except for better contrast, first pixel is in white and last pixel is in black."
print "Note: The images are drawn with pyqtgraph. A matplotlib display will render pixels differently."
app = QtGui.QApplication([])

## Create window with ImageView widget

win = QtGui.QMainWindow()
area = DockArea()
win.resize(1300,1300)
win.setCentralWidget(area)

win.setWindowTitle('ImageView')
d1 = Dock("Assembled image", size=(800, 800))
d2 = Dock("Pixel index (dark to light). Exception: First pixel is white, Last pixel is black", size=(800, 800))
area.addDock(d1, 'left')
area.addDock(d2, 'right')
w1 = pg.ImageView()#view=pg.PlotItem())
w1.setImage(data)
d1.addWidget(w1)
w2 = pg.ImageView()#view=pg.PlotItem())
w2.setImage(pixelIndex)
d2.addWidget(w2)
win.show()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()