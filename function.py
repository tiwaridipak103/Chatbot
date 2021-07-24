import pandas as pd
import re
import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from newspaper import Article
import random
import string
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# https://stackoverflow.com/a/47091490/4084039
def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase 

def remove_underscore(string):
  e = []
  for i in string.split(' '):
    if len(i) >=1:
      if i[0] == '_' and i[len(i)-1] == '_':
        e.append(i[1:(len(i)-1)])
        continue
      if i[0] == '_':
        e.append(i[1:])
        continue
      if i[len(i)-1] == '_':
        e.append(i[0:(len(i)-1)])
        continue
      else:
        e.append(i) 

  return ' '.join(e)

#complete preprocessing function
def data_preprocessing(Input_Text):
  preprocessed_string = []
  for i in range(len(Input_Text)):
    x = Input_Text[i].replace("from:", "").replace("write to:", "").replace('\\n',' ').replace('\\t',' ')
    remove_char_word = lambda y: ' '.join(j for j in y.split() if ':' not in j)
    x = remove_char_word(x)
    x = decontracted(x)
    x = remove_underscore(x)
    preprocessed_string.append(x)

  return  preprocessed_string

#creating greeting response 
def greeting_response(text):
  text = text.lower()

  #bot greting resonce
  bot_gretting = ['hi', 'hello', 'hola' , 'hey']
  
  #user gretting responds
  user_gretting = ['wasaap' , 'hello', 'hola' , 'hi']

  for word in text.split():
    if word in user_gretting:
      return random.choice(bot_gretting)

def index_sort(list_var):
  length = len(list_var)
  list_index = list(range(0 , length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        #swap
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j]  = temp

  return list_index


#create bot responce
def bot_responce(user_input):
  user_input = user_input.lower()
  preprocessed.append(user_input)
  bot_resp = ''
  cm = CountVectorizer().fit_transform(preprocessed)
  simi_score = cosine_similarity(cm[-1] , cm)
  simi_list = simi_score.flatten()
  index = index_sort(simi_list)

  index = index[1:]
  response_flag = 0

  j = 0
  for i in range(len(index)):
    if simi_list[index[i]] > 0.0 :
      bot_resp = bot_resp + ' ' + preprocessed[index[i]]
      response_flag = 1
      j = j + 1

      if j > 2:
        break

  if response_flag ==0:
    bot_resp = bot_resp + ' ' + "i apologies , i don't understand"

  preprocessed.remove(user_input)

  return bot_resp 

#downlaod the article
article = Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp
corpous = article.text

#tokenization
text = corpous
sentence_list = nltk.sent_tokenize(text)
preprocessed = data_preprocessing(sentence_list)


