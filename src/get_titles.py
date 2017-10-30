import pandas as pd

questions = pd.read_csv('../processed_data/questions.csv')

titles = questions['Title'].tolist()

with open('titles.txt', mode='wt', encoding='utf-8') as file:
	file.write('\n'.join(titles))