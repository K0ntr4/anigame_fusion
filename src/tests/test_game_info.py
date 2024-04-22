import time
import unittest
from unittest.mock import patch, Mock
from src.image.game_info import (
    GameInfo, get_year_recency,
    get_summary_keywords, is_relevant_adjective
)

TEKKEN_GAME_INFO = {
    'id': 7498,
    'first_release_date': 1424217600,
    'genres': [4],
    'name': 'Tekken 7',
    'summary': ('Experience the epic conclusion of the Mishima clan and unravel '
                'the reasons behind each step of their ceaseless fight. '
                'Powered by Unreal Engine 4, Tekken 7 features stunning '
                'story-driven cinematic battles and intense duels that '
                'can be enjoyed with friends and rivals alike through '
                'innovative fight mechanics.')
}


class TestGameInfo(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.game_info = GameInfo()

    @patch('requests.post')
    def test_authenticate(self, mock_post):
        """
        Test Twitch API Authentication
        """
        mock_response = Mock()
        response_body = {
            "access_token": "someAccessToken",
            "expires_in": 9112004,
            "token_type": "bearer"
        }
        mock_response.json.return_value = response_body
        mock_post.return_value = mock_response

        self.game_info.authenticate()

        self.assertIsNotNone(self.game_info.token)
        self.assertTrue(time.time() - response_body["expires_in"]
                        < self.game_info.authentication_time)

    @patch("requests.post")
    @patch("src.image.game_info.GameInfo.authenticate", Mock())
    def test_get_game_info(self, mock_post_info):
        """
        Test IGDB Response on https://api.igdb.com/v4/games
        """
        mock_response = Mock()
        response_body = [TEKKEN_GAME_INFO, {}]
        mock_response.json.return_value = response_body
        mock_post_info.return_value = mock_response
        self.game_info.token = {
            "access_token": "someAccessToken",
            "expires_in": 9112004,
            "token_type": "bearer"
        }
        info = self.game_info.get_game_info("Tekken 7")

        self.assertEqual(response_body[0], info)

    @patch("requests.post")
    @patch("src.image.game_info.GameInfo.authenticate", Mock())
    def test_get_genres(self, mock_post):
        """
        Test IGDB Response on https://api.igdb.com/v4/genres
        """
        mock_response = Mock()
        response_body = [{
            "id": 4,
            "name": "Fighting"
        }]
        mock_response.json.return_value = response_body
        mock_post.return_value = mock_response
        self.game_info.token = {
            "access_token": "someAccessToken",
            "expires_in": 9112004,
            "token_type": "bearer"
        }
        self.game_info.get_genres([4])

        self.assertEqual(response_body[0]["name"], 'Fighting')

    @patch("src.image.game_info.GameInfo.get_game_info", Mock(return_value=TEKKEN_GAME_INFO))
    @patch("src.image.game_info.GameInfo.get_genres", Mock(return_value=['Fighting']))
    @patch("src.image.game_info.GameInfo.authenticate", Mock())
    def test_get_game_keywords(self):
        """
        Test IGDB Response on https://api.igdb.com/v4/genres
        """
        self.game_info.token = {
            "access_token": "someAccessToken",
            "expires_in": 9112004,
            "token_type": "bearer"
        }
        keywords = self.game_info.get_game_keywords('Tekken 7')

        self.assertIsNotNone(keywords)
        self.assertIn("Fighting", keywords[1])

    def test_get_year_recency(self):
        self.assertEqual(get_year_recency(time.time()), 'newest')
        self.assertEqual(get_year_recency(time.time() - 4 * 365 * 24 * 60 * 60), 'recent')
        self.assertEqual(get_year_recency(time.time() - 7 * 365 * 24 * 60 * 60), 'mid')
        self.assertEqual(get_year_recency(time.time() - 10 * 365 * 24 * 60 * 60), 'early')
        self.assertEqual(get_year_recency(time.time() - 15 * 365 * 24 * 60 * 60), 'oldest')

    def test_get_summary_keywords(self):
        keywords = get_summary_keywords('Experience the epic conclusion of the Mishima clan '
                                        'and unravel the reasons '
                                        'behind each step of their ceaseless fight. Powered '
                                        'by Unreal Engine 4, Tekken 7 '
                                        'features stunning story-driven cinematic battles and '
                                        'intense duels that can be '
                                        'enjoyed with friends and rivals alike through '
                                        'innovative fight mechanics.')

        self.assertEqual(keywords,
                         ['Experience', 'epic', 'conclusion', 'clan', 'reasons'])

    def test_is_relevant_adjective(self):
        self.assertTrue(is_relevant_adjective('epic'))
        self.assertFalse(is_relevant_adjective('the'))


if __name__ == '__main__':
    unittest.main()
