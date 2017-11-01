
# coding: utf-8

import nltk
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('sentence', type=str, help='input sentence for postagging')
	args = parser.parse_args()

	text = nltk.word_tokenize(args.sentence)
	print(nltk.pos_tag(text))

