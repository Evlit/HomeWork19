from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from utils import admin_required, auth_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    """
    Класс жанров
    """
    @auth_required
    def get(self):
        """
        Вывод всех жанров
        """
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        """
        Добавление жанра
        """
        req_json = request.json
        genre = genre_service.create(req_json)
        return "", 201, {"location": f"/genres/{genre.id}"}


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    """
    Класс жанр
    """
    @auth_required
    def get(self, gid):
        """
        Вывод жанра по id
        """
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, gid):
        """
        Обновление жанра по id
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = gid
        genre_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, gid):
        """
        Удаление жанра по id
        """
        genre_service.delete(gid)
        return "", 204