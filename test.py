from sksound.sounds import Sound
import sounddevice, time
from scipy.io import wavefile

rate,data = wavefile.read('/home/jatin/Music/Animals.wav')
#mysound = Sound('/home/jatin/Music/Animals.wav')
#print(mysound.get_info())
#sounddevice.play(mysound.data,mysound.rate)
#time.sleep(5)
#sounddevice.stop()


from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
times=np.arange(len(mysound.data))/float(mysound.rate)
p1 = win.addPlot(x=times[:2000],y=mysound.data[:2000,0])

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()