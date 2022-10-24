# Сервис ПОЛЬЗОВАТЕЛИ
import datetime
import hashlib
import calendar

import jwt

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d['password'] = self.get_hash(user_d.get('password'))
        return self.dao.create(user_d)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def get_tokens(self, data):
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, PWD_HASH_SALT, algorithm='HS256')
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, PWD_HASH_SALT, algorithm='HS256')
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens

    def auth_user(self, username, password):
        user = self.dao.get_one_by_username(username)
        if not user:
            return "Нет пользователя с таким логином",401

        passwd_new = self.get_hash(password)
        if passwd_new != user.password:
            return "Неверный пароль",401

        data = {
            "username": user.username,
            "role": user.role
        }
        return self.get_tokens(data)

    def check_token(self, token):
        try:
            data = jwt.decode(token, PWD_HASH_SALT, algorithms='HS256')
            return self.get_tokens(data)
        except Exception as e:
            return e




