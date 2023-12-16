'''
Selectively removing tracks from MIDI audio data
'''
import pretty_midi as pm
from scipy.io import wavfile
import numpy as np

midi = pm.PrettyMIDI('WatermelonMan.mid')
print(f'Initial # of tracks: {len(midi.instruments)}')

instruments = [i for i in midi.instruments if not i.is_drum]
print(f'New # of tracks: {len(instruments)}')

midi.instruments = instruments
midi.write('no_drums.mid')

sr = 44100
duration = 60
wav = midi.synthesize(sr)[:int(sr * duration)]
wavfile.write("no_drums.wav", sr, np.asarray(wav, dtype=np.float32))
