"""
import relevant modules for recording immediate voice,
storing audio as WAV file and plotting waveform of the WAV file
"""
#-----------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import wave
import pyaudio                  #using pyaudio means that the recording is stored as a bytes object
from fileinput import filename
import chunk
#--------------------------------------------------------------------------

chunk = 1024                        #set chunk size of 1024 samples per data frame
samp_format = pyaudio.paInt16       #used to store each audio sample as 16-bit value
fs = 44100                          #set sampling frequency at 44100 samples per second.High sampling frequency equals to quality audio file
duration = 20                       #set duration of recording at 20 seconds
filename = 'output1.wav'     #create file path to where the WAV file will be stored when created

#create interface to PortAudio I/O library
p = pyaudio.PyAudio()

print('Recording')

#Open a .Stream object to write the WAV file to.
# 'input=True' indicates sound will be recorded. 
stream = p.open(format=samp_format, channels=2, rate=fs,
                frames_per_buffer=chunk, input=True)

frames = []     #initialize array to store frames

#store audio stream data in chunks for 20 seconds
for i in range(0, int(fs/chunk * duration)):
    data = stream.read(chunk)
    frames.append(data)         #the data is stored in the array of frames

#stop and close the audio stream
stream.stop_stream()
stream.close()
p.terminate()       #terminate PortAudio Interface

print('Finished recording')

#save recorded data as WAV file
wf = wave.open(filename, 'w')  # initialize and create a 'wf' object which is used to create a WAV file at specified path.
wf.setnchannels(2)          #sets the number of channels for the WAV file, 2 channels is stereo, 1 channel is mono
wf.setsampwidth(p.get_sample_size(samp_format))     #set the sample width of the WAV file
wf.setframerate(fs)             #set the frame rate equal to sampling frequency
wf.writeframes(b''.join(frames))        #method used to join frames in the frame Array
wf.close()                          # close the "wf" object

"""
Plotting the Waveform of the WAV file created above
"""

#open the 'wf' object and perform read function to obtain information of the WAV file
wf = wave.open(filename, 'rb')      
#pyAudio creates bytes object which are used to store and play audio files.'rb' is used to read the bytes.
raw = wf.readframes(-1)
raw = np.frombuffer(raw, "int32")   
#----------------------------------------------------------------------------
num_frames = wf.getnframes()
print(num_frames)
#----------------------------------------------------------------------------
samp_Rate = wf.getframerate()
time = np.linspace(0, len(raw)/samp_Rate, num=len(raw))

fig = plt.figure()
axis = fig.add_subplot(111)
fig.suptitle('Waveform of WAV file')
axis.plot(time, raw, color='blue', linewidth=0.2)
plt.ylabel('Amplitude')
plt.show()
