import pandas as pd
for i in range (16, 100):
    post = str(i)+'.csv'
    code = pd.read_csv(post, index_col=0)
    for j in range(len(code)):
        print("Post: " + post, end=" ")
        print("Index: " + str(j))
        print()
        print(code.loc[j].text)
        print()
        print(code.loc[j].token)
        print()
        print(code.loc[j]["annotation"])
        input()
    
        
    


