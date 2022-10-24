# описание декораторов авторизации
import jwt
from flask import request
from flask_restx import abort
from constants import PWD_HASH_SALT

algo = 'HS256'


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, PWD_HASH_SALT, algorithms=[algo])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        role = None
        try:
            user = jwt.decode(token, PWD_HASH_SALT, algorithms=[algo])
            role = user.get("role")
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        if role != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper
