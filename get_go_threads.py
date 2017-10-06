
# coding: utf-8

# In[ ]:

import time
import pickle
import pandas as pd
import os


# In[ ]:

base_file_name = "./go_thread_data/go_thread_data_"
file_count = 0
if (os.path.exists("./go_thread_data/")) is False:
#     if path not exists, make directory
    os.mkdir("./go_thread_data/")


# In[ ]:

def key_content(line, key):
    """
    since we read the file line by line
    this function is to parse the content of a key in a line
    """
    start_index = line.index(key + '="')
    for index in range(start_index+len(key + '="'),len(line)):
        if line[index] == '"':
            end_index = index
            break
    return line[start_index + len(key + '="'): end_index]


# In[ ]:

# class Go_thread:
#     def __init__(self, question, questionID, answer, answerID):
#         self.question_post = question
#         self.questionID = questionID
#         self.answer = answer
#         self.answerID = answerID
        


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
go_threads_df = pd.DataFrame(None, columns=['question', 'answer', 'answerID'])
go_threads_df.index.rename("questionID")

without_answer = pd.DataFrame(None, columns=['question', 'answerID'])
start_time = time.time()

with open("./Posts.xml", "r") as f:
    print("Start to open the file")
    # skip the first 2 lines
    f.readline()
    f.readline()
    for line in f:
        current_line_id = int(key_content(line, "Id"))
    #     if the post if a answer
        if key_content(line, "PostTypeId") == "2":
            if current_line_id in without_answer.answerID.tolist():
                # if the post is an answer of a go question
                # put the answer and question into go_threads_df
                question_df = without_answer[without_answer.answerID == current_line_id]
                go_threads_df = go_threads_df.append(
                    pd.DataFrame([[question_df.question, line, current_line_id]], 
                                 index=[question_df.index], 
                                 columns=['question', 'answer', 'answerID']))
                without_answer = without_answer[without_answer.answerID != current_line_id]
    #     if the post if a question
        elif 'Tags="' in line:
            if ("&lt;go&gt" in key_content(line, "Tags")):
    #             if the question has tag go
    #             put the question into without_answer
                if 'AcceptedAnswerId="' in line:
                    AcceptedAnswerId = int(key_content(line, "AcceptedAnswerId"))
                    without_answer = without_answer.append(
                        pd.DataFrame([[line, AcceptedAnswerId]], 
                                     index=[current_line_id], 
                                     columns=['question', 'answerID']))

        if len(go_threads_df) > 5000:
            # save and clear to go_thread once the len(go_threads_df) > 5000
            save_and_clear_go_thread()
            print('saved 5000 go threads to disk')
    


# In[ ]:

save_and_clear_go_thread()
without_answer.to_csv("without_answer_post.csv")
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
#             current_line_id = int(key_content(line, "Id"))
#             if current_line_id in without_answer.answerID.tolist():
#                 question_df = without_answer[without_answer.answerID == current_line_id]
#         #         print("find!")
#                 go_threads_df = go_threads_df.append(
#                     pd.DataFrame([[question_df.question, line, current_line_id]], 
#                                  index=[question_df.index], 
#                                  columns=['question', 'answer', 'answerID']))
#                 without_answer = without_answer[without_answer.answerID != current_line_id]
                
# save_and_clear_go_thread()
# without_answer.to_csv("without_answer_post.csv")

