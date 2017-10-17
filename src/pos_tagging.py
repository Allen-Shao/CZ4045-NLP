
# coding: utf-8

# In[11]:


import nltk
text = nltk.word_tokenize("if nr >= buf_size { die (""Buffer overrun"") }")
nltk.pos_tag(text)

