
# coding: utf-8

# In[ ]:

import pandas as pd
from help_func import *
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


# In[ ]:

from nltk.tokenize import TweetTokenizer
 
tknzr = TweetTokenizer()


# In[ ]:

write = ""


# In[ ]:

# read data
answers = read_dataframe(path="../processed_data/answers.csv")
questions = read_dataframe(path="../processed_data/questions.csv")


# In[ ]:

# number of questions
tex = "There are %d questions" % len(questions)
print(tex)
write += tex + '\n\n'


# In[ ]:

# number of answers
tex = "There are %d answers" % len(answers)
print(tex)
write += tex + '\n\n'


# In[ ]:

# what is the percentage of questions having one, two, or more answers

c = Counter(questions.AnswerCount)
x = list(c.keys())
y = [i / len(questions) for i in c.values()]

# plot the histogram
fig, ax = plt.subplots(figsize=(10,6))
rect = ax.bar(x,y,align='center') # A bar chart
plt.title("Percentage of questions having one, two, or more answers")
plt.xlabel('Number of answers')
plt.ylabel('Percentage')
# for i in range(len(y)):
#     plt.hlines(y[i],0,x[i]) # Here you are drawing the horizontal lines
def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.3f' % (float(height) * 100) + "%",
                ha='center', va='bottom')

autolabel(rect)
plt.savefig('../Stats/NoOfAnswerDist.png')
plt.show()
plt.close()

# save the result in text
for i in sorted(c.keys()):
    tex = "There are %.3f"  % (c[i] / len(questions) * 100) + "% " + "of question have %d answer(s)." % i
    print(tex)
    write += tex + '\n'
    
write += "\n"


# In[ ]:

# the length of the posts in number of words (using an off- the-shelf tokenizer).


# In[ ]:

def get_Post_Token_Length(question_series):
    ans_length = 0
    for i in answers[answers.ParentId == question_series.PostId].Body.tolist():
        ans_length+=len(tknzr.tokenize(i))
    que_length = len(tknzr.tokenize(question_series.Title + question_series.Body))
    return (ans_length, que_length)


# In[ ]:

question_copy = questions.copy()
question_copy['ans_token_length'] = pd.Series([None] * len(question_copy))
question_copy['question_token_length'] = pd.Series([None] * len(question_copy))


# In[ ]:

for i in range(len(question_copy)):
    cur_q = question_copy.iloc[i]
    cur_ans_length, cur_que_length = get_Post_Token_Length(cur_q)
    question_copy.set_value(i,'ans_token_length', cur_ans_length)
    question_copy.set_value(i,'question_token_length', cur_que_length)
    


# In[ ]:

plt.plot(sorted(list(question_copy.ans_token_length)))
plt.title("Length of the post answers in number of tokens (nltk TweetTokenizer)")
plt.ylabel("Lengths of Tokens in Answers of a Question")
plt.xlabel("Questions")
plt.savefig("../Stats/ans_length_dist.png")
plt.show()
plt.close()

plt.plot(sorted(list(question_copy.question_token_length)))
plt.title("Length of the post question in number of tokens (nltk TweetTokenizer)")
plt.ylabel("Lengths of Tokens in a Question")
plt.xlabel("Questions")
plt.savefig("../Stats/question_length_dist.png")
plt.show()
plt.close()


# In[ ]:

question_copy['total_length'] = question_copy['question_token_length'] + question_copy['ans_token_length']
plt.plot(sorted(list(question_copy.total_length)))
plt.title("Length of the whole post including question and answers in number of tokens (nltk TweetTokenizer)")
plt.ylabel("Lengths of Tokens in a Post")
plt.xlabel("Post")
plt.savefig("../Stats/post_length_dist.png")
plt.show()
plt.close()


# In[ ]:

write += "For Lengths of Tokens in Answers of a Question: \n"
write += "95 percentile is %d. \n" % np.percentile(question_copy.ans_token_length, 95)
write += "Min is %d. \n" % np.min(question_copy.ans_token_length)
write += "Max is %d. \n" % np.max(question_copy.ans_token_length)
write += "\n"


# In[ ]:

write += "For Lengths of Lengths of Tokens in an Answer: \n"
write += "95 percentile is %d. \n" % np.percentile(question_copy.question_token_length, 95)
write += "Min is %d. \n" % np.min(question_copy.question_token_length)
write += "Max is %d. \n" % np.max(question_copy.question_token_length)
write += "\n"


# In[ ]:

write += "For Lengths of Lengths of Tokens in a Post: \n"
total = list(question_copy.total_length)
write += "95 percentile is %d. \n" % np.percentile(total, 95)
write += "Min is %d. \n" % np.min(total)
write += "Max is %d. \n" % np.max(total)


# In[ ]:

with open("../Stats/stats_text.txt", 'w') as f:
    f.writelines(write)


# In[ ]:

print(write)


# In[ ]:



