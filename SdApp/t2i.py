import json
import requests
import io
import base64
from PIL import Image

url = "http://127.0.0.1:7860"

payload = {
    "prompt": "puppy dog",
    "steps": 5
}


def gen(text, step):
    payload = {
        "prompt": text,
        "steps": step
    }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()
    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    image.save('t2i.png')
    return r['images'][0]

