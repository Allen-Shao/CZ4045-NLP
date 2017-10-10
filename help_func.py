import pandas as pd

def read_dataframe(path):
	return pd.read_csv(path, index_col=0)
	# TODO: Need some process maybe


def find_answers(answers_df, questionId):
	return answers_df.loc[(answers_df["ParentId"] == questionId)]


def find_answers(questions_df, answers_df, questionId):
	return answers_df.loc[answers_df["PostId"] == questions_df.loc[questions_df['PostId']==questionId]['AcceptedAnswerId']]


def check_answers_count(questions_df, answers_df, questionId):
	return questions_df.loc[questions_df['PostId']==questionId]['AnswerCount'] == len(find_answers(answers_df, questionId))