'''
Decreasing the amplidude of some audio
'''
from scipy.io import wavfile
import matplotlib.pyplot as plt

# read wav file and plot the data
sr, data = wavfile.read('piano.wav')

plt.plot(data)
plt.show()

# decrease amplitude for seconds 3 to 5
start_time, end_time = 3, 5
start, end = int(start_time * sr), int((end_time + 1) * sr)
data[start:end] = data[start:end] * 0.1

plt.plot(data)
plt.show()

wavfile.write('decreased.wav', sr, data)
