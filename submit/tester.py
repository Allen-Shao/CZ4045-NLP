import pandas as pd
import os.path as path
import ast
import argparse

def read_csv(dirname, file_number):
	text = []
	token = []

	df = pd.read_csv(path.join(dirname, str(file_number)+'.csv'), encoding='utf-8')
	text.extend(df['text'].tolist())
	for t in df['token'].tolist():
		# annotation typo
		t = t.replace("’", "'")
		t = t.replace("‘", "'")
		t = t.replace("“", '"')
		t = t.replace("”", '"')
		t = t.replace("''s'", "\"'s\"")# Special Handle
		try:
			token.append(ast.literal_eval(t))
		except:
			print("ERR: "+ str(i)+ " " + t)
	return text, token

def find_wrong_token(generated_texts, generated_tokens, test_texts, test_tokens, writer):
    if (len(generated_texts) != len(test_texts)):
    	print("Err: Length of two datasets differ!")
    	print(len(generated_texts), len(test_texts))
    	exit()
	# count number of mistake
    wrong = 0

    for i in range(len(generated_texts)):

    	generated_text = generated_texts[i]
    	test_text = test_texts[i]

    	generated_token = generated_tokens[i]
    	test_token = test_tokens[i]

    	if (i==459):
    		continue

    	i_generated = i_test = 0
    	start_generated = end_generated = 0
    	start_test = end_test = 0

    	while (i_generated < len(generated_token) or i_test < len(test_token)):

    		generated_processed = "".join(generated_token[start_generated:i_generated+1]).replace(" ", "")
    		test_processed = "".join(test_token[start_test:i_test+1]).replace(" ", "")
    		if generated_processed == test_processed:
    			end_generated = i_generated
    			end_test = i_test
    			if (end_generated - start_generated) != (end_test - start_test):

    				#NOT MATCH
    				wrong += end_test - start_test + 1
    				writer.write("Wrong tokens: \n")
    				writer.write("Generated: " + str(generated_token[start_generated:i_generated+1]) + '\n')
    				writer.write("Test: " + str(test_token[start_test:i_test+1]) + '\n')
    				writer.write('\n')

    			i_generated += 1
    			i_test += 1
    			start_generated = end_generated = i_generated
    			start_test = end_test = i_test
    			continue
    		else:
    			if (i_test+1 >= len(test_token)) or (i_generated+1 >= len(generated_token)):
    				break

    			if generated_processed.find(test_processed) != -1:
    				i_test += 1
    			elif test_processed.find(generated_processed) != -1:
    				i_generated += 1
    			else:
    				wrong += i_test - start_test + 1
    				writer.write("Wrong tokens: \n")
    				writer.write("Generated: " + str(generated_token[start_generated:i_generated+1]) + '\n')
    				writer.write("Test: " + str(test_token[start_test:i_test+1]) + '\n')
    				writer.write('\n')
    				i_generated += 1
    				i_test += 1
    				start_generated = end_generated = i_generated
    				start_test = end_test = i_test
    				continue
    return wrong


# mian
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--generated_results', type=str, default='./',
					help='the directory where all the generated csv file are stored')
	parser.add_argument('--annotated_results', type=str, default='./',
					help='the directory where all the annotated csv file are stored')
	parser.add_argument('--output_directory',  type=str, default='./',
					help='the output directory to store test report')
	args = parser.parse_args()

	writer = open(path.join(path.abspath(args.output_directory), 'test_report.txt'), 'w', encoding='utf-8')

	total_wrong = 0
	total_token_number = 0
	for i in range(100):
	    generated_directory = path.abspath(args.generated_results)
	    generated_texts, generated_tokens = read_csv(generated_directory, i)

	    test_directory = path.abspath(args.annotated_results)
	    test_texts, test_tokens = read_csv(test_directory, i)
	    total_token_number += sum(len(t) for t in test_tokens)
	    total_wrong += find_wrong_token(generated_texts, generated_tokens, test_texts, test_tokens, writer)

	print("Total token number: ", end="")
	writer.write("Total token number: \n")
	print(total_token_number)
	writer.write(str(total_token_number) + '\n')
	print("Total wront token number: ", end="")
	writer.write("Total wrong token number: \n")
	print(total_wrong)
	writer.write(str(total_wrong))

	writer.close()

if __name__ == '__main__':
	main()
