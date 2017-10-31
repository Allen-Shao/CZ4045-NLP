
# coding: utf-8

# In[ ]:

# Irregular Tokens. Tokenize the dataset using your own tokenizer. Identify the top-20 most frequent
# tokens which are NOT standard English words (including their morphological forms).


# In[ ]:

import enchant
import pandas as pd
import os.path as path
import ast
import operator
import re


# In[ ]:

def sentence_has_irregular_token(sentence, irregular_token):
    for token in sentence:
        if token in irregular_token:
            return True
    return False


# In[ ]:

english_dictionary = enchant.Dict("en_US")


# In[ ]:

token_frequency_dic = {} # [token_content] : frequency
df = pd.DataFrame.from_csv('../processed_data/tokenizer_result/all/overall_results.csv')
generated_tokens = [ast.literal_eval(t) for t in df.tokens.tolist()]

for sentence in generated_tokens:
    for token in sentence:
        if token not in token_frequency_dic.keys():
            token_frequency_dic[token] = 1
        else:
            token_frequency_dic[token] += 1


# In[ ]:

top_20 = {}
floating_literal = r'''^\d+\.\d*(?:[eE][+-]\d+)?i?     
                | \d+[eE][+-]\d+i?               
                | \.\d+(?:[eE][+-]\d+)?i?$     
                '''
decimal_literal = r'^\d+$'
operators = r'^[%/\+\-\*\,;\$><!:\.\|&\^=\(\)\[\]\{\}\"\'\#\?_]+$'

for token, frequency in sorted(token_frequency_dic.items(), key=operator.itemgetter(1), reverse=True):
    if english_dictionary.check(token):
        continue
    if re.match(decimal_literal, token):
        # the token is an number
        continue
    if re.match(floating_literal, token):
        # the token is an float number
        continue
    if re.match(operators, token):
        # the token is an number
        continue
        
    if token in ["'d","'m", "'v", "'re", "'ve", "'s", "n't"]:
        # special english token
        continue
    top_20[token] = frequency
    if (len(top_20.keys()) == 20):
        break
#     print(token)
#     print(frequency)


# In[ ]:

write = "token:\tfrequency\n"
for token, frequency in sorted(top_20.items(), key=operator.itemgetter(1), reverse=True):
    write += str(token) + ':\t' + str(frequency) + '\n'
    
print(write)
with open('../Stats/top_20_irregular.txt', 'w') as f:
    f.write(write)


# In[ ]:

# POS Tagging. Randomly select 10 sentences from the dataset where each sentence contains at
# least one irregular token. Apply POS tagging on the sentences based on your own tokenization
# results. Show and discuss the tagging results.


# In[ ]:

import numpy as np


# In[ ]:

selected_10_sentences = []
np.random.shuffle(generated_tokens)
# for sentence in generated_tokens:
for sentence in generated_tokens:
    if sentence_has_irregular_token(sentence, top_20.keys()):
        selected_10_sentences.append(sentence)
    if (len(selected_10_sentences) == 10):
        break


# In[ ]:

import nltk
pos_tagging_10_sentences = []
for sentence in selected_10_sentences:
    pos_tagging_10_sentences.append(nltk.pos_tag(sentence))


# In[ ]:

with open('../Stats/postagging_10_sentences_result.txt', 'w') as f:
    for i in pos_tagging_10_sentences:
        f.write(str(i) + '\n')


# In[ ]:



