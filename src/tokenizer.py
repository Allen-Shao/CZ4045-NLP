from nltk.tokenize import RegexpTokenizer
import pandas as pd
import nltk
import re
import numpy as np

def tokenize_code(code, dic, post):
    code_lines = list(filter(None, code.split('\n')))
    for line in code_lines:
        # store line info then append to 'post' array
        line_info = [line]
        tokens = tokenizer.tokenize(line)
        line_info.append(tokens)
        dic['tokens'] += (tokens)
        if tokens and re.match(comments, tokens[0]):
            t = tokens[0]
            t = t.replace('//', '')
            # tokenize comments as natural language
            t = natural_lang_tokenizer.tokenize(t)
            last = line_info.pop()
            last.pop()
            line_info.append(last + ['//'] + t)

            dic['tokens'].pop()
            dic['tokens'] += (last + ['//'] + t)
        post.append(line_info)
    return dic, post

def _tokenizer(post_df, code_df, store_directory, store_each_post = False, process_amount = None):
    tokenization=[]
    count = 0
    for post_number,p_id in enumerate(post_df.index.values):
        no_match = False
        body = post_df.loc[p_id]['Body']
        # separate code and natural language, store into parts
        parts = []
        # 1 for code, 0 for natural language
        code_or_not = []
        # if the body does not have any code block, no need to process
        if p_id not in code_df.index:
            parts.append(body)
            code_or_not=[0]
        else:
            code_blks = code_df.loc[p_id]['Code']
            # check code blk position in a post
            # arrange them in order
            position = {}
            if isinstance(code_blks, str):
                if body.find(code_blks) == -1:
                    no_match = True
                elif len(code_blks) > 20:
                    position[body.index(code_blks)] = code_blks
            else:
                for code_blk in code_blks.values:
                    # Note: the 'no-match' problem is due to different formatting/parsing methods from xml to csv
                    if not isinstance(code_blk, str):
                        continue
                    if body.find(code_blk) == -1:
                        no_match = True
                        break
                    if len(code_blk) > 20:
                        position[body.index(code_blk)] = code_blk
            if no_match:
                continue
            keylist = sorted(position.keys())
            for key in keylist:
                code = position[key]
                # handle the situation where the code appears more than once
                # split based on fist occurence
                rest = body.split(code, 1)
                parts += ([rest[0], code])
                code_or_not += ([0, 1] if rest[0] else [1])
                if len(rest) > 2:
                    parts.append(rest[-1])
                    if rest[-1].strip():
                        code_or_not.append(0)

                parts = list(filter(None, parts))
                body = rest[-1]
            if len(rest) == 2 and rest[1].strip():
                parts.append(rest[1])
                code_or_not.append(0)
        # post is used to store line by line info
        post = []
        # dic is used to store the overall info for one post
        dic = {'text' : body, 'tokens' : []}
        for index, value in enumerate(parts):
            if code_or_not[index]:
                dic, post = tokenize_code(value, dic, post)
            else:
                token = natural_lang_tokenizer.tokenize(value)
                post.append([value, token])
                dic['tokens'] += token

        # df for each post, do line by line annotation
        if store_each_post:
            post_tokenization_df = pd.DataFrame(post, columns = ['text', 'token'])
            post_tokenization_df.to_csv(store_directory + str(post_number)+'.csv')
        tokenization.append([p_id, dic['text'], dic['tokens']])
        count +=1
        if process_amount and count >= process_amount:
            break
    # df for all posts
    results = pd.DataFrame(tokenization, columns = ['post_id', 'text', 'tokens'])
    results.to_csv(store_directory + 'overall_results.csv')
    return results

ALL_codes = pd.read_csv("../processed_data/code.csv")
ALL_codes.set_index('PostId', inplace=True)

selected_qns = pd.read_csv('../processed_data/selected_questions.csv')
selected_ans = pd.read_csv('../processed_data/selected_answer.csv')
selected_post = pd.concat([selected_ans, selected_qns])[['PostId', 'Body']]
selected_post.set_index('PostId', inplace=True)

ground_truth_post = pd.read_csv('../processed_data/150_ground_truth_post.csv')
ground_truth_post.set_index('PostId', inplace=True)
ground_truth_post_ids = ground_truth_post.index.values

groud_truth_code_blk_list=[]
n = 0
for p_id in ground_truth_post_ids:
    if p_id in ALL_codes.index:
        groud_truth_code_blk_list.append([p_id, ALL_codes.loc[p_id]['Code']])
    else:
        n += 1
print(str(n) + " number of posts do not have code block")
ground_truth_code_blk = pd.DataFrame(groud_truth_code_blk_list, columns=['PostId', 'Code'])
ground_truth_code_blk.set_index('PostId', inplace=True)

identifier = r'[a-zA-Z_][\d\w_]*'

keywords = r'''break|default|func|interface|select|case|defer
                |go|map|struct|chan|else|goto|package|switch
                |const|fallthrough|if|range|type|continue|for|import|return|var'''

# operators and punctuation
operators = r'[%/\+\-\*\,;\$><!:\.\|&\^=\(\)\[\]\{\}]+'

decimal_literal = r'\d+i?'
octal_literal = r'0[1-7]*'
hex_literal = r'0[xX][1-9a-fA-F]+'
floating_literal = r''' \d+\.\d*(?:[eE][+-]\d+)?i?
                | \d+[eE][+-]\d+i?
                | \.\d+(?:[eE][+-]\d+)?i?
                '''
string_literal = r'''(?:\"\s*.*?\n?\")|(?:\'\s*.*?\n?\')'''

comments = r'//.*$'
function_call = r'\w+\.\w+\s*\(.*\)'
directory = r'/?\w+/(?:.+/)*\S+/?'

patterns =  keywords + '|' + function_call + '|' + string_literal + '|' + comments + '|'\
        + directory + '|' + identifier + '|' + operators + '|' \
        + hex_literal + '|' + floating_literal + '|' + octal_literal + '|' \
        + decimal_literal

tokenizer = RegexpTokenizer(patterns)
natural_lang_tokenizer = RegexpTokenizer(r'\S+')

# tokenize all ground truth posts
gt_results = _tokenizer(ground_truth_post, ground_truth_code_blk, '../processed_data/tokenizer_result/gt_results/', True, 100)

# tokenize all posts from 700 threads
all_results = _tokenizer(selected_post, ALL_codes , '../processed_data/tokenizer_result/others/', False)
