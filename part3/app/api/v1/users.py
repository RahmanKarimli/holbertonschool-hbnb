from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from part3.app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, describtion="Password of the user")
})

user_model_put = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, describtion="Password of the user")
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    # @jwt_required()
    def post(self):
        """Register a new user"""
        # claims = get_jwt()
        # if claims.get("is_admin", False) == False:
        #     return {'error': 'Admin privileges required'}, 403
        try:
            user_data = api.payload
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name,
                    'email': new_user.email}, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Users list retrieved successfully')
    def get(self):
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email} for
                user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model_put, validate=True)
    @api.response(200, "User successfully updated")
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims.get("is_admin"):
            user_data = api.payload

            if "email" in user_data:
                existing_user = facade.get_user_by_email(user_data["email"])
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400

            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name,
                    'email': updated_user.email}, 200

        if user_id != str(current_user):
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400

        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name,
                'email': updated_user.email}, 200
