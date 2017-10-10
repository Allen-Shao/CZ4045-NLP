
import sys
from bs4 import BeautifulSoup

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

target = input("Input id to be found: ")



with open("./Posts.xml", "r") as f:
	print("Start to open the file")
	# skip the first 2 lines
	f.readline() # <?xml metadata>
	f.readline() # <posts>
	for line in f:
		try:
			if (key_content(line, "Id") == target):
				print(line)
				break;
		except:
			print(line)
			print("sth wrong, but continue: ", sys.exc_info()[0])
			break