'''
Manipulating MIDI audio data
'''
import pretty_midi as pm
from scipy.io import wavfile
import numpy as np
from copy import deepcopy

sr: int = 44100

def write_wav(filename: str, track: pm.PrettyMIDI | pm.Instrument) -> None:
  wav: np.ndarray = track.synthesize(sr)
  wavfile.write(f'{filename}.wav', sr, np.asarray(wav, dtype=np.float32))

def pitch_up(note: pm.Note) -> pm.Note:
  note.pitch += 12
  return note

def update_inst(inst: pm.Instrument) -> pm.Instrument:
  if not inst.is_drum:
    inst.notes = [pitch_up(note) for note in inst.notes]
  return inst

# read in some midi data
midi: pm.PrettyMIDI = pm.PrettyMIDI('ICantGiveYouAnythingButLove.mid')
write_wav('audio_master', midi)

midi.instruments = [update_inst(inst) for inst in midi.instruments]

# note that the drum track does not save correctly - issue with pretty_midi libray
for inst in midi.instruments:
  track = deepcopy(midi)
  track.instruments = [inst]
  write_wav(inst.name.strip(), track)

write_wav('combined', midi)