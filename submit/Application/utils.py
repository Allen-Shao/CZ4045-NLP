# -*- coding: utf-8 -*-
import os
import codecs
from collections import Counter
from six.moves import cPickle
import numpy as np


class TextLoader():
    def __init__(self, data_dir, batch_size, seq_length, encoding=None):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length

        input_file = os.path.join(data_dir, "input.txt")
        vocab_file = os.path.join(data_dir, "vocab.pkl")
        tensor_file = os.path.join(data_dir, "data.npy")

        print("reading text file")

        with codecs.open(input_file, "r", encoding=encoding) as f:
            data = f.read()

        # Optional text cleaning or make them lower case, etc.
        # data = self.clean_str(data)
        x_text = data.split()

        word_counts = Counter(x_text)
        # Mapping from index to word
        vocabulary_inv = [x[0] for x in word_counts.most_common()]
        self.words = list(sorted(vocabulary_inv))
        # Mapping from word to index
        self.vocab = {x: i for i, x in enumerate(vocabulary_inv)}

        self.vocab_size = len(self.words)

        with open(vocab_file, 'wb') as f:
            cPickle.dump(self.words, f)

        # The same operation like this [self.vocab[word] for word in x_text]
        # index of words as our basic data
        self.tensor = np.array(list(map(self.vocab.get, x_text)))
        # Save the data to data.npy
        np.save(tensor_file, self.tensor)

        self.num_batches = int(self.tensor.size / (self.batch_size *
                                                   self.seq_length))
        if self.num_batches == 0:
            assert False, "Not enough data. Make seq_length and batch_size small."

        self.tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length]
        xdata = self.tensor
        ydata = np.copy(self.tensor)

        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]
        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1), self.num_batches, 1)

        self.reset_batch_pointer()

    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0


# method for generating text
def generate_text(model, length, vocab_size, ix_to_char):
    # starting with random character
    ix = [np.random.randint(vocab_size)]
    y_char = [ix_to_char[ix[-1]]]
    X = np.zeros((1, length, vocab_size))
    for i in range(length):
        # appending the last predicted character to sequence
        X[0, i, :][ix[-1]] = 1
        print(ix_to_char[ix[-1]], end="")
        ix = np.argmax(model.predict(X[:, :i + 1, :])[0], 1)
        y_char.append(ix_to_char[ix[-1]])
    return ('').join(y_char)


# method for preparing the training data
def load_data(data_dir, seq_length):
    data = open(data_dir, 'r', encoding='utf-8').read()
    chars = list(set(data))
    VOCAB_SIZE = len(chars)

    print('Data length: {} characters'.format(len(data)))
    print('Vocabulary size: {} characters'.format(VOCAB_SIZE))

    ix_to_char = {ix: char for ix, char in enumerate(chars)}
    char_to_ix = {char: ix for ix, char in enumerate(chars)}

    X = np.zeros((int((len(data) / seq_length)), seq_length, VOCAB_SIZE))
    y = np.zeros((int((len(data) / seq_length)), seq_length, VOCAB_SIZE))
    for i in range(0, int(len(data) / seq_length)):
        X_sequence = data[i * seq_length:(i + 1) * seq_length]
        X_sequence_ix = [char_to_ix[value] for value in X_sequence]
        input_sequence = np.zeros((seq_length, VOCAB_SIZE))
        for j in range(seq_length):
            input_sequence[j][X_sequence_ix[j]] = 1.
            X[i] = input_sequence

        y_sequence = data[i * seq_length + 1:(i + 1) * seq_length + 1]
        y_sequence_ix = [char_to_ix[value] for value in y_sequence]
        target_sequence = np.zeros((seq_length, VOCAB_SIZE))
        for j in range(seq_length):
            target_sequence[j][y_sequence_ix[j]] = 1.
            y[i] = target_sequence
    return X, y, VOCAB_SIZE, ix_to_char
