import os
import time
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn

# Download NLTK resources if not already downloaded
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

DATE_RECENCY = {
    'newest': (2021, int(time.strftime('%Y', time.gmtime(time.time())))),
    'recent': (2018, 2020),
    'mid': (2015, 2017),
    'early': (2011, 2014),
    'oldest': (2005, 2010)
}
FILTER_WORDS = ['game', 'play']


def is_relevant_adjective(word):
    synsets = wn.synsets(word)
    return bool(synsets)

class GameInfo:
    def __init__(self):
        self.token = None
        self.client_id = os.environ.get('TWITCH_CLIENT_ID')
        self.client_secret = os.environ.get('TWITCH_CLIENT_SECRET')
        self.authentication_time = 0

    def authenticate(self):
        if self.token and time.time() - self.authentication_time < self.token['expires_in']:
            return

        url = "https://id.twitch.tv/oauth2/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        self.token = response.json()
        self.authentication_time = time.time()

    def get_game_info(self, name):
        self.authenticate()
        url = "https://api.igdb.com/v4/games"
        payload = f"search \"{name}\"; fields name, first_release_date, genres, summary;\nwhere category = 0;\nlimit 1;"
        headers = {
            "Content-Type": "text/plain",
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token['access_token']}"
        }
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        games = response.json()
        if not games:
            print(f"Game with name '{name}' not found")
            return None
        return games[0]

    def get_year_recency(self, release_date):
        year = int(time.strftime('%Y', time.gmtime(release_date)))
        for recency, years in DATE_RECENCY.items():
            if years[0] <= year <= years[1]:
                return recency
        return 'oldest'

    def get_genres(self, genre_ids):
        self.authenticate()
        url = "https://api.igdb.com/v4/genres"
        payload = f"fields name; where id = {(str(genre_ids)).translate(str.maketrans('[]','()'))};"
        headers = {
            "Content-Type": "text/plain",
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token['access_token']}"
        }
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        genres = [genre['name'] for genre in response.json()]
        return genres

    def get_summary_keywords(self, summary):
        tokens = word_tokenize(summary)
        tagged = pos_tag(tokens)
        keywords = [word for word, tag in tagged if tag in ('NN', 'NNS', 'JJ', 'JJR', 'JJS') and is_relevant_adjective(word) and all(FILTER_WORD not in word for FILTER_WORD in FILTER_WORDS)]
        return keywords[:10]

    def get_game_keywords(self, name):
        game_info = self.get_game_info(name)
        if not game_info:
            return None

        release_date = game_info.get('first_release_date', 0)
        genre_ids = game_info.get('genres', None)
        summary = game_info.get('summary', '')

        year = self.get_year_recency(release_date)
        genres = genre_ids and self.get_genres(genre_ids)
        keywords = self.get_summary_keywords(summary)

        return year, list(set(genres + keywords))

if __name__ == "__main__":
    game_info = GameInfo()
    keywords = game_info.get_game_keywords("Tekken 7")
    if keywords:
        year, game_keywords = keywords
        print(f"Year recency: {year}")
        print(f"Game keywords: {game_keywords}")