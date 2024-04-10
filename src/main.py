import PySimpleGUI as sg
from game_info import GameInfo
from text_to_image import create_image

def get_input():
    layout = [
        [sg.Text("What is the full name of the anime character you want to generate an image of?")],
        [sg.InputText(key="anime_name")],
        [sg.Text("What gender do you want the character to be? (1boy/1girl)")],
        [sg.InputText("1boy", key="gender")],
        [sg.Text("What is the full name of the game you want the character to be in?")],
        [sg.InputText(key="game_name")],
        [sg.Text("What facial expression should the character have? (smile)")],
        [sg.InputText("smile", key="facial_expression")],
        [sg.Text("What should the character be looking at? (viewer)")],
        [sg.InputText("viewer", key="looking_at")],
        [sg.Text("Should the character be indoors or outdoors? (indoors)")],
        [sg.InputText("indoors", key="indoors")],
        [sg.Text("What time of day should it be? (night)")],
        [sg.InputText("night", key="daytime")],
        [sg.Text("Any additional tags (separated with commas)?")],
        [sg.InputText(key="additional_tags")],
        [sg.Button("Generate Image")]
    ]

    window = sg.Window("Anime Character Image Generator", layout)

    event, values = window.read()
    window.close()
    if event == "Generate Image":
        anime_name = values["anime_name"].lower().replace(',', ' ')
        gender = values["gender"]
        game_name = values["game_name"].lower().replace(',', ' ').replace(':', '')
        facial_expression = values["facial_expression"]
        looking_at = values["looking_at"]
        indoors = values["indoors"]
        daytime = values["daytime"]
        additional_tags = values["additional_tags"].lower().split(',') \
            if values["additional_tags"] else None
        game_info = GameInfo()
        recency, game_tags = game_info.get_game_keywords(game_name)
        return {
            "recency": recency,
            "gender": gender,
            "anime_name": anime_name,
            "game_name": game_name,
            "game_tags": game_tags,
            "facial_expression": facial_expression,
            "looking_at": looking_at,
            "indoors": indoors,
            "daytime": daytime,
            "additional_tags": additional_tags
        }
    return None


if __name__ == '__main__':
    input_values = get_input()
    if input_values:
        output_filename = create_image(input_values)
        print(f"Image saved as: {output_filename}")
