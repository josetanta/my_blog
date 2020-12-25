import os
import secrets
from PIL import Image
from flask import current_app


def save_upload(img, model='', size=350):
    name_token_img = secrets.token_hex(12)

    _, b_img = os.path.splitext(img.filename)
    t_img = name_token_img + b_img

    image_path = os.path.join(current_app.root_path,
                              f'static/uploads/{model}', t_img)
    save_img = Image.open(img)
    save_img.thumbnail((size, size))
    save_img.save(image_path)

    return t_img
