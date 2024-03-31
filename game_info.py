import requests
import os
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

DATE_RECENCY = {'newest': (2021, int(time.strftime('%Y', time.gmtime(time.time())))), 'recent': (2018, 2020), 'mid': (2015, 2017), 'early': (2011, 2014), 'oldest': (2005, 2010)}
FILTER_WORDS = ['game', 'play']

# Function to determine the relevance of an adjective
def is_relevant_adjective(word):
    synsets = wn.synsets(word)
    if synsets:
        return True
    else:
        return False

class GameInfo():
    def __init__(self):
        self.token = None
        self.client_id = os.environ.get('TWITCH_CLIENT_ID')

    def authenticate(self, client_id, client_secret):
        if self.token and time.time() - self.authenticationTime < self.token['expires_in']:
            return
        url = "https://id.twitch.tv/oauth2/token"
        querystring = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.request("POST", url, params=querystring)
        self.token = response.json()
        self.authenticationTime = time.time()

    def get_game_info(self, name):
        self.authenticate(self.client_id, os.environ.get('TWITCH_CLIENT_SECRET'))
        url = "https://api.igdb.com/v4/games"

        payload = f"search \"{name}\"; fields name, first_release_date, genres, summary;\nwhere category = 0;\nlimit 1;"
        headers = {
            "Content-Type": "text/plain",
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token['access_token']}"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code != 200:
            print(f"Failed to get game information: {response.text}")
            return
        response = response.json()
        if not response:
            print(f"Game with name {name} not found")
            return
        response = response[0]
        return response['first_release_date'], response['genres'], response['name'], response['summary']

    def get_year_recency(self, release_date):
        year = int(time.strftime('%Y', time.gmtime(release_date)))
        for recency, years in DATE_RECENCY.items():
            if years[0] <= year <= years[1]:
                return recency
        return 'oldest'

    def get_genres(self, genre_ids):
        self.authenticate(self.client_id, os.environ.get('TWITCH_CLIENT_SECRET'))
        url = "https://api.igdb.com/v4/genres"

        payload = f"fields name; where id = {str(tuple(genre_ids))};"
        headers = {
            "Content-Type": "text/plain",
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token['access_token']}"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        response = list(map(lambda x: x['name'], response.json()))
        return response

    def get_summary_keywords(self, summary):
        tokens = word_tokenize(summary)
        tagged = pos_tag(tokens)
        return [word for word, tag in tagged if tag in ('NN', 'NNS', 'JJ', 'JJR', 'JJS') and is_relevant_adjective(word) and all(FILTER_WORD not in word for FILTER_WORD in FILTER_WORDS)][:15]

    def get_game_keywords(self, name):
        release_date, genre_ids, name, summary = self.get_game_info(name)
        year = self.get_year_recency(release_date)
        genres = self.get_genres(genre_ids)
        keywords = self.get_summary_keywords(summary)
        return year, list(set(genres + keywords))


if __name__ == "__main__":
    name = input("What is the full name of the game you want to get information for? ")
    # normalize the name to ascii
    name = name.encode('ascii', errors='ignore').decode()
    game_info = GameInfo()
    year, keywords = game_info.get_game_keywords(name)
    print(year, keywords)