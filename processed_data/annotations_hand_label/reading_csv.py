import pandas as pd
# for i in range (100):
#     post = str(i)+'.csv'
#     code = pd.read_csv(post, index_col=0)
#     for j in range(len(code)):
#         print("Post: " + post, end=" ")
#         print("Index: " + str(j))
#         print()
#         print(code.loc[j].text)
#         print()
#         print(code.loc[j].token)
#         print()
#         print(code.loc[j]["annotation"])
#         input()
    
for i in range (0, 1):
    post = str(63)+'.csv'
    content = pd.read_csv(post, index_col=0)
    print(content)
    # for j in range(len(content)):   
    # print(i)
    # print(content.loc[0].text)
    # print(content.loc[len(content)-1].text)
    


