# Представление для режиссеров
from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from utils import auth_required, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    """
    Класс режиссеров
    """
    @auth_required
    def get(self):
        """
        Вывод всех режиссеров
        """
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        """
        Добавление режиссера
        """
        req_json = request.json
        director = director_service.create(req_json)
        return "", 201, {"location": f"/directors/{director.id}"}


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    """
    Класс режиссер
    """
    @auth_required
    def get(self, did):
        """
        Вывод режиссера по id
        """
        r = director_service.get_one(did)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, did):
        """
        Обновление режиссера по id
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = did
        director_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, did):
        """
        Удаление режиссера по id
        """
        director_service.delete(did)
        return "", 204
