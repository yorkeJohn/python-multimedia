'''
Generating audio from chords
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

sr = 44100 # sample rate (Hz)
duration = 2  # duration (s)
t = np.linspace(0, duration, int(sr * duration), endpoint=False)

def gen_audio(freq: list) -> np.ndarray:
  return np.sin(2 * np.pi * np.outer(t, freq)).sum(axis=1)

def show_audio(data: np.ndarray) -> None:
  plt.plot(t[:int(0.05 * sr)], data[:int(0.05 * sr)])
  plt.show()

def write_audio(filename: str, data: np.ndarray) -> None:
  scale = np.iinfo(np.int16).max
  normalized = (data / np.max(np.abs(data)) * scale).astype(np.int16)
  wavfile.write(f'prog_3_{filename}.wav', sr, normalized)

def main(freq: list, suffix: str) -> None:
  data = gen_audio(freq)
  show_audio(data)
  write_audio(f'q1{suffix}', data)
  return data

# F4 A4 C5
freq_a = [349.228, 440, 523.25]
data_a = main(freq_a, 'a')

# E4 G4 Bb4 C#5
freq_b = [329.63, 391.995, 466.16, 554.36]
data_b = main(freq_b, 'b')

# F4 A4 D5
freq_c = [349.228, 440, 587.32]
data_c = main(freq_c, 'c')

# concatenated audio sequence
write_audio('sequence', np.concatenate((data_a, data_b, data_c), axis=0))