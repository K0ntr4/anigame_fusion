import torch
from diffusers import DiffusionPipeline

def create_image(recency, anime_name, game_name, game_tags, facial_expression, looking_at, indoors, daytime, additional_tags):
    pipe = DiffusionPipeline.from_pretrained(
        "cagliostrolab/animagine-xl-3.1",
        torch_dtype=torch.float16,
        use_safetensors=True,
    )
    if torch.cuda.is_available():
        pipe.to('cuda')

    prepend = f"{recency}, masterpiece, best quality, very aesthetic"
    prompt = prepend + f"1boy, {anime_name}, solo, upper body, v, {facial_expression}, looking at {looking_at}, {indoors}, {daytime}, {game_name}, {', '.join(game_tags).lower()}, {', '.join(additional_tags)}"
    negative_prompt = "nsfw, lowres, (bad), text, error, fewer, extra, missing, worst quality, jpeg artifacts, low quality, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]"

    image = pipe(
        prompt,
        negative_prompt=negative_prompt,
        width=1024,
        height=1024,
        guidance_scale=7,
        num_inference_steps=28
    ).images[0]

    image.save(f"./output/{anime_name + '_' + game_name}.png")