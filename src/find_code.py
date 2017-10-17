import pandas as pd
import re, html

code_beginning = '&lt;code&gt;'
code_ending = '&lt;/code&gt;'

class Code():
	def __init__(id, code):
		self.PostId = id
		self.Code = code

	
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

	if (key+'="' in line):
		start_index = line.index(key + '="')
		for index in range(start_index+len(key + '="'),len(line)):
			if line[index] == '"':
				end_index = index
				break
		return line[start_index + len(key + '="'): end_index]
	else:
		return False

def strip_html(content):
	return re.sub(r'<.*?>','',html.unescape(html.unescape(html.unescape(content))))  ## Unescape trice to make it cleaner.

codes = []
count = 0

answers = pd.read_csv('answers.csv')
answers_id = answers['PostId'].tolist()
questions = pd.read_csv('questions.csv')
questions_id = questions['PostId'].tolist()

all_ids = answers_id + questions_id
max_id = max(all_ids)
min_id = min(all_ids)


with open("./Posts.xml", "r") as f:
	print("Start to open the file")
	# skip the first 2 lines
	f.readline() # <?xml metadata>
	f.readline() # <posts>
	for line in f:
			# Check HasId
			cur_id = key_content(line, "Id")
			if (not cur_id):
				continue
			else:
				cur_id = int(cur_id)

			if (cur_id < min_id or cur_id > max_id):
				continue

			post_type_id = int(key_content(line, "PostTypeId"))

			if (post_type_id == 1): # Question
				tags = key_content(line, "Tags")
				if ("&lt;go&gt" in tags):  # Golang thread
					body = key_content(line, "Body")
					if (code_beginning in body):
						code_list = find_code(body)
						for code in code_list:
							new_code_section = (cur_id, strip_html(code)) 
							codes.append(new_code_section)
						print(cur_id)
						count += 1
			if (post_type_id == 2): 
				if (cur_id in answers_id):
					body = key_content(line, "Body")
					if (code_beginning in body):
						code_list = find_code(body)
						for code in code_list:
							new_code_section = (cur_id, strip_html(code)) 
							codes.append(new_code_section)
						print(cur_id)
						count += 1


code_df = pd.DataFrame(data = codes, columns=['PostId', 'Code'])
code_df.to_csv('code.csv')
