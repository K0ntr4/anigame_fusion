from game_info import GameInfo
from text_to_image import create_image

def get_input():
    anime_name = input("What is the full name of the anime character you want to generate an image of? ").lower().replace(',', ' ')
    # Normalize the name to ASCII
    anime_name = anime_name.encode('ascii', errors='ignore').decode()
    game_name = input(f"What is the full name of the game you want {anime_name} to be in? ").lower().replace(',', ' ')
    # Normalize the name to ASCII
    game_name = game_name.encode('ascii', errors='ignore').decode()
    facial_expression = input(f"What facial expression should {anime_name} have? (smile) ").lower() or 'smile'
    looking_at = input(f"What should {anime_name} be looking at? (viewer) ").lower() or 'viewer'
    indoors = input(f"Should {anime_name} be indoors or outdoors? (indoors) ").lower() or 'indoors'
    daytime = input(f"What time of day should it be? (night) ").lower() or 'night'
    additional_tags = input(f"Any additional tags (separated with commas)? ").lower().split(',') if input else None
    return anime_name, game_name, facial_expression, looking_at, indoors, daytime, additional_tags

if __name__ == '__main__':
    anime_name, game_name, facial_expression, looking_at, indoors, daytime, additional_tags = get_input()
    game_info = GameInfo()
    recency, game_tags = game_info.get_game_keywords(game_name)
    res = create_image(recency, anime_name, game_name, game_tags, facial_expression, looking_at, indoors, daytime, additional_tags)
    print(f"Image saved as: {res}")