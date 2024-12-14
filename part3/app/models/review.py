from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from part3.app.models import BaseModel
from part3.app.models.place import Place
from part3.app.models.user import User


class Review(BaseModel):
    __tablename__ = "reviews"

    text = Column(String(200), nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(36), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)

    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __init__(self, text: str, rating: int, place: Place, user: User):
        super().__init__()
        if not isinstance(text, str) or not text:
            raise ValueError("text must be a string")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
