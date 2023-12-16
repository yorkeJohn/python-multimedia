'''
Word frequencies from text data

Note: assumes that 'gutenberg' and 'book' have been downloaded (see https://www.nltk.org/data.html)
'''
from nltk import word_tokenize
from nltk.book import * 
from nltk.corpus import stopwords
from nltk.probability import FreqDist

import random
import time
import re

texts = (text1, text2, text3, text4, text5, text6, text7, text8, text9)
text = random.choice(texts)

text_data = text.generate(2000, random_seed=time.time())

tokens = word_tokenize(text_data)
stop_words = stopwords.words('english')
tokens = [t for t in tokens if re.match(r'[a-zA-Z\']', t) and t.lower() not in stop_words]
print(tokens)

freq_dist = FreqDist(t.lower() for t in tokens)
top_word, top_word_freq = freq_dist.most_common(1)[0]

print(f'Text used: {text}')
print(f'{top_word} appeared most often ({top_word_freq} times)')
