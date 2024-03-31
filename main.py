from game_info import GameInfo
from text_to_image import create_image

def get_input():
    anime_name = input("What is the full name of the anime character you want to generate an image of? ").lower().replace(',', ' ')
    # normalize the name to ascii
    anime_name = anime_name.encode('ascii', errors='ignore').decode()
    game_name = input(f"What is the full name of the game you want {anime_name} to be in? ").lower().replace(',', ' ')
    # normalize the name to ascii
    game_name = game_name.encode('ascii', errors='ignore').decode()
    facial_expression = input(f"What facial expression should {anime_name} have? (smile) ").lower()
    looking_at = input(f"What should {anime_name} be looking at? (viewer) ").lower()
    indoors = input(f"Should {anime_name} be indoors or outdoors? (indoors) ").lower()
    daytime = input(f"What time of day should it be? (night) ").lower()
    additional_tags = input(f"Any additional tags (separated with commas)? ").lower()
    return anime_name, game_name, facial_expression, looking_at, indoors, daytime, additional_tags