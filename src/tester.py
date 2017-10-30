import pandas as pd
import os.path as path
import os
import ast


def read_csv(dirname):
	text = []
	token = []
	for i in range(100):
		df = pd.read_csv(path.join(dirname, str(i)+'.csv'))
		# print(path.join(dirname, str(i)+'.csv'))
		text.extend(df['text'].tolist())
		for t in df['token'].tolist():
			t = t.replace("’", "'")
			t = t.replace("‘", "'")
			t = t.replace("“", '"')
			t = t.replace("”", '"')

			t = t.replace("''s'", "\"'s\"")# Special Handle
			# start = t.find("[")
			# end = t.find("]")
			# while (end != -1):
			# 	last = end
			# 	end = t.find("]", end+1)
			# print(start, last)
			# t = t[start:last+1]
			try:
				token.append(ast.literal_eval(t))
			except:
				print("ERR: "+ str(i)+ " " + t)
	return text, token

def replace_quotation_annotation(str):
	return str.replace("`", "'").replace('"', "'").replace("``", "'").replace("''", "'")



generated_directory = path.abspath('../processed_data/tokenizer_result/generated_100_result_v2/')
generated_texts, generated_tokens = read_csv(generated_directory)

test_directory = path.abspath('../processed_data/annotations_hand_label/')
test_texts, test_tokens = read_csv(test_directory)


if (len(generated_texts) != len(test_texts)):
	print("Err: Length of two datasets differ!")
	print(len(generated_texts), len(test_texts))
	exit()

wrong = 0
writer = open("./test_report2.txt", 'w')

for i in range(len(generated_texts)):
	# generated_text = generated_texts[i].strip('\n')
	# if (generated_text != test_texts[i]):
	# 	print("WARNING: generated and test text differ.")
	# 	print("Generated: \n"+generated_texts[i])
	# 	print("Test: \n"+test_texts[i])
	# i=459

	generated_text = generated_texts[i]
	test_text = test_texts[i]

	generated_token = generated_tokens[i]
	test_token = test_tokens[i]
	
	if (i==459):
		continue

	# print(i)
	# print(generated_text)
	# print(generated_token)
	# print(test_text)
	# print(test_token)

	i_generated = i_test = 0
	start_generated = end_generated = 0
	start_test = end_test = 0

	while (i_generated < len(generated_token) or i_test < len(test_token)):
		# if generated_token[i_generated] == test_token[i_test]:
		# print(i_generated, i_test)
		# input()
		generated_processed = replace_quotation_annotation("".join(generated_token[start_generated:i_generated+1]).replace(" ", ""))
		test_processed = replace_quotation_annotation("".join(test_token[start_test:i_test+1]).replace(" ", ""))
		# print(generated_processed)
		# print(test_processed)
		if generated_processed == test_processed:
		 # or (join(generated_token[start_generated:i_generated+1]) == " ".join(test_token[start_test:i_test+1])):
			end_generated = i_generated
			end_test = i_test
			if ((end_generated - start_generated) > 0) or ((end_test - start_test) > 0)  :
				#NOT MATCH
				wrong += end_test - start_test + 1
				# print("Wrong tokens: ")
				writer.write("Wrong tokens: \n")
				# print("Generated: " + str(generated_token[start_generated:i_generated+1]))
				writer.write("Generated: " + str(generated_token[start_generated:i_generated+1]) + '\n')
				# print("Test: " + str(test_token[start_test:i_test+1]))
				writer.write("Test: " + str(test_token[start_test:i_test+1]) + '\n')
				# print()
				writer.write('\n')

			i_generated += 1
			i_test += 1
			start_generated = end_generated = i_generated
			start_test = end_test = i_test
			continue
		else:
			if (i_test+1 >= len(test_token)) or (i_generated+1 >= len(generated_token)):
				break

			if generated_token[i_generated+1] == test_token[i_test+1]:
				#WRONG TOKEN
				# print(generated_token[i_generated+1], test_token[i_test+1])
				wrong += i_test - start_test + 1
				# print("Wrong tokens: ")
				writer.write("Wrong tokens: \n")
				# print("Generated: " + str(generated_token[start_generated:i_generated+1]))
				writer.write("Generated: " + str(generated_token[start_generated:i_generated+1]) + '\n')
				# print("Test: " + str(test_token[start_test:i_test+1]))
				writer.write("Test: " + str(test_token[start_test:i_test+1]) + '\n')
				# print()
				writer.write('\n')
				i_generated += 1
				i_test += 1
				start_generated = end_generated = i_generated
				start_test = end_test = i_test
				continue

			if len(generated_processed) > len(test_processed):
				i_test += 1
			elif len(generated_processed) < len(test_processed):
				i_generated += 1
			# else:
				# wrong += i_test - start_test + 1
				# print("Wrong tokens: ")
				# print("Generated: " + str(generated_token[start_generated:i_generated+1]))
				# print("Test: " + str(test_token[start_test:i_test+1]))
				# print()
				# i_generated += 1
				# i_test += 1
				# start_generated = end_generated = i_generated
				# start_test = end_test = i_test

			# else:
				#TODO: SIMPLY WRONG
print("Total token number: ", end="")
writer.write("Total token number: \n")
print(sum([len(a) for a in test_tokens]))
writer.write(str(sum([len(a) for a in test_tokens])) + '\n')
print("Total wront token number: ", end="")
writer.write("Total wront token number: \n")
print(wrong)

writer.close()
