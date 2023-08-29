from typing import Annotated

from fastapi import APIRouter, Depends

from order.container import get_repository
from order.domain import GetOrderQuery, Order, OrderRepository, read_query

router = APIRouter()


@router.get("/{order_id}")
def get_order(
    order_id: int, repository: Annotated[OrderRepository, Depends(get_repository)]
) -> Order:
    query = GetOrderQuery(order_id=order_id)
    order = read_query(query, repository)
    return order
