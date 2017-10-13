import csv
import operator
from re import match as re_match
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

'''
1. From the dataset, identify the top-20 most frequent words
(excluding the stop words) before and after performing stemming.

2. For each of the top-20 most frequent stems,
list their original words from which the stem is reached
'''

tokenizer = RegexpTokenizer(r'\w+')
stemmer = SnowballStemmer("english")

try:
    with open('../processed_data/answers.csv', 'r') as ansfile:
        reader = csv.reader(ansfile, delimiter=',')
        # skip header
        next(reader, None)
        i = 0
        word_frequency = {}
        stem_frequency = {}
        stem_origin = {}
        stems = []
        for answer in reader:
            answer_body = answer[2]
            # change all to lower case
            tokens = map(str.lower,tokenizer.tokenize(answer_body))
            # remove stop words and numbers
            filtered_tokens = [token for token in tokens 
                               if token not in stopwords.words('english') 
                               and re_match(r'[-]?\d[\d,]*[\.]?[\d{2}]*', token) is None]
            
            for token in filtered_tokens:
                # calculate word frequency
                if token in word_frequency:
                    word_frequency[token] += 1
                else:
                    word_frequency[token] = 1

                stem = stemmer.stem(token)
                stems.append(stem)
                # preserve the original word for stem
                if stem in stem_origin:
                    stem_origin[stem].add(token)
                else:
                    stem_origin[stem] = set([token])

            # find the top 20 frequently appearing words
            top_20_words = [word_f_pair[0] for word_f_pair in 
                                reversed(sorted(word_frequency.items(), key=operator.itemgetter(1))[-20:])]

            # find the top 20 frequently apearing stems
            for stem in stems:
                if stem in stem_frequency:
                    stem_frequency[stem] += 1
                else:
                    stem_frequency[stem] = 1
            top_20_stems = [stem_f_pair[0] for stem_f_pair in 
                                reversed(sorted(stem_frequency.items(), key=operator.itemgetter(1))[-20:])]

            # for each stem in top-20 list, get the original words
            top_20_stem_origins = {stem: stem_origin[stem] for stem in top_20_stems}
    
except KeyboardInterrupt:
    print("keyboard interrupt")

finally:
    print("check result")
    print("top_20_words")
    print(top_20_words)
    print("top_20_stems")
    print(top_20_stems)
    print("top_20_stem_origins")
    print(top_20_stem_origins)
    
