import os

import requests
from flask import Flask, json, Response
from flask import request
from flask import make_response
from flask_mongoengine import MongoEngine
from flask_expects_json import expects_json
from datetime import datetime
from typing import Any, Hashable, Iterable, Optional

from mongoengine import EmbeddedDocumentField, ReferenceField

UPLOAD_FOLDER = 'static/files'
ONSALE_DATE = "onsaleDate"
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__, template_folder='template')
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '3l2gribj4YoX9ZEgF0nIWnV7pmpwHXEy0QE6i9njoOrpWDBVkf'

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://' + os.environ.get("MONGO_USER") + '@' + os.environ.get("MONGO_HOST") + ':' + os.environ.get(
        "MONGO_PORT") + '/' + os.environ.get("MONGO_DB"),
    "username": os.environ.get("MONGO_USER"),
    "password": os.environ.get("MONGO_PASS"),
}

db = MongoEngine(app)

if __name__ == "__main__":
    app.run()

schemaComicRegister = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "imagen": {"type": "string"},
        "name": {"type": "string"},
        "onsaleDate": {"type": "string"},
        "personaje": {"type": "string"},
    },
    "required": ["id", "imagen", "name", "onsaleDate"]
}


@app.route('/api/addToLayaway', methods=["POST"])
@app.route('/api/addToLayaway/', methods=["POST"])
@expects_json(schemaComicRegister)
def comic_store():
    auth = request.headers.get('Authorization')
    if not auth:
        return make_response({"mensaje": 'could not verify'}, 401,
                             {'WWW.Authentication': 'Basic realm: "login required"'})
    user_url = os.environ.get("USER_URL")
    comic_url = os.environ.get("COMIC_URL")
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': auth,
    }
    response = requests.request("GET", user_url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        email = response_json["email"]
        userExist = User.objects(email=email).first()
        if userExist is not None:
            name = request.json.get("name", None)
            character = request.json.get("character", None)
            order = request.json.get("order", "desc")
            by = request.json.get("by", "name")
            if order == 'desc':
                by = "-" + by
            if name is not None:
                print(name)
                comics = Comics.objects(name__contains=name, user=userExist.id).order_by(by).all()
            elif character is not None:
                print(character)
                comics = Comics.objects(character__contains=character, user=userExist.id).order_by(by).all()
            else:
                comics = Comics.objects(user=userExist.id).order_by(by).all()
            print(comics)
            if len(comics) > 0:
                c = []
                for comic in comics:
                    c.append({
                        "id": str(comic.id),
                        "comic_id": str(comic.comic_id),
                        "name": str(comic.name),
                        "created_at": comic.created_at,
                        "imagen": comic.imagen,
                        "onsaleDate": comic.onsaleDate,
                    })
                return Response(response=json.dumps(c), status=201, mimetype='application/json')
            else:
                response = {
                    "mensaje": "No se encontro ningun resultado en la busqueda"
                }
        else:
            response = {
                "mensaje": "El usuario no existe, y no se puede agregar"
            }
    else:
        response = {
            "mensaje": "Usuario invalido"
        }
    return Response(response=json.dumps(response), status=400, mimetype='application/json')


def buscar_dicc(it: Iterable[dict], clave: Hashable, valor: Any) -> Optional[dict]:
    for dicc in it:
        if dicc[clave] == valor:
            return dicc
    return None


class User(db.Document):
    __tablename__ = 'users'
    name = db.StringField(required=True)
    age = db.IntField()
    email = db.StringField()
    password = db.StringField()
    meta = {
        'indexes': [
            'email',  # single-field index
        ]
    }


class Comics(db.Document):
    comic_id = db.IntField()
    name = db.StringField()
    imagen = db.StringField()
    onsaleDate = db.StringField()
    character = db.StringField()
    created_at = db.DateTimeField(default=datetime.utcnow)
    user = db.ReferenceField(User)
