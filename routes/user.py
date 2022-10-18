from fastapi import APIRouter, Response, status
from config.db import conn
from models.user import users
from schemas.user import User
from starlette.status import HTTP_204_NO_CONTENT

from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

# /users
user = APIRouter()


@user.get('/users', response_model=list[User], tags=["users"])
def get_users():
    return conn.execute(users.select()).fetchall()


@user.post('/users', response_model=User, tags=["users"])
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    print(result.lastrowid)
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.get('/users/{user_id}', response_model=User, tags=["users"])
def get_user(user_id: str):
    return conn.execute(
        users.select().where(users.c.id == user_id)).first()


@user.put('/users/{user_id}', response_model=User, tags=["users"])
def update_user(user_id: str, user: User):
    conn.execute(users.update().values(name=user.name,
                                       email=user.email,
                                       password=f.encrypt(user.password.encode("utf-8")))
                 .where(users.c.id == user_id))
    return conn.execute(users.select().where(users.c.id == user_id)).first()


@user.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(user_id: str):
    conn.execute(users.delete().where(users.c.id == user_id))
    return Response(status_code=HTTP_204_NO_CONTENT)
