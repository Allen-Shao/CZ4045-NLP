
# coding: utf-8

# In[ ]:

import time
import pickle
import pandas as pd
import os
import sys


# In[ ]:

base_file_name = "./go_thread_data/go_thread_data_"
file_count = 0
if (os.path.exists("./go_thread_data/")) is False:
#     if path not exists, make directory
	os.mkdir("./go_thread_data/")


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


# In[ ]:

# def save_go_thread_to_file(go_threads, file_name):
#     with open(file_name, 'wb') as output:
#         for thread in go_threads:
#             pickle.dump(thread, output, pickle.HIGHEST_PROTOCOL)


# In[ ]:

def save_and_clear_go_thread():
	"""
	save the current go_threads_df to disk
	and clear go_threads_df
	"""
	global file_count, total_go_threads_len, go_threads_df
	file_count += 1
	total_go_threads_len += len(go_threads_df)
	go_threads_df.to_csv(base_file_name + str(file_count) + '.csv')
	
	go_threads_df = pd.DataFrame(None, columns=['question', 'answer', 'answerID'])
	go_threads_df.index.rename("questionID")




# In[ ]:

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

		# #     if the post if a answer
		#     if key_content(line, "PostTypeId") == "2":
		#         if cur_id in without_answer.answerID.tolist():
		#             # if the post is an answer of a go question
		#             # put the answer and question into go_threads_df
		#             question_df = without_answer[without_answer.answerID == cur_id]
		#             go_threads_df = go_threads_df.append(
		#                 pd.DataFrame([[question_df.question, line, cur_id]], 
		#                              index=[question_df.index], 
		#                              columns=['question', 'answer', 'answerID']))
		#             without_answer = without_answer[without_answer.answerID != cur_id]
		# #     if the post if a question
		#     elif 'Tags="' in line:
		#         if ("&lt;go&gt" in key_content(line, "Tags")):
		# #             if the question has tag go
		# #             put the question into without_answer
		#             if 'AcceptedAnswerId="' in line:
		#                 AcceptedAnswerId = int(key_content(line, "AcceptedAnswerId"))
		#                 without_answer = without_answer.append(
		#                     pd.DataFrame([[line, AcceptedAnswerId]], 
		#                                  index=[cur_id], 
		#                                  columns=['question', 'answerID']))

			# if total_go_threads_len > 10:
			# 	print(questions)
			# 	break
				# save and clear to go_thread once the len(go_threads_df) > 5000
				# save_and_clear_go_thread()
				# print('saved 5000 go threads to disk')
		except:
			print(line)
			print("sth wrong, but continue: "+ sys.exc_info()[0])
			continue




question_df = pd.DataFrame(data = questions, columns=['PostId', 'Body', 'AnswerCount', 'AcceptedAnswerId', 'AnswerIds'])
answer_df = pd.DataFrame(data = answers, columns=['PostId', 'Body', 'ParentId'])

question_df.to_csv("questions.csv")
answer_df.to_csv("answers.csv")

# In[ ]:

# save_and_clear_go_thread()

# without_answer.to_csv('./go_thread_data/without_answer_post.csv')

print("Total Go Threads: "+ str(total_go_threads_len))
print("Program finished")


# In[ ]:

# if there are still questions which has not been found the corresponding answer
# loop the file again
# if (len(without_answer) > 0):
#     with open("./Posts.xml", "r") as f
#         # skip the first 2 lines
#         f.readline()
#         f.readline()
#         for line in f:
#             cur_id = int(key_content(line, "Id"))
#             if cur_id in without_answer.answerID.tolist():
#                 question_df = without_answer[without_answer.answerID == cur_id]
#         #         print("find!")
#                 go_threads_df = go_threads_df.append(
#                     pd.DataFrame([[question_df.question, line, cur_id]], 
#                                  index=[question_df.index], 
#                                  columns=['question', 'answer', 'answerID']))
#                 without_answer = without_answer[without_answer.answerID != cur_id]
				
# save_and_clear_go_thread()
# without_answer.to_csv("without_answer_post.csv")


# In[ ]:



