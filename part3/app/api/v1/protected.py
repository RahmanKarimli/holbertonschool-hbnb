from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

api = Namespace('protected', description='Protected sources')


@api.route('')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's ID (now always a string)
        claims = get_jwt()  # Retrieve additional claims from the token

        is_admin = claims.get("is_admin", False)  # Access the 'is_admin' claim

        return {'message': f'Hello, user {current_user}, is_admin: {is_admin}'}, 200
