from nltk.translate.bleu_score import sentence_bleu
import numpy as np
import csv

with open('qna.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

data_array = np.array(data)
data_split = np.split(data_array,1)

print(data_split)
"""
reference = [
    'this is a dog'.split(),
    'it is dog'.split(),
    'dog it is'.split(),
    'a dog, it is'.split() 
]

candidate = 'cara daftar akun'.split()

print('Individual 1-gram: %f' % sentence_bleu(reference, candidate, weights=(1, 0, 0, 0)))
print('Individual 2-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 1, 0, 0)))
print('Individual 3-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 0, 1, 0)))
print('Individual 4-gram: %f' % sentence_bleu(reference, candidate, weights=(0, 0, 0, 1)))

score = sentence_bleu(reference, candidate, weights=(0.25, 0.25, 0.25, 0.25))
print(score)
"""