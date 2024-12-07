from part3.app.models import BaseModel
from part3.app.models.place import Place
from part3.app.models.user import User


class Review(BaseModel):
    def __init__(self, text: str, rating: int, place: Place, user: User):
        super().__init__()
        if not isinstance(text, str) or not text:
            raise ValueError("text must be a string")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")
        if not isinstance(place, Place) or not place in Place.places_set:
            raise ValueError("place must be an instance of Place")
        if not isinstance(user, User) or not user in User.users_set:
            raise ValueError("user must be an instance of User")
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
