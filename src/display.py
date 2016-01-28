import pyqtgraph as pg
import psana
import numpy as np
from IPython import embed
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *

experimentName='xpptut15'
runNumber=54
detectorName='cspad'
evtNumber = 0

ds = psana.DataSource('exp='+experimentName+':run='+str(runNumber)+':idx')
det = psana.Detector(detectorName, ds.env())
run = ds.runs().next()
times = run.times()
evt = run.event(times[evtNumber])

nda = det.calib(evt)
data = det.image(evt,nda)

pixelIndex = np.arange(1,nda.size+1)
pixelIndex[0] = np.max(pixelIndex)
pixelIndex[-1] = np.min(pixelIndex)
pixelIndex.reshape(nda.shape)
pixelIndex = det.image(evt,pixelIndex)

###

## Add path to library (just for examples; you do not need this)
print "Note: The images are drawn with pyqtgraph. A matplotlib display will render pixels differently."
app = QtGui.QApplication([])

## Create window with ImageView widget

win = QtGui.QMainWindow()
area = DockArea()
win.resize(1300,1300)
win.setCentralWidget(area)

win.setWindowTitle('ImageView')
d1 = Dock("Image Panel1", size=(800, 800))
d2 = Dock("Image Panel2", size=(800, 800))
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