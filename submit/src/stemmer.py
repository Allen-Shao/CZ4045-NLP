import operator
from re import match as re_match
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import sys
import argparse
import os

'''
1. From the dataset, identify the top-20 most frequent words
(excluding the stop words) before and after performing stemming.

2. For each of the top-20 most frequent stems,
list their original words from which the stem is reached
'''
# input arguments: selected_answer.csv   selected_questions.csv
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selected_questions", type=str, default='./selected_questions.csv',
                      help="the csv file containing all the selected questions")
    parser.add_argument("--selected_answers", type=str, default='./selected_answers.csv',
                      help="the csv file containing all the selected answers")
    parser.add_argument("--output_directory", type=str, default='./', 
                      help='the output directory to store stemming result')
    args = parser.parse_args()
    stemming(args)


def stemming(args):
    ans_path = os.path.abspath(args.selected_answers)
    qns_path = os.path.abspath(args.selected_questions)
    output = os.path.join(os.path.abspath(args.output_directory), 'stemmer_result.txt')

    tokenizer = RegexpTokenizer(r'\w+')
    stemmer = SnowballStemmer("english")

    ans = pd.read_csv(ans_path)
    qns = pd.read_csv(qns_path)

    posts = pd.concat([ans,qns])['Body']

    i = 0
    word_frequency = {}
    stem_frequency = {}
    stem_origin = {}
    stems = []
    for post in posts:
        # change all to lower case
        tokens = map(str.lower,tokenizer.tokenize(post))
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

    writer = open(output, "w")
    writer.write("top_20_words\n")
    writer.write(str(top_20_words))
    writer.write("\n")
    writer.write("top_20_stems\n")
    writer.write(str(top_20_stems))
    writer.write("\n")
    writer.write("top_20_stem_origins\n")
    writer.write(str(top_20_stem_origins))
    writer.close()
    print("The stemming result is stored as stemming_result.txt")


if __name__ == '__main__':
    main()