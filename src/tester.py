import pandas as pd 

def read_csv(filename):
	df = pd.read_csv(filename)
	return df['text'].tolist(), df['token'].tolist()
 

filename = “”
generated_texts, generated_tokens = read_csv(filename)

test_texts, test_tokens = read_csv(filename)