import re
import spacy
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords
import gensim
from gensim.models import Word2Vec
import nltk
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_data(text):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 1500000
    stemmer = SnowballStemmer(language='english')
    text = remove_stopwords(text).rstrip().lstrip().lower()
    text = (re.sub("[^a-zA-Z]"," ",text))
    return text

def get_data(df,text,query):
	try:
		if len(str(query)) > 0 and isinstance(query, str) == True and len(str(text)) > 0 and isinstance(text, list) == True:
			vectorizer = TfidfVectorizer()
			X = vectorizer.fit_transform(text)
			vectorizer.fit(text)
			vector = vectorizer.transform([query])
			results = cosine_similarity(X,vector).reshape((-1,))
			df['grades'] = results
			df = df.sort_values(by=['grades'], ascending=False)
			return df[['title','recommendations','artist','publisher','writer','genres','summary']].head(100)
		else:
			pass
	except:
		pass

def read_data(dataset):
	try:
		if len(str(dataset)) > 0 and isinstance(dataset, str) == True:
			df = pd.read_csv(dataset)
			if len(df) > 0 and isinstance(df, pd.DataFrame) == True:
				return df
			else:
				pass
		else:
			pass
	except:
		pass

def execute_search(input_data,search_field,df):
	query = clean_data(input_data)
	text = df[search_field].values.tolist()
	df = get_data(df,text,query)	
	return df

def advanced_type_search(input_data,df,search_type):
	if search_type == 'title' and df['title'].str.contains(input_data).any() == True:
		df['occ'] = df['title'].str.contains(input_data) 
		df1 = df.loc[df['occ'] == True]
	elif search_type == 'genres' and df['genres'].str.contains(input_data).any() == True:
		df['occ'] = df['genres'].str.contains(input_data) 
		df1 = df.loc[df['occ'] == True]
	elif search_type == 'artist' and  df['artist'].str.contains(input_data).any() == True:
		df['occ'] = df['artist'].str.contains(input_data)
		df1 = df.loc[df['occ'] == True]
	elif search_type == 'publisher' and df['publisher'].str.contains(input_data).any() == True:
		df['occ'] = df['publisher'].str.contains(input_data)
		df1 = df.loc[df['occ'] == True]
	elif search_type == 'writer' and df['writer'].str.contains(input_data).any() == True:
		df['occ'] = df['writer'].str.contains(input_data)
		df1 = df.loc[df['occ'] == True]
	return df1

def generate_answer(type_request,query,df):
	if len(type_request) > 0 and isinstance(type_request, str) == True and len(str(type_request)) > 0 and isinstance(type_request, str) == True and len(query) > 0 and isinstance(query, str) == True and len(str(query)) > 0 and isinstance(query, str) == True: 
		if str(type_request) == "title_search":
			df = execute_search(str(query),"title",df)	
			return df
		elif  str(type_request) == "plot_search":
			df = execute_search(str(query),"clean_summary",df)	
			return df
		else:
			flash("Some informations are missing or incorrect","info")
			return render_template("search.html")
	else:
		flash("Some informations are missing or incorrect","info")
		return render_template("search.html")
