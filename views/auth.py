from flask import request
from flask_restx import Resource, Namespace, abort

from implemented import user_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    """
    Класс аутентификации
    """
    def post(self):
        """
        Получение токенов при успешной проверке логина и пароля
        """
        req_json = request.json
        username = req_json.get('username')
        password = req_json.get('password')
        if not username and not password:
            abort(400)

        return user_service.auth_user(username, password), 201

    def put(self):
        """
        Обновление refresh токена
        """
        req_json = request.json
        refresh_token = req_json.get('refresh_token')
        if not refresh_token:
            abort(400)

        return user_service.check_token(refresh_token), 201
