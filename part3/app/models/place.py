from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from part3.app.models import BaseModel
from part3.app.models.amenity import place_amenity_association
from part3.app.models.user import User


class Place(BaseModel):
    __tablename__ = "places"

    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", lazy=True)
    amenities = relationship("Amenity", secondary=place_amenity_association, back_populates="places")

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
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    def add_review(self, review):
        from part3.app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Review must be a valid Review instance")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        from part3.app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be a valid Amenity instance")
        self.amenities.append(amenity)

    def get_amenities(self):
        return [{"id": amenity.id, "name": amenity.name} for amenity in self.amenities]

    def get_reviews(self):
        return [{"id": review.id, "text": review.text, "rating": review.rating} for review in self.reviews]
