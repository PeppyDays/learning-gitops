from order.domain import Order, OrderRepository


class FakeOrderRepository(OrderRepository):
    _credential: dict[str, str]
    _items: dict[int, Order]

    def __init__(
        self, username: str, password: str, items: list[dict[str, int]] = None
    ):
        self._credential = {"username": username, "password": password}

        if self._credential["username"] not in ["administrator", "order"]:
            raise ValueError(f"Invalid username from credential {self._credential}.")

        self._items = {}

        if items:
            for item in items:
                self._items[item["order_id"]] = Order(**item)

    def find_by_order_id(self, order_id: int) -> Order:
        return self._items.get(order_id)

    def save(self, order: Order) -> Order:
        self._items[order.order_id] = order
        return order
