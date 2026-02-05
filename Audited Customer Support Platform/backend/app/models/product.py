from pydantic import BaseModel
from uuid import uuid4
from pydantic import Field

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    price: float
