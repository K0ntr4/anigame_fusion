import time
import unittest
from src.image.game_info import (
    GameInfo, get_year_recency,
    get_summary_keywords, is_relevant_adjective
)


class TestGameInfo(unittest.TestCase):
    def setUp(self):
        self.game_info = GameInfo()

    def test_authenticate(self):
        self.game_info.authenticate()
        self.assertIsNotNone(self.game_info.token)
        self.assertIsNotNone(self.game_info.authentication_time)
        self.assertTrue(time.time() - self.game_info.authentication_time
                        < self.game_info.token['expires_in'])

    def test_get_game_info(self):
        # Call the method under test
        game_data = self.game_info.get_game_info('Tekken 7')

        # Assertions
        self.assertIsNotNone(game_data)
        self.assertEqual(game_data['name'], 'Tekken 7')
        self.assertEqual(game_data['first_release_date'], 1424217600)
        self.assertEqual(game_data['genres'], [4])
        self.assertEqual(game_data['summary'], 'Experience the epic conclusion of the '
                                               'Mishima clan and unravel the '
                                               'reasons behind each step of their ceaseless fight. '
                                               'Powered by Unreal '
                                               'Engine 4, Tekken 7 features stunning story-driven '
                                               'cinematic battles '
                                               'and intense duels that can be enjoyed with friends '
                                               'and rivals alike '
                                               'through innovative fight mechanics.')

    def test_get_genres(self):
        genres = self.game_info.get_genres([4])
        self.assertEqual(genres, ['Fighting'])

    def test_get_game_keywords(self):
        keywords = self.game_info.get_game_keywords('Tekken 7')
        self.assertIsNotNone(keywords)
        self.assertEqual(keywords[0], 'mid')
        # The order of the keywords may vary
        self.assertIn('Fighting', keywords[1])

    def test_get_year_recency(self):
        # right now
        self.assertEqual(get_year_recency(time.time()), 'newest')
        # 4 years ago
        self.assertEqual(get_year_recency(time.time() - 4 * 365 * 24 * 60 * 60), 'recent')
        # 7 years ago
        self.assertEqual(get_year_recency(time.time() - 7 * 365 * 24 * 60 * 60), 'mid')
        # 10 years ago
        self.assertEqual(get_year_recency(time.time() - 10 * 365 * 24 * 60 * 60), 'early')
        # 15 years ago
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
