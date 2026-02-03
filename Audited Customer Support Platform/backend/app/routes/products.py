from fastapi import APIRouter
from app.db import products_col
from app.models.product import Product

router = APIRouter()

@router.post("/products")
async def create_product(product: Product):
    await products_col.insert_one(product.dict())
    return product

