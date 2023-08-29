import abc
from dataclasses import dataclass
from typing import Callable


@dataclass
class Order:
    order_id: int
    user_id: int
    price: int


class OrderRepository(abc.ABC):
    @abc.abstractmethod
    def find_by_order_id(self, order_id: int) -> Order:
        pass

    @abc.abstractmethod
    def save(self, cart: Order) -> Order:
        pass


class Query(abc.ABC):
    ...


@dataclass(frozen=True)
class GetOrderQuery(Query):
    order_id: int


def read_query(query: Query, repository: OrderRepository) -> Order:
    reader: Callable[[Query, OrderRepository], Order] = QUERY_READER_REGISTRY[
        type(query)
    ]
    return reader(query, repository)


def _get_order_query_reader(query: GetOrderQuery, repository: OrderRepository) -> Order:
    return repository.find_by_order_id(query.order_id)


QUERY_READER_REGISTRY = {
    GetOrderQuery: _get_order_query_reader,
}
