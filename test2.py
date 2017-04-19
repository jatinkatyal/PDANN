from __future__ import print_function, division, unicode_literals
import wave, matplotlib.pyplot as plt
import numpy as np


lowpass = 21 # Remove lower frequencies.
highpass = 9000 # Remove higher frequencies.
# compatibility with Python 3
wr = wave.open('bass.wav', 'r')
sz = wr.getframerate() # Read and process 1 second at a time.
c = int(wr.getnframes()/sz) # whole file
for num in range(c):
    print('Processing {}/{} s'.format(num+1, c))
    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
    left, right = da[0::2], da[1::2] # left and right channel
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)
    lf[:lowpass], rf[:lowpass] = 0, 0 # low pass filter
    lf[55:66], rf[55:66] = 0, 0 # line noise
    lf[highpass:], rf[highpass:] = 0,0 # high pass filter
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
    ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
    plt.figure(1)
    a = plt.subplot(211)
    r = 2**16/2
    a.set_ylim([-r, r])
    a.set_xlabel('time [s]')
    a.set_ylabel('sample value [-]')
    x = np.arange(wr.getframerate())/wr.getnframes()
    plt.plot(x, left)
    b = plt.subplot(212)
    b.set_xscale('log')
    b.set_xlabel('frequency [Hz]')
    b.set_ylabel('|amplitude|')
    plt.plot(abs(lf))
    plt.show()    
# Close the files.
wr.close()


#plt.savefig('sample-graph.png')