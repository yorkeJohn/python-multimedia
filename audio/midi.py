'''
Generating MIDI audio data with chords and pitch bends
'''
import pretty_midi as pm
from scipy.io import wavfile
import numpy as np

def create_inst(program: int, name: str, data: tuple) -> pm.Instrument:
  instrument = pm.Instrument(program, False, name)
  instrument.notes = [pm.Note(90, pitch, start, end) for chord, start, end in data for pitch in chord]
  return instrument

steps = 512
bend_range = 4096
bend_step = bend_range / steps

def add_pitch_bend(instrument: pm.Instrument, start: float, end: float, reverse: bool=False) -> None:
  for t in range(steps + 1):
    bend_value = int(bend_range - t * bend_step) if reverse else int(t * bend_step)
    time = start + t * (end - start) / steps
    instrument.pitch_bends.append(pm.PitchBend(bend_value, time))

midi = pm.PrettyMIDI(initial_tempo=60)

# organ only
chords = [[60, 64, 67, 71], [61, 64, 67, 70], [62, 65, 69, 72], [63, 65, 67, 71]]
starts = [0, 2, 4, 6]
ends = [2, 4, 6, 10]
midi.instruments.append(create_inst(18, 'perc org', zip(chords, starts, ends)))

# trumpet with pitch bends
pitches = [72, 76, 81, 79, 81, 77, 76, 79]
chords = [[pitch] for pitch in pitches]
starts = [0.5, 1, 1.5, 2, 2.5, 4.5, 5, 5.5]
ends = [1, 1.5, 2, 2.5, 4.5, 5, 5.5, 10]

instrument = create_inst(60, 'mute tp', zip(chords, starts, ends))
add_pitch_bend(instrument, 2.7, 3.0)
add_pitch_bend(instrument, 3.7, 4.0, True)
midi.instruments.append(instrument)

midi.write('generated.mid')

sr = 44100
wavfile.write("generated.wav", sr, np.asarray(midi.synthesize(sr), dtype=np.float32))
