import dash
import pickle
import string
import numpy as np

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords 
from nltk.stem import wordnet
import contractions

new_punctuation_list = list(string.punctuation) + ['...']

stopword_list = stopwords.words('english')

stopwords1 = stopword_list[:116]
stopwords2 = stopword_list[119:131]
stopwords3 = stopword_list[133:143]
stopwords4 = ['ma']

new_stopwords_list = stopwords1 + stopwords2 + stopwords3 + stopwords4

def lemmatize_input_review(review_text: str):
  expanded_review_text = contractions.fix(review_text)
  all_tokens = wordpunct_tokenize(expanded_review_text)
  tokens = []
  stopword_count = 0
  punctuation_count = 0

  for token in all_tokens:
    if token not in new_punctuation_list:
      cleaned_token = token.lower().replace(" ","")
      if cleaned_token not in new_stopwords_list:
        tokens.append(cleaned_token)
      else:
        stopword_count+=1
    else:
      punctuation_count+=1
  lem = wordnet.WordNetLemmatizer()
  lemmatized_tokens = [lem.lemmatize(token) for token in tokens]
  lemma_str = " ".join(lemmatized_tokens)

  return lemma_str

def vectorize_input_lemma(lemma_string: str):
  with open('assets/tdidf.pkl', 'rb') as f:
    tv = pickle.load(f)
  input_vector = tv.transform(np.array([lemma_string]))

  return input_vector

def classify_and_predict(input_vector):
  with open('assets/lr_unbalanced.pkl', 'rb') as f:
    lr_model_tdidf_unbalanced = pickle.load(f)

  predicted_value = lr_model_tdidf_unbalanced.predict(input_vector)
  predicted_label = ['Positive' if p==1 else 'Negative' for p in predicted_value]

  return predicted_label[0]

def run_pipeline(input_review):
    lemmas = lemmatize_input_review(input_review)
    lemma_vector = vectorize_input_lemma(lemmas)
    prediction = classify_and_predict(lemma_vector)

    return prediction
