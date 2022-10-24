from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    """
    Класс пользователей
    """
    def get(self):
        """
        Вывод пользователей
        """
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        """
        Добавление пользователя
        """
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    """
    Класс пользователь
    """
    def get(self, uid):
        """
        Вывод пользователя по id
        """
        r = user_service.get_one(uid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def delete(self, uid):
        """
        Удаление пользователя по id
        """
        user_service.delete(uid)
        return "", 204
