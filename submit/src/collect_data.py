
# coding: utf-8
import pandas as pd
import os
import os.path as path
import sys
import html, re

import argparse

code_beginning = '&lt;code&gt;'
code_ending = '&lt;/code&gt;'

class Code():
	def __init__(id, code):
		self.PostId = id
		self.Code = code

class Question:
	def __init__(self, post_id, title, body, accepted_answer, answer_count):
		self.PostId = post_id
		self.Title = strip_html(title) if title else ""
		self.Body = strip_html(body) if body else ""
		self.AcceptedAnswerId = int(accepted_answer) if accepted_answer else ""
		self.AnswerCount = int(answer_count) if answer_count else ""

class Answer:
	def __init__(self, post_id, body, parent_id):
		self.PostId = post_id
		self.Body = strip_html(body) if body else ""
		self.ParentId = int(parent_id) if parent_id else ""


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def find_code(line):
	start_indexs = [x + len(code_beginning) for x in list(find_all(line, code_beginning))]
	end_indexs = list(find_all(line, code_ending))
	codes = []
	for start, end in zip(start_indexs, end_indexs):
		codes.append(line[start:end])
	return codes



def key_content(line, key):

	if (key in line):
		start_index = line.index(key + '="')
		for index in range(start_index+len(key + '="'),len(line)):
			if line[index] == '"':
				end_index = index
				break
		return line[start_index + len(key + '="'): end_index]
	else:
		return False

def strip_html(content):
	return re.sub(r'<.*?>','',html.unescape(html.unescape(content)))  ## Unescape twice to make it cleaner.


def dump_data(output_directory):

	global questions, answers

	question_df = pd.DataFrame(data = questions, columns=['PostId', 'Title', 'Body', 'AnswerCount', 'AcceptedAnswerId'])
	answer_df = pd.DataFrame(data = answers, columns=['PostId', 'Body', 'ParentId'])
	code_df = pd.DataFrame(data = codes, columns=['PostId', 'Code'])

	questions = []
	answers = []
	codes = []

	question_df.to_csv(path.join(output_directory, "questions.csv"))
	answer_df.to_csv(path.join(output_directory, "answers.csv"))
	code_df.to_csv(path.join(output_directory, "code.csv"))


def collect_data(input_file, output_directory, target_tag):
	questions_count = 0
	questions = [] # Keep all the questions in list, later convert to DataFrame
	question_ids = [] # Keep track of question id for convenience
	answers = [] # Keep all the answers in list, later convert to DataFrame
	codes = []

	with open(input_file, "r") as f:
		print("Start to open the file")
		# skip the first 2 lines
		f.readline() # <?xml metadata>
		f.readline() # <posts>
		for line in f:
			try:
				# Check HasId
				cur_id = key_content(line, "Id")
				if (not cur_id):
					continue
				else:
					cur_id = int(cur_id)


				post_type_id = int(key_content(line, "PostTypeId"))

				if (post_type_id == 1): # Question
					tags = key_content(line, "Tags")
					if (("&lt;"+target_tag+"&gt") in tags):  # Golang thread
						# Extract Info
						title = key_content(line, "Title")
						body = key_content(line, "Body")
						accept = key_content(line, "AcceptedAnswerId")
						answer_count = key_content(line, "AnswerCount")
						if (answer_count < 1):
							continue
						question = Question(cur_id, title, body, accept, answer_count)
						if (code_beginning in body):
							code_list = find_code(body)
							for code in code_list:
								new_code_section = (cur_id, strip_html(code)) 
								codes.append(new_code_section)

						questions.append(question.__dict__)
						question_ids.append(cur_id)
						questions_count = questions_count + 1


				if (post_type_id == 2): # Answer
					parent_id = key_content(line, "ParentId")
					if parent_id and (int(parent_id) in question_ids):
						body = key_content(line, "Body")
						answer = Answer(cur_id, body, parent_id)
						answers.append(answer.__dict__)
						if (code_beginning in body):
							code_list = find_code(body)
							for code in code_list:
								new_code_section = (cur_id, strip_html(code)) 
								codes.append(new_code_section)

				# CheckPoint
				if questions_count == 1000:
					print("1000 questions collected.")
					questions_count = 0


			except KeyboardInterrupt:
				print(str(questions_count) + " questions collected.")
				dump_data(output_directory)
			except:
				print(line)
				print("sth wrong, but continue: ", sys.exc_info()[0])
				continue

	print(str(questions_count) + " questions collected.")
	dump_data(output_directory)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--input_xml', type=str, default='./Posts.xml',
					help='the xml file containing raw data')
	parser.add_argument('--output_directory', type=str, default='./csv',
					help='the output directory to store processed csv')
	parser.add_argument('--tag', type=str, default='go',
					help='the desired tag want to extract from xml file')
	args = parser.parse_args()
	collect_data(path.abspath(args.input_xml), path.abspath(args.output_directory), args.tag)

if __name__ == '__main__':
	main()
