import os
import secrets
from PIL import Image
from flask import current_app, url_for

def save_upload_post(img):
	name_token_img = secrets.token_hex(12)

	_, b_img = os.path.splitext(img.filename)
	t_img = name_token_img + b_img

	image_path = os.path.join(current_app.root_path,'html/static/uploads/posts' , t_img)
	save_img = Image.open(img)
	save_img.thumbnail((550,550))
	save_img.save(image_path)

	return t_img


def save_upload_user(img):
	name_token_img = secrets.token_hex(12)

	_, b_img = os.path.splitext(img.filename)
	t_img = name_token_img + b_img

	image_path = os.path.join(current_app.root_path,'html/static/uploads/users' , t_img)
	save_img = Image.open(img)
	save_img.thumbnail((300,300))
	save_img.save(image_path)

	return t_img