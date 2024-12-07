from flask import Flask
from flask_restx import Api

from config import DevelopmentConfig
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from part3.app.api.v1.amenities import api as amenities_ns
from part3.app.api.v1.users import api as users_ns
from part3.app.api.v1.places import api as places_ns
from part3.app.api.v1.reviews import api as reviews_ns
from part3.app.api.v1.auth import api as auth_ns

bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.config.from_object(config_class)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
