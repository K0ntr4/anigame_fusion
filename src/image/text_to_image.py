import torch
from diffusers import DiffusionPipeline


def create_image(image_params):
    pipe = DiffusionPipeline.from_pretrained(
        "cagliostrolab/animagine-xl-3.1",
        torch_dtype=torch.float16,
        use_safetensors=torch.cuda.is_available(),  # Use CUDA if available
    )

    if torch.cuda.is_available():
        pipe.to('cuda')

    prompt_parts = [
        image_params["recency"],
        "masterpiece", "best quality", "very aesthetic",
        image_params["gender"],
        image_params["anime_name"], "solo", "upper body", "v",
        image_params["facial_expression"], f"looking at {image_params['looking_at']}",
        image_params["indoors"], image_params["daytime"], image_params["game_name"],
        ', '.join(image_params["game_tags"]).lower()
    ]

    if image_params["additional_tags"]:
        prompt_parts.extend(image_params["additional_tags"])

    prompt = ", ".join(prompt_parts)

    negative_prompt = (
        "nsfw, lowres, (bad), text, error, fewer, extra, missing, "
        "worst quality, jpeg artifacts, low quality, watermark, "
        "unfinished, displeasing, oldest, early, chromatic aberration, "
        "signature, extra digits, artistic error, username, scan, [abstract]"
    )

    images = pipe(
        prompt,
        negative_prompt=negative_prompt,
        width=1024,
        height=1024,
        guidance_scale=7,
        num_inference_steps=28
    ).images

    filename = (
        f"./output/{image_params['anime_name'].replace(' ', '_')}_"
        f"{image_params['game_name'].replace(' ', '_')}.png"
    )

    return images, filename


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
        "additional_tags": ["fantasy", "adventure"]
    }

    result, output_filename = create_image(params)
    print(len(result))
    result[0].show()
