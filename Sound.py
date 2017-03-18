import wave, numpy, sounddevice, time
from PyQt4 import QtGui, QtCore

class Sound:
	def __init__(self,file=None):
		if file==None:
			file = QtGui.QFileDialog.getOpenFileName(None,"Open file")
		temp = wave.open(file,'r')
		QtCore.QTimer.singleShot(10,app.quit)
		app.exec_()
		self.rate = temp.getframerate()
		self.frames = temp.getnframes()
		self.channels = temp.getnchannels()
		data = numpy.fromstring(temp.readframes(self.frames),dtype=numpy.int16)
		self.data = numpy.transpose(numpy.array([data[0::2],data[1::2]]))
	def play(self):
		sounddevice.play(self.data,self.rate)
	def stop(self):
		sounddevice.stop()	

import sys
app = QtGui.QApplication(sys.argv)
mysound = Sound()
mysound.play()
time.sleep(5)
mysound.stop()