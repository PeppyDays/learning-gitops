from typing import Annotated

from fastapi import APIRouter, Depends

from cart.container import get_repository
from cart.domain import Cart, CartRepository, GetCartQuery, read_query

router = APIRouter()


@router.get("/{cart_id}")
def get_cart(
    cart_id: int, repository: Annotated[CartRepository, Depends(get_repository)]
) -> Cart:
    query = GetCartQuery(cart_id=cart_id)
    cart = read_query(query, repository)
    return cart
