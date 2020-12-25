from flask import Flask, render_template, request, flash, session
import re
import utils
import spacy
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
from gensim.parsing.preprocessing import remove_stopwords
import gensim
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import *


app = Flask(__name__, static_folder="static")
FILE = 'final_clean_prod4.csv'

@app.route("/") 
def home():
	return render_template("index.html")

@app.route("/search", methods=["POST", "GET"]) 
def search():
	try:
		if request.method == "POST":
			df = utils.read_data(FILE)
			df = utils.generate_answer(request.form["type"],request.form["search"],df)
			return render_template("search.html", column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)
		else:
			flash("Some informations are missing or incorrect","info")
			return render_template("search.html")
	except:
			return render_template("search.html")

@app.route("/advanced_search", methods=["POST", "GET"]) 
def advanced_search():
	if len(str(request.form["search"])) > 0 and isinstance(request.form["search"], str) == True and len(str(request.form["search_type"])) > 0 and isinstance(request.form["search_type"], str) == True:
		df = utils.read_data(FILE)
		if request.method == "POST":
			df1 = utils.advanced_type_search(str(request.form["search"]).rstrip().lstrip(),df,str(request.form["search_type"]))
			return render_template("advanced_search.html", column_names=df1.columns.values, row_data=list(df1.values.tolist()), zip=zip)
		else:
			return render_template("advanced_search.html")
	else:
		return render_template("advanced_search.html")


if __name__ == "__main__":
	app.debug = True
	app.run()

