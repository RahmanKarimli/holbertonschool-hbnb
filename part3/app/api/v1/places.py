from flask_restx import Namespace, Resource, fields
from part3.app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # Placeholder for the logic to register a new place
        try:
            place_data = api.payload
            new_place = facade.create_place(place_data)
            return {'title': new_place.title, 'owner': new_place.owner.id, 'description': new_place.description,
                    'price': new_place.price, }, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        places = facade.get_all_places()
        return [{'id': place.id, 'title': place.title,
                 'latitude': place.latitude, 'longitude': place.longitude, } for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID, including associated owner and amenities
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'id': place.id, 'title': place.title,
                'owner': {"id": place.owner.id, "first_name": place.owner.first_name,
                          "last_name": place.owner.last_name, "email": place.owner.email},
                'description': place.description,
                'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude,
                'amenities': place.get_amenities()}, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        try:
            place_data = api.payload
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            return {'id': updated_place.id, 'title': updated_place.title,
                    'owner': {"id": updated_place.owner.id, "first_name": updated_place.owner.first_name,
                              "last_name": updated_place.owner.last_name, "email": updated_place.owner.email},
                    'description': updated_place.description,
                    'price': updated_place.price, 'latitude': updated_place.latitude, 'longitude': updated_place.longitude,
                    'amenities': updated_place.get_amenities()}, 200
        except ValueError as e:
            return {'message': str(e)}, 400