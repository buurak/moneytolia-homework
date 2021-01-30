from flask import Blueprint, render_template, request
from .forms import SearchForm
import requests
import json

words = Blueprint('words', __name__)


BASE_URL = 'https://wordsapiv1.p.rapidapi.com/words/'


headers = {
    'x-rapidapi-key': "821b950c45msh91f67e1bf3b5100p198b0djsnfe5b8481ac28",
    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
    }

@words.route('/search', methods=['GET','POST'])
def search_words():
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm()
        searchedWord = form.search.data
        url = BASE_URL+ searchedWord + '/definitions'
        r = requests.get(url, headers=headers)
        result = r.json()
        meanings=[]
        for meaning in result['definitions']:
            meanings.append(meaning['definition'])
    
        return render_template('index.html', meanings=meanings, form=form, word=searchedWord)

    return render_template('index.html',form=form)
