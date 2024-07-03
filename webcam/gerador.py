# gerador.py

import requests

def generate_image(prompt: str, output_file: str, api_key: str):
    print(f"Generating image with prompt: {prompt}")
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "png",  # Ensuring output format is PNG
        },
    )

    if response.status_code == 200:
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {output_file}")
    else:
        raise Exception(str(response.json()))
