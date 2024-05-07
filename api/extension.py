from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

bearer = "Bearer"
oauth2 = "oauth2"
authorizations = {
    bearer: {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    },
    oauth2: {
        "type": "oauth2",
        "flow": "password",
        "tokenUrl": "api/signin",
        "authorizationUrl": "api/signin",
    },
}

api = Api(
    prefix="/api",
    doc="/doc",
    ordered=True,
    validate=True,
    default_mediatype="application/json",
    authorizations=authorizations,
    security=[
        bearer,
        oauth2,
    ],
)
