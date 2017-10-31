import pandas as pd
import os.path as path
import os
import ast

def read_csv(dirname, file_number):
	text = []
	token = []

	df = pd.read_csv(path.join(dirname, str(file_number)+'.csv'))
	# print(path.join(dirname, str(i)+'.csv'))
	text.extend(df['text'].tolist())
	for t in df['token'].tolist():
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

def replace_quotation_annotation(str):
	return str.replace("`", "'").replace('"', "'").replace("``", "'").replace("''", "'")

def find_wrong_token(generated_texts, generated_tokens, test_texts, test_tokens, writer):
    if (len(generated_texts) != len(test_texts)):
    	print("Err: Length of two datasets differ!")
    	print(len(generated_texts), len(test_texts))
    	exit()

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

    		generated_processed = replace_quotation_annotation("".join(generated_token[start_generated:i_generated+1]).replace(" ", ""))
    		test_processed = replace_quotation_annotation("".join(test_token[start_test:i_test+1]).replace(" ", ""))
    		# print(generated_processed)
    		# print(test_processed)
    		if generated_processed == test_processed:
    		 # or (join(generated_token[start_generated:i_generated+1]) == " ".join(test_token[start_test:i_test+1])):
    			end_generated = i_generated
    			end_test = i_test
    			# if ((end_generated - start_generated) > 0) or ((end_test - start_test) > 0)  :
    			if (end_generated - start_generated) != (end_test - start_test):

    				#NOT MATCH
    				wrong += end_test - start_test + 1
    				print("Wrong tokens: ")
    				writer.write("Wrong tokens: \n")
    				print("Generated: " + str(generated_token[start_generated:i_generated+1]))
    				print("Generated: " + str(generated_token))
    				writer.write("Generated: " + str(generated_token[start_generated:i_generated+1]) + '\n')
    				print("Test: " + str(test_token[start_test:i_test+1]))
    				print("Test: " + str(test_token))
    				writer.write("Test: " + str(test_token[start_test:i_test+1]) + '\n')
    				print()
    				writer.write('\n')

    			i_generated += 1
    			i_test += 1
    			start_generated = end_generated = i_generated
    			start_test = end_test = i_test
    			continue
    		else:
    			if (i_test+1 >= len(test_token)) or (i_generated+1 >= len(generated_token)):
    				break

    			# if len(generated_processed) > len(test_processed):
    			if generated_processed.find(test_processed) != -1:
    				i_test += 1
    			# elif len(generated_processed) < len(test_processed):
    			elif test_processed.find(generated_processed) != -1:
    				i_generated += 1
    			else:
    				wrong += i_test - start_test + 1
    				print("Wrong tokens: ")
    				writer.write("Wrong tokens: \n")
    				print("Generated: " + str(generated_token[start_generated:i_generated+1]))
    				print("Generated: " + str(generated_token))
    				writer.write("Generated: " + str(generated_token[start_generated:i_generated+1]) + '\n')
    				print("Test: " + str(test_token[start_test:i_test+1]))
    				print("Test: " + str(test_token))
    				writer.write("Test: " + str(test_token[start_test:i_test+1]) + '\n')
    				print()
    				writer.write('\n')
    				i_generated += 1
    				i_test += 1
    				start_generated = end_generated = i_generated
    				start_test = end_test = i_test
    				continue
    return wrong


# mian

writer = open("./test_report2.txt", 'w')
total_wrong = 0
total_token_number = 0
for i in range(100):
    print(str(i) + "th file")
    generated_directory = path.abspath('../processed_data/tokenizer_result/generated_100_result_v2/')
    generated_texts, generated_tokens = read_csv(generated_directory, i)

    test_directory = path.abspath('../processed_data/annotations_hand_label/')
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
