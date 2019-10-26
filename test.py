import re
import string
import nltk
from nltk.corpus import stopwords

stops = set(stopwords.words('english'))
words = []

for sample in stops:
    words.append(sample)
    if len(words) >=150 :
        break

print(words)