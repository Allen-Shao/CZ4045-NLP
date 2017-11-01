from nltk.tokenize import RegexpTokenizer
import pandas as pd
import nltk
import re
import string
from nltk import pos_tag, word_tokenize
import argparse
import os

def get_patterns():
    identifier = r'[a-zA-Z_][\d\w_]*'

    keywords = r'''break|default|func|interface|select|case|defer
                    |go|map|struct|chan|else|goto|package|switch
                    |const|fallthrough|if|range|type|continue|for|import|return|var'''

    # operators and punctuation
    operators = r'[%/\+\-\*\,;\$><!:\.\|&\^=\(\)\[\]\{\}]+'

    # special symbol
    special = r'[#]'

    decimal_literal = r'\d+i?'
    octal_literal = r'0[1-7]*'
    hex_literal = r'0[xX][0-9a-fA-F]+'
    floating_literal = r'''(?:\d+\.\d*(?:[eE][+-]\d+)?i?)|(?:\d+[eE][+-]\d+i?)|(?:\.\d+(?:[eE][+-]\d+)?i?)'''
    string_literal = r'''(?:\"\s*.*?\n?\")|(?:\'\s*.*?\n?\')'''

    comments = r'//.*$'
    function_call = r'(?:\w+\.\w+\s*\(.*\))|(?:\w+\s*\(.*\))'
    directory = r'/?\w+/(?:.+/)*\S+/?'

    return special + '|' + keywords + '|' + function_call + '|' + string_literal + '|' + comments + '|'\
            + directory + '|' + identifier + '|' + floating_literal + '|' \
            + hex_literal + '|' + operators + '|' + octal_literal + '|' \
            + decimal_literal

def tokenize_code(code, dic, post):
    code_lines = list(filter(None, code.split('\n')))
    for line in code_lines:
        # store line info then append to 'post' array
        line_info = [line]
        tokens = code_tokenizer.tokenize(line)
        # remove function definition from matching the case of function call
        fun_def = False
        for t in tokens:
            if re.match(function_call, t) and not re.match(r'(?:\w+\.\w+\s*\(.*\))',t):
                # if there is a { symbol after a function
                # re-tokenize the line
                if t != tokens[-1] and '{' in tokens[tokens.index(t)+1:]:
                    fun_def = True
                    break
        if fun_def:
            temp_patterns = patterns =  keywords + '|' + string_literal + '|' + comments + '|'\
                + directory + '|' + identifier + '|' + floating_literal + '|' \
                + hex_literal + '|' + operators + '|' + octal_literal + '|' \
                + decimal_literal
            temp_code_tokenizer = RegexpTokenizer(temp_patterns)
            tokens = temp_code_tokenizer.tokenize(line)
        line_info.append(tokens)
        dic['tokens'] += (tokens)
        if tokens and re.match(comments, tokens[-1]):
            t = tokens[-1]
            t = t.replace('//', '')
            # tokenize comments as natural language
            t = tokenize_natural_language(t)
            last = line_info.pop()
            last.pop()
            line_info.append(last + ['//'] + t)

            dic['tokens'].pop()
            dic['tokens'] += (last + ['//'] + t)
        post.append(line_info)
    return dic, post

ddef split_punc(token):

    punc = string.punctuation.replace('/', '')
    punctuation_mark = r"[{}]".format(punc) # create the pattern
    left = '<{[('
    right = '>}])'
    if re.match(punctuation_mark, token[0]) and not re.match(punctuation_mark, token[-1]):
#         print("first char is punctuation mark")
        token_lst = []
        iter_token = iter(range(len(token)))
        for i in iter_token: 
            if token[i] in punc:
                if token[i] in left:
                    corresponding_right = right[left.index(token[i])]
                    if corresponding_right in token:
                        token_lst.append(token[i:])
                        token_lst.insert(0, token[i:])
                        break
                token_lst.append(token[i])
            else:
                token_lst.append(token[i:])
                # copy the word token in front for later processing
                token_lst.insert(0, token[i:])
                break
        omit = ''
        lst = token_lst[:]
        for i in range(len(lst)-1, -1, -1):
            if token_lst[i] == '.':
                omit += token_lst[i]
            else:
                if len(omit) >= 3:
                    token_lst = token_lst[:i+1]
                    token_lst.append(omit)
                    if (i+len(omit)+1) < len(lst):
                        token_lst += lst[i+len(omit)+1:]
                    break
        return token_lst
    elif re.match(punctuation_mark, token[-1]) and not re.match(punctuation_mark, token[0]):
#         print("last char is punctuation mark")
        token_lst = []
        iter_token = iter(range(len(token)-1, -1, -1))
        for i in iter_token:
            if token[i] in punc:
                
                if token[i] in right:
                    corresponding_left = left[right.index(token[i])]
                    if corresponding_left in token:
                        token_lst.insert(0, token[:i+1])
                        token_lst.insert(0, token[:i+1])
                        break
                token_lst.insert(0, token[i])
            else:
                token_lst.insert(0, token[:i+1])
                # copy the word token in front for later processing
                token_lst.insert(0, token[:i+1])
                break
        omit = ''
        lst = token_lst[:]
        for i in range(len(lst)-1, -1, -1):
            if token_lst[i] == '.':
                omit += token_lst[i]
            else:
                if len(omit) >= 3:
                    token_lst = token_lst[:i+1]
                    token_lst.append(omit)
                    if (i+len(omit)+1) < len(lst):
                        token_lst += lst[i+len(omit)+1:]
                    break        
        return token_lst
    else:
        return [token, token]

def tokenize_natural_language(txt):
#     re_entity = r'(?:[A-Z][A-Za-z]*\s)*[A-Z][A-Za-z]*'

#     entities = RegexpTokenizer(re_entity).tokenize(txt)
#     name_entities = []
#     for entity in entities:
#         if " " not in entity:
#             break
#         satisfier = True
#         pos = nltk.pos_tag(entity.split(" "))[0][1]:
#         if pos == 'DT' or pos == 'PRP'or pos == 'CC' or pos == 'WRB' or pos == 'IN':
#             satisfier = False
#             break
#         if satisfier:
#             name_entities.append(entity)

#     if name_entities:
#         print(name_entities)
#     dic = {entity:entity.split(" ") for entity in name_entities}
#     entity_tokens = [item for sublist in dic.values() for item in sublist]
    space_tokenizer = RegexpTokenizer(r'\S+')
    tokens = space_tokenizer.tokenize(txt)

    new_token_list = []
#     find_entity = False
    iter_tokens = iter(tokens)
    for token in iter_tokens:
#         for key, val in dic.items():
#             index = tokens.index(token)
#             if token in val and (index+len(val)) < len(tokens):
#                 reconstruct = " ".join([tokens[t] for t in range(index, index + len(val))])
#                 splited = split_punc(reconstruct)
#                 if splited[0] == key:
#                     new_token_list += splited[1:]
#                     if len(val) != 1:
#                         for n in range(len(val)-1):
#                             next(iter_tokens)
#                     find_entity = True
#                     break
#         if find_entity:
#             find_entity = False
#             continue

        new_token_list += split_punc(token)[1:]

    # split abbreviation
    abbreviation = r'(?:n\'t$)|(?:\'s$)|(?:\'m$)|(?:\'ve$)|(?:\'re$)|(?:\'ll$)|(?:\'d$)'
    old_tokens = new_token_list[:]
    match_count = 0
    for i, t in enumerate(old_tokens):
        if re.search(abbreviation, t):
            m = re.search(abbreviation, t)
            word_root = t[:m.span()[0]]
            suffix = t[m.span()[0]:m.span()[1]]
            new_token_list[i+match_count] = word_root
            new_token_list.insert(i+match_count+1, suffix)
            match_count += 1

    return new_token_list

def _tokenizer(post_df, code_df, store_directory, store_each_post = False, process_amount = None):
    tokenization=[]
    count = 0
    for post_number,p_id in enumerate(post_df.index.values):
        no_match = False
        body = post_df.loc[p_id]['Body']
        # dic is used to store the overall info for one post
        dic = {'text' : body, 'tokens' : []}
        # separate code and natural language, store into parts
        parts = []
        # 1 for code, 0 for natural language
        code_or_not = []
        # if the body does not have any code block, no need to process
        if p_id in code_df.index:
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
            if keylist and len(rest) == 2 and rest[1].strip():
                parts.append(rest[1])
                code_or_not.append(0)
        # if there is not code block
        if not parts:
            parts.append(body)
            code_or_not=[0]
        # post is used to store line by line info
        post = []
        for index, value in enumerate(parts):
            if code_or_not[index]:
                dic, post = tokenize_code(value, dic, post)
            else:
                token = tokenize_natural_language(value)
                post.append([value, token])
                dic['tokens'] += token
        # df for each post, do line by line annotation
        if store_each_post:
            post_tokenization_df = pd.DataFrame(post, columns = ['text', 'token'])
            post_tokenization_df.to_csv(os.path.join(store_directory, str(post_number) + ".csv"))
        tokenization.append([p_id, dic['text'], dic['tokens']])
        count +=1
        if process_amount and count >= process_amount:
            break
    # df for all posts
    results = pd.DataFrame(tokenization, columns = ['post_id', 'text', 'tokens'])
    results.to_csv(os.path.join(store_directory + 'overall_results.csv'))
    return results


patterns = get_patterns()

# main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", type=str, default='./code.csv',
                     help="the csv file containing all the code blocks")
    parser.add_argument("selected_questions", type=str, default='./questions.csv',
                     help="the csv file containing all the selected questions")
    parser.add_argument("--selected_answers", type=str, default='./answers.csv',
                     help="the csv file containing all the selected answers")
    parser.add_argument("--test_dataset", type=str, default='./100_posts.csv', 
                     help="the csv file containing selected data used for further testing")
    args = parser.parse_args()

    all_codes = pd.read_csv(os.path.abspath(args.code))
    all_codes.set_index('PostId', inplace=True)

    selected_qns = pd.read_csv(os.path.abspath(args.selected_questions))
    selected_ans = pd.read_csv(os.path.abspath(args.selected_answers))
    selected_post = pd.concat([selected_ans, selected_qns])[['PostId', 'Body']]
    selected_post.set_index('PostId', inplace=True)

    ground_truth_post = pd.read_csv(os.path.abspath(args.test_dataset))
    ground_truth_post.set_index('PostId', inplace=True)
    ground_truth_post_ids = ground_truth_post.index.values

    groud_truth_code_blk_list=[]
    n = 0
    for p_id in ground_truth_post_ids:
        if p_id in all_codes.index:
            groud_truth_code_blk_list.append([p_id, all_codes.loc[p_id]['Code']])
        else:
            n += 1
    print(str(n) + " number of posts do not have code block")
    ground_truth_code_blk = pd.DataFrame(groud_truth_code_blk_list, columns=['PostId', 'Code'])
    ground_truth_code_blk.set_index('PostId', inplace=True)



    code_tokenizer = RegexpTokenizer(patterns)

    if not os.path.exists('./processed_gt_data/'):
        os.makedirs('./processed_gt_data/')
    # tokenize all ground truth posts
    gt_results = _tokenizer(ground_truth_post, ground_truth_code_blk, './processed_gt_data/', True, 100)
    print("The ground truth tokenization result is under ./processed_gt_data/")

    if not os.path.exists('./processed_all_data/'):
        os.makedirs('./processed_all_data/')
    # tokenize all posts from 700 threads
    all_results = _tokenizer(selected_post, all_codes , './processed_all_data/', False)
    print("The overall tokenization result is under ./processed_all_data/")
