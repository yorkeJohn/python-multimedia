'''
Generating a bag of words from text data
'''
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

import matplotlib.pyplot as plt
import csv

with open('friends_ep624.txt', 'r', encoding='utf-8') as file:
  corpus = file.read()

tokens = word_tokenize(corpus)

with open('w_tokens.txt', 'w') as file:
  file.write('\n'.join(tokens))

names = ['monica', 'chandler', 'joey', 'richard', 'phoebe', 'ross', 'rachel', 'thompson', 'elizabeth']
non_words = ['n\'t', '\'s', '\'re', '\'m', 'na', 'gon']
excluded = set(stopwords.words('english')).union(names).union(non_words)

tokens = [t for t in tokens if t.isalpha() and t.lower() not in excluded]

# bar graph
freq_dist = FreqDist(t.lower() for t in tokens)
top_20 = freq_dist.most_common(20)
words, freqs = zip(*top_20)

plt.bar(words, freqs)
plt.xticks(rotation=45)
plt.show()

# write csv
with open('BoW.csv', 'w', newline='') as file:
  csv_writer = csv.writer(file)
  for word, freq in sorted(freq_dist.items(), key=lambda i: i[1], reverse=True):
    csv_writer.writerow([word, freq])

# write lines
def write_lines(lines, filename):
  with open(f'{filename}.txt', 'w', encoding='utf-8') as file:
    for line in lines:
      file.write(line + '\n------\n')

lines = sent_tokenize(corpus)
write_lines(lines, 's_tokens')

lines_with_top_20 = [line for line in lines if any(t in line for t in set(t[0] for t in top_20))]
write_lines(lines_with_top_20, 'sentences_with_top20')
