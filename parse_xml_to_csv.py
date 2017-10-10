
# coding: utf-8


import pandas as pd
import os
import sys
import html, re

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


def dump_data():

	global questions, answers

	question_df = pd.DataFrame(data = questions, columns=['PostId', 'Body', 'Title', 'AnswerCount', 'AcceptedAnswerId', 'AnswerIds'])
	answer_df = pd.DataFrame(data = answers, columns=['PostId', 'Body', 'ParentId'])

	questions = []
	answers = []

	question_df.to_csv("questions.csv")
	answer_df.to_csv("answers.csv")


# Main
questions_count = 0
questions = [] # Keep all the questions in list, later convert to DataFrame
question_ids = [] # Keep track of question id for convenience
answers = [] # Keep all the answers in list, later convert to DataFrame

with open("./Posts.xml", "r") as f:
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
				if ("&lt;go&gt" in tags):  # Golang thread
					# Extract Info
					title = key_content(line, "Title")
					body = key_content(line, "Body")
					accept = key_content(line, "AcceptedAnswerId")
					answer_count = key_content(line, "AnswerCount")
					question = Question(cur_id, title, body, accept, answer_count)
					

					questions.append(question.__dict__)
					question_ids.append(cur_id)
					questions_count = questions_count + 1


			if (post_type_id == 2): # Answer
				parent_id = key_content(line, "ParentId")
				if parent_id and (int(parent_id) in question_ids):
					body = key_content(line, "Body")
					answer = Answer(cur_id, body, parent_id)
					answers.append(answer.__dict__)

			# CheckPoint
			if questions_count == 100:
				print("1000 questions collected.")
				questions_count = 0
				break
				# if (questions_count % 5000 == 0):
				# 	dump_data(questions_count // 5000)
				# 	print("5000 ")
		except KeyboardInterrupt:
			print(str(questions_count) + " questions collected.")
			dump_data()
		except:
			print(line)
			print("sth wrong, but continue: ", sys.exc_info()[0])
			continue


dump_data()

print("Program finished")





