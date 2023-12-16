'''
Generating text from audio using natural language processing

Note: On my machine, it took about 5 minutes to generate the chunks and corpora
The code only generates them if they have not already been saved
'''
from typing import List, Tuple, Dict
from os import mkdir, path, listdir
from natsort import natsorted
from tabulate import tabulate

from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import huffman

# Functions ===================================================================

def create_dir(dirname: str) -> None:
  if not path.exists(dirname):
    mkdir(dirname)

def dir_cached(dirname: str) -> bool:
  return path.exists(dirname) and listdir(dirname)

def list_dir_sorted(dirname: str) -> List[str]:
  return natsorted(listdir(dirname))

def chunk_audio(filename: str, chunk_dir: str) -> None:
  audio_data = AudioSegment.from_file(filename)
  chunks = split_on_silence(audio_data, silence_thresh=audio_data.dBFS - 20)
  create_dir(chunk_dir)
  for i, chunk in enumerate(chunks):
    chunk.export(path.join(chunk_dir, f'chunk_{i}.wav'), format='wav')

def transcribe_audio(chunk_dir: str, text_dir: str) -> None:
  create_dir(text_dir)
  r = sr.Recognizer()
  for i, filename in enumerate(list_dir_sorted(chunk_dir)):
    with sr.AudioFile(path.join(chunk_dir, filename)) as source:
      audio = r.record(source)
      text = r.recognize_google(audio)
      with open(path.join(text_dir, f'text_{i}.txt'), 'w') as dest:
        dest.write(text)

Corpus = Tuple[str, List[str]]

def get_corpora(text_dir: str) -> List[Corpus]:
  corpora = []
  for filename in list_dir_sorted(text_dir):
    with open(path.join(text_dir, filename)) as text:
      name, _ = path.splitext(filename)
      corpora.append((name, text.read().lower()))
  return corpora

BoW = Dict[str, int]

def get_bow(corpora: List[Corpus]) -> BoW:
  excluded = set(stopwords.words('english'))
  words = [w for _, text in corpora for w in text.split() if w not in excluded]
  freq_dist = FreqDist(words)
  return {word: count for word, count in freq_dist.items() if count >= 5}

# Main code ===================================================================

chunk_dir = 'chunks'
if not dir_cached(chunk_dir):
  chunk_audio('alice_in_wonderlandch01.mp3', chunk_dir)

text_dir = 'text'
if not dir_cached(text_dir):
  transcribe_audio(chunk_dir, text_dir)

# create the corpora, BoW, and huffman encoding
corpora = get_corpora(text_dir)
bow = get_bow(corpora)
encoding = {code: word for word, code in huffman.codebook(bow.items()).items()}

# print out the encoding table
table = [[word, code, bow[word]] for code, word in encoding.items()]
sorted_table = sorted(table, key=lambda x: (x[2], x[1]), reverse=True)
print(tabulate(sorted_table, headers=['Word', 'Code', 'Freq'], tablefmt='simple_outline'))

# search for a code
word = encoding[input('Enter a code to select a word: ')]
print(f'\n"{word}" is found in the following text:\n')

for name, text in corpora:
  if word in text.split():
    print(f'{name}: {text}')