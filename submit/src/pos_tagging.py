
# coding: utf-8

import nltk
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('sentence', type=str, help='input sentence for POS tagging')
	args = parser.parse_args()

	text = nltk.word_tokenize(args.sentence)
	print(nltk.pos_tag(text))

if __name__ == '__main__':
    main()
