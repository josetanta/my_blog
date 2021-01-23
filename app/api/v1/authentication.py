from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from . import v1
from app import csrf


@v1.route('/signin', methods=['POST'])
def login():
    return jsonify({'message': "Hola"})
