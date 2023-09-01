import abc
from dataclasses import dataclass
from typing import Callable


@dataclass
class Cart:
    cart_id: int
    user_id: int
    price: int

class CartRepository(abc.ABC):
    @abc.abstractmethod
    def find_by_cart_id(self, cart_id: int) -> Cart:
        pass

    @abc.abstractmethod
    def save(self, cart: Cart) -> Cart:
        pass


class Query(abc.ABC):
    ...


@dataclass(frozen=True)
class GetCartQuery(Query):
    cart_id: int


def read_query(query: Query, repository: CartRepository) -> Cart:
    reader: Callable[[Query, CartRepository], Cart] = QUERY_READER_REGISTRY[type(query)]
    return reader(query, repository)


def _get_cart_query_reader(query: GetCartQuery, repository: CartRepository) -> Cart:
    return repository.find_by_cart_id(query.cart_id)


QUERY_READER_REGISTRY = {
    GetCartQuery: _get_cart_query_reader,
}
