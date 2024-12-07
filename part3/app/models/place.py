from part3.app.models import BaseModel
from part3.app.models.user import User


class Place(BaseModel):
    places_set = set()

    def __init__(self, title: str, description: str, price: float, latitude: float, longitude: float, owner: User):
        super().__init__()
        if not all([isinstance(title, str), len(title) > 0, len(title) < 100]):
            raise ValueError("Title must be 100 characters or less")
        if not all([price > 0]):
            raise ValueError("Price must be positive")
        if not all([isinstance(latitude, float), -90.0 <= latitude <= 90.0]):
            raise ValueError("Latitude must be within the range of -90 to 90")
        if not all([isinstance(longitude, float), -180.0 <= longitude <= 180.0]):
            raise ValueError("Longitude must be within the range of -180 to 180")
        if not all([isinstance(owner, User), owner in User.users_set]):
            raise ValueError("Owner must be User")
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
        Place.places_set.add(self)
        owner.add_place(self)

    def add_review(self, review):
        from part2.app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Review must be a valid Review instance")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        from part2.app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be a valid Amenity instance")
        self.amenities.append(amenity)

    def get_amenities(self):
        return [{"id": amenity.id, "name": amenity.name} for amenity in self.amenities]

    def get_reviews(self):
        return [{"id": review.id, "text": review.text, "rating": review.rating} for review in self.reviews]
