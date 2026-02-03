from pydantic import BaseModel
from uuid import uuid4

class Product(BaseModel):
    id: str = str(uuid4())
    name: str
    price: float
