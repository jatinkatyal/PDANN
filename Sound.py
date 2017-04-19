import wave, numpy, sounddevice, time, sys, pyqtgraph as pg
from PyQt4 import QtGui, QtCore
from scipy.io.wavfile import write

class Sound:
	def browse(self):
		path = QtGui.QFileDialog.getOpenFileName(None,"Open file")
		self.file = wave.open(path,'r')
		QtCore.QTimer.singleShot(10,app.quit)
		app.exec_()
		print('Opening',path)
		self.rate = self.file.getframerate()
		self.frames = self.file.getnframes()
		self.channels = self.file.getnchannels()
		data = numpy.fromstring(self.file.readframes(self.frames),dtype=numpy.int16)
		self.data = numpy.array([data[0::2],data[1::2]])
		self.fourierData=numpy.array([numpy.fft.rfft(self.data[0]),numpy.fft.rfft(self.data)[1]])
		self.fourierData[0,:21]=0	# Low pass filter
		self.fourierData[0,9000:]=0 # High pass filter
	
	def record(self):
		self.rate = 44100
		self.channels = 2
		print('Enter recording time: ')
		time = input()
		self.frames = int(time) * self.rate
		print('recording now....')
		data = sounddevice.rec(self.frames,samplerate = self.rate,channels = self.channels,blocking = True)
		self.data = numpy.transpose(data)
		print('recording complete')
		write('input.wav', self.rate, data)
		self.fourierData=numpy.array([numpy.fft.rfft(self.data[0]),numpy.fft.rfft(self.data)[1]])
		self.fourierData[0,:21]=0	# Low pass filter
		self.fourierData[0,9000:]=0 # High pass filter

	def play(self):
		sounddevice.play(numpy.transpose(self.data),self.rate)

	def stop(self):
		sounddevice.stop()

	def plot(self):
		win = pg.GraphicsWindow()
		p1 = win.addPlot(title="Sound waveform",x=numpy.arange(self.frames)/self.rate, y=self.data[0])
		win.nextRow()
		p2 = win.addPlot(title="frequency", y=abs(self.fourierData[0]))

		if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
			QtGui.QApplication.instance().exec_()

	def exit(self):
		self.file.close()