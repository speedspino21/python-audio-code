# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 50

# open stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

# read some data
# play stream and find the frequency of each chunk
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    # write data out to the audio stream
    data = stream.read(CHUNK)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/2),\
                                         data))
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/CHUNK
        print ("The freq is %f Hz." % (thefreq))
    else:
        thefreq = which*RATE/CHUNK
        print ("The freq is %f Hz." % (thefreq))
    # read some more data
if data:
    stream.write(data)
stream.close()
p.terminate()