import os
import time
import nltk
import requests
import requests_cache
from nltk.corpus import wordnet as wn
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
nltk.download('wordnet', quiet=True)
requests_cache.install_cache('game_api_cache', expire_after=3600)

CURRENT_YEAR = int(time.strftime('%Y', time.gmtime(time.time())))
DATE_RECENCY = { # Date ranges provided by ai model
    'newest': (2021, int(time.strftime('%Y', time.gmtime(time.time())))),
    'recent': (2018, 2020),
    'mid': (2015, 2017),
    'early': (2011, 2014),
    'oldest': (2005, 2010)
}
FILTER_WORDS = ['game', 'play']


def is_relevant_adjective(word):
    """
    Check if a word is a relevant adjective using WordNet.
    """
    synsets = wn.synsets(word)
    return bool(synsets)


def get_year_recency(release_date):
    """
    Determine the recency category based on the release date.
    """
    release_year = int(time.strftime('%Y', time.gmtime(release_date)))
    for recency, years in DATE_RECENCY.items():
        if years[0] <= release_year <= years[1]:
            return recency
    return 'oldest'


def get_summary_keywords(summary):
    """
    Extract relevant keywords from the game summary.
    """
    tokens = word_tokenize(summary)
    tagged = pos_tag(tokens)
    summary_keywords = [word for word, tag in tagged if
                        tag in ('NN', 'NNS', 'JJ', 'JJR', 'JJS')
                        and is_relevant_adjective(word)
                        and all(
                            FILTER_WORD not in word for FILTER_WORD in FILTER_WORDS)]
    return summary_keywords[:5]


class GameInfo:
    """
    Class to fetch game information from Twitch and IGDB.
    """

    def __init__(self):
        self.token = None
        self.client_id = os.environ.get('TWITCH_CLIENT_ID')
        self.client_secret = os.environ.get('TWITCH_CLIENT_SECRET')
        self.authentication_time = 0

    def authenticate(self):
        """
        Authenticate with the Twitch API.
        """
        if self.token and time.time() - self.authentication_time < self.token['expires_in']:
            return
        url = "https://id.twitch.tv/oauth2/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        self.token = response.json()
        self.authentication_time = time.time()
        return

    def get_game_info(self, name):
        """
        Fetch game information from the IGDB API.
        """
        self.authenticate()
        url = "https://api.igdb.com/v4/games"
        payload = (f"search \"{name}\"; fields name, first_release_date, genres, summary;"
                   f"\nwhere category = 0;\nlimit 1;")
        headers = {
            "Content-Type": "text/plain",
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token['access_token']}"
        }
        response = requests.post(url, data=payload, headers=headers, timeout=3)
        response.raise_for_status()
        games = response.json()
        if not games:
            print(f"Game with name '{name}' not found")
            return None
        return games[0]

    def get_genres(self, genre_ids):
        """
        Fetch genre names from the IGDB API.
        """
        self.authenticate()
        url = "https://api.igdb.com/v4/genres"
        payload = (f"fields name; where id = "
                   f"{(str(genre_ids)).translate(str.maketrans('[]', '()'))};")
        headers = {
            "Content-Type": "text/plain",
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token['access_token']}"
        }
        response = requests.post(url, data=payload, headers=headers, timeout=3)
        response.raise_for_status()
        genres = [genre['name'] for genre in response.json()]
        return genres

    def get_game_keywords(self, name):
        """
        Get recency, genres, and keywords for a game.
        """
        game_details = self.get_game_info(name)
        if not game_details:
            return None

        release_date = game_details.get('first_release_date', 0)
        genre_ids = game_details.get('genres', None)
        summary = game_details.get('summary', '')

        recency = get_year_recency(release_date)
        genres = genre_ids and self.get_genres(genre_ids)
        buzzwords = get_summary_keywords(summary)

        return recency, list(set(genres + buzzwords))


if __name__ == "__main__":
    game_info = GameInfo()
    keywords = game_info.get_game_keywords("Tekken 7")
    if keywords:
        year, game_keywords = keywords
        print(f"Year recency: {year}")
        print(f"Game keywords: {game_keywords}")
