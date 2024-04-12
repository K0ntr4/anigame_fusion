import unittest
from src.image.character_info import get_all_characters, get_closest_character


class TestCharacterFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.character_list = ["souryuu asuka langley", "warrior of light (ff14)"]

    def test_get_all_characters(self):
        characters = get_all_characters()

        self.assertIsInstance(characters, list)
        self.assertTrue(all(isinstance(c, str) for c in characters))

    def test_get_closest_character(self):
        closest_name = get_closest_character("Asuka Langley")

        self.assertEqual(closest_name, "1girl, souryuu asuka langley, neon genesis evangelion")

    def test_get_closest_character_not_found(self):
        closest_name = get_closest_character("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        self.assertIsNone(closest_name)


if __name__ == '__main__':
    unittest.main()
