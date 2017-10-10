
# coding: utf-8

# In[ ]:

import time
import pickle
import pandas as pd
import os
import sys


# In[ ]:

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


# In[ ]:

class Question:
	def __init__(self, post_id, title, body, accepted_answer, answer_count):
		self.PostId = post_id
		self.Title = title if title else ""
		self.Body = body if body else ""
		self.AcceptedAnswerId = int(accepted_answer) if accepted_answer else ""
		self.AnswerCount = int(answer_count) if answer_count else ""

class Answer:
	def __init__(self, post_id, body, parent_id):
		self.PostId = post_id
		self.Body = body if body else ""
		self.ParentId = int(parent_id) if parent_id else ""


total_go_threads_len = 0

questions = [] # Keep all the questions in list, later convert to DataFrame

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
					total_go_threads_len = total_go_threads_len + 1


			if (post_type_id == 2): # Answer
				body = key_content(line, "Body")
				parent_id = key_content(line, "ParentId")
				answer = Answer(cur_id, body, parent_id)

				answers.append(answer.__dict__)

		except:
			print(line)
			print("sth wrong, but continue: "+ sys.exc_info()[0])
			continue




question_df = pd.DataFrame(data = questions, columns=['PostId', 'Body', 'AnswerCount', 'AcceptedAnswerId', 'AnswerIds'])
answer_df = pd.DataFrame(data = answers, columns=['PostId', 'Body', 'ParentId'])

question_df.to_csv("questions.csv")
answer_df.to_csv("answers.csv")


print("Total Go Threads: "+ str(total_go_threads_len))
print("Program finished")





