import json
import requests
import io
import base64
from PIL import Image

url = "http://127.0.0.1:7860"


def fix(image):
    payload = {
        "resize_mode": 0,
        "show_extras_results": True,
        "gfpgan_visibility": 1,
        "codeformer_visibility": 0,
        "codeformer_weight": 0,
        "upscaling_resize": 2,
        "upscaling_resize_w": 512,
        "upscaling_resize_h": 512,
        "upscaling_crop": True,
        "upscaler_1": "None",
        "upscaler_2": "None",
        "extras_upscaler_2_visibility": 0,
        "upscale_first": False,
        "image": image
    }
    response = requests.post(url=f'{url}/sdapi/v1/extra-single-image', json=payload)

    r = response.json()
    result = r['image']
    image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
    image.save('i2i.png')
    return result.split(",", 1)[0]
