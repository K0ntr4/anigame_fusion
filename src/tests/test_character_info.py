import unittest
from unittest.mock import patch, Mock
from src.image.character_info import (
    get_all_characters, get_closest_character, get_closest_characters
)


class TestCharacterFunctions(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.character_list = ["souryuu asuka langley", "warrior of light (ff14)"]

    @patch('requests.get')
    def test_get_all_characters(self, mock_get):
        mock_response = Mock()
        response_body = ("1girl, souryuu asuka langley, neon genesis evangelion\n"
                         "1girl, warrior of light \\(ff14\\), final fantasy\n"
                         "1girl, akiyama mio, k-on!\n"
                         "1girl, tifa lockhart, final fantasy\n"
                         "1girl, 2b \\(nier:automata\\), nier \\(series\\)\n"
                         "1girl, nakano azusa, k-on!\n"
                         "1girl, rem \\(re:zero\\), re:zero kara hajimeru isekai seikatsu\n"
                         "1girl, hirasawa yui, k-on!\n"
                         "1girl, gotoh hitori, bocchi the rock!\n"
                         "1girl, ayanami rei, neon genesis evangelion\n"
                         "1boy, male focus, joseph joestar, jojo no kimyou na bouken\n"
                         "1girl, matoi ryuuko, kill la kill\n"
                         "1girl, yor briar, spy x family\n"
                         "1girl, tainaka ritsu, k-on!\n")
        mock_response.text = response_body
        mock_get.return_value = mock_response

        characters = get_all_characters()

        self.assertIsInstance(characters, list)
        self.assertTrue(all(isinstance(c, str) for c in characters))

    @patch('requests.get')
    def test_get_closest_character(self, mock_get):
        mock_response = Mock()
        response_body = ("1girl, souryuu asuka langley, neon genesis evangelion\n"
                         "1girl, warrior of light \\(ff14\\), final fantasy\n"
                         "1girl, akiyama mio, k-on!\n"
                         "1girl, tifa lockhart, final fantasy\n"
                         "1girl, 2b \\(nier:automata\\), nier \\(series\\)\n"
                         "1girl, nakano azusa, k-on!\n"
                         "1girl, rem \\(re:zero\\), re:zero kara hajimeru isekai seikatsu\n"
                         "1girl, hirasawa yui, k-on!\n"
                         "1girl, gotoh hitori, bocchi the rock!\n"
                         "1girl, ayanami rei, neon genesis evangelion\n"
                         "1boy, male focus, joseph joestar, jojo no kimyou na bouken\n"
                         "1girl, matoi ryuuko, kill la kill\n"
                         "1girl, yor briar, spy x family\n"
                         "1girl, tainaka ritsu, k-on!\n")
        mock_response.text = response_body
        mock_get.return_value = mock_response
        closest_name = get_closest_character("Asuka Langley")

        self.assertEqual(closest_name, "1girl, souryuu asuka langley, neon genesis evangelion")

    @patch('requests.get')
    def test_get_closest_characters(self, mock_get):
        mock_response = Mock()
        response_body = ("1boy, male focus, uzumaki naruto, naruto \\(series\\)\n"
                         "1boy, male focus, uzumaki boruto, naruto \\(series\\)\n"
                         "1girl, uzumaki himawari, naruto \\(series\\)\n"
                         "1girl, carrot \\(one piece\\), one piece\n"
                         "1girl, uzumaki kushina, naruto \\(series\\)\n")
        mock_response.text = response_body
        mock_get.return_value = mock_response

        closest_names = get_closest_characters("Naruto Uzumaki", 3)

        self.assertEqual(closest_names, ['1boy, male focus, uzumaki naruto, naruto \\(series\\)',
                                         '1boy, male focus, uzumaki boruto, naruto \\(series\\)',
                                         '1girl, uzumaki himawari, naruto \\(series\\)'])

    @patch('requests.get')
    def test_get_closest_character_not_found(self, mock_get):
        mock_response = Mock()
        response_body = ("1boy, male focus, uzumaki naruto, naruto \\(series\\)\n"
                         "1boy, male focus, uzumaki boruto, naruto \\(series\\)\n"
                         "1girl, uzumaki himawari, naruto \\(series\\)\n"
                         "1girl, carrot \\(one piece\\), one piece\n"
                         "1girl, uzumaki kushina, naruto \\(series\\)\n")
        mock_response.text = response_body
        mock_get.return_value = mock_response
        closest_name = get_closest_character("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        self.assertIsNone(closest_name)


if __name__ == '__main__':
    unittest.main()
