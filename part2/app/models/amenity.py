from part2.app.models import BaseModel


class Amenity(BaseModel):
    amenities_set = set()

    def __init__(self, name: str):
        super().__init__()
        if not isinstance(name, str) or not len(name) < 50:
            raise ValueError("Name is required and must be 50 characters or fewer")
        self.name = name
        Amenity.amenities_set.add(self)
