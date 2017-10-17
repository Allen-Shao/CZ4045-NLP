import pandas as pd

top = 120

code_df = pd.read_csv('code.csv', index_col=0)
code_df['PostId'] = code_df['PostId'].astype(str)
code_df['Code'] = code_df['Code'].astype(str)


code_df['CodeLength'] = code_df['Code'].apply(lambda x: len(x))



code_len_df = code_df.groupby('PostId', sort=False, as_index=False).sum()
code_len_df = code_len_df.sort_values('CodeLength', ascending=False).reset_index().drop('index', axis=1)
top_list = code_len_df[0:top]['PostId'].tolist()
print("Top %d long code session indexes:"%top)
print(top_list)

code_top = code_df.loc[code_df['PostId'].isin(top_list)].reset_index().drop('index', axis=1)

code_top.to_csv('code_top'+str(top)+'.csv')