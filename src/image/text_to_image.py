import torch
from diffusers import DiffusionPipeline

NEGATIVE_PROMPT = (
    "nsfw, lowres, (bad), text, error, fewer, extra, missing, "
    "worst quality, jpeg artifacts, low quality, watermark, "
    "unfinished, displeasing, oldest, early, chromatic aberration, "
    "signature, extra digits, artistic error, username, scan, [abstract]"
)
MODEL = "cagliostrolab/animagine-xl-3.1"


def show_results(images):
    print(len(images))
    for img in images:
        img.show()


def create_image(image_params):
    """
    Create an anime-style image based on the provided parameters.

    Args:
        image_params (dict): A dictionary containing parameters for image generation, including:
            - 'recency': The recency of the character (e.g., 'recent', 'classic', 'retro').
            - 'anime_name': The name of the anime character.
            - 'processed_anime_name': The processed names of the anime character.
            - 'game_name': The name of the game associated with the character.
            - 'game_tags': A list of tags describing the game.
            - 'facial_expression': The facial expression of the character.
            - 'looking_at': The direction the character is looking at.
            - 'indoors': Whether the scene is indoors or outdoors.
            - 'daytime': Whether it's daytime or nighttime.
            - 'additional_tags': Additional tags to provide more context for image generation.

    Returns:
        tuple: A tuple containing the generated images and the output filename.
    """
    pipe = DiffusionPipeline.from_pretrained(
        MODEL,
        torch_dtype=torch.float16,
        use_safetensors=torch.cuda.is_available(),
    )

    if torch.cuda.is_available():
        pipe.to('cuda')

    prompt_parts = [
        image_params.get('recency', ''),
        "masterpiece", "best quality", "very aesthetic",
        image_params.get('gender', ''),
        "solo", "upper body", "v",
        image_params.get('facial_expression', ''),
        f"looking at {image_params.get('looking_at', '')}",
        image_params.get('indoors', ''),
        image_params.get('daytime', ''),
        image_params.get('game_name', ''),
        ', '.join(image_params.get('game_tags', [])).lower(),
        image_params.get('additional_tags', '').lower()
    ]
    prompt_parts = [part.lower() for part in prompt_parts if part]

    images = []
    for name in image_params.get('processed_anime_name', image_params['anime_name']):
        images += pipe(
            prompt=", ".join(prompt_parts[:4] + [name] + prompt_parts[4:]),
            negative_prompt=NEGATIVE_PROMPT,
            width=1024,
            height=1024,
            guidance_scale=7,
            num_inference_steps=28
        ).images

    return images, (f"./output/{image_params['anime_name'].replace(' ', '_')}_"
                    f"{image_params['game_name'].replace(' ', '_')}")


if __name__ == "__main__":
    params = {
        "recency": "recent",
        "anime_name": "Naruto Uzumaki",
        "gender": "1boy",
        "game_name": "Final Fantasy VII",
        "game_tags": ["Action", "RPG"],
        "facial_expression": "smiling",
        "looking_at": "camera",
        "indoors": "indoors",
        "daytime": "night",
        "additional_tags": "fantasy, adventure"
    }
    params2 = {
        "recency": "recent",
        "processed_anime_name": ['1boy, male focus, uzumaki naruto, naruto \\(series\\)',
                                 '1boy, male focus, uzumaki boruto, naruto \\(series\\)',
                                 '1girl, uzumaki himawari, naruto \\(series\\)'],
        "anime_name": "Naruto Uzumaki",
        "game_name": "Final Fantasy VII",
        "game_tags": ["Action", "RPG"],
        "facial_expression": "smiling",
        "looking_at": "camera",
        "indoors": "indoors",
        "daytime": "night",
        "additional_tags": "fantasy, adventure"
    }

    first_result, first_output_filename = create_image(params)
    second_result, second_output_filename = create_image(params2)
    show_results(first_result)
    show_results(second_result)
