import pandas as pd 
import os.path as path
import os
import ast


def read_csv(dirname):
	text = []
	token = []
	for i in range(100):
		i=99
		df = pd.read_csv(path.join(dirname, str(i)+'.csv'))
		print(path.join(dirname, str(i)+'.csv'))
		text.extend(df['text'].tolist())
		print("\n".join(df['token'].tolist()))
		break
		for t in df['token'].tolist():
			t = t.replace("’", "'")
			t = t.replace("‘", "'")
			t = t.replace("“", '"')
			t = t.replace("”", '"')
			t = t.replace(":", ":")
			# start = t.find("[")
			# end = t.find("]")
			# while (end != -1):
			# 	last = end
			# 	end = t.find("]", end+1)
			# print(start, last)
			# t = t[start:last+1]
			try:
				token.extend(ast.literal_eval(t))
			except:
				print(t)
	return text, token
 

generated_directory = path.abspath('../processed_data/tokenizer_result/generated_100_result_v2/')
generated_texts, generated_tokens = read_csv(generated_directory)

test_directory = path.abspath('../processed_data/annotations_hand_label/')
test_texts, test_tokens = read_csv(test_directory)

print(test_tokens[0])

if (len(generated_texts) != len(test_texts)):
	print("Err: Length of two datasets differ!")
	exit()

for i in range(len(generated_texts)):
	# generated_text = generated_texts[i].strip('\n')
	# if (generated_text != test_texts[i]):
	# 	print("WARNING: generated and test text differ.")
	# 	print("Generated: \n"+generated_texts[i])
	# 	print("Test: \n"+test_texts[i])

	generated_token_i=0
	test_token_i=0