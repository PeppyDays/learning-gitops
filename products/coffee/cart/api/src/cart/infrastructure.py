from cart.domain import Cart, CartRepository


class FakeCartRepository(CartRepository):
    _credential: dict[str, str]
    _items: dict[int, Cart]

    def __init__(
        self, username: str, password: str, items: list[dict[str, int]] = None
    ):
        self._credential = {"username": username, "password": password}

        if self._credential["username"] not in ["administrator", "cart"]:
            raise ValueError(f"Invalid username from credential {self._credential}.")

        self._items = {}

        if items:
            for item in items:
                self._items[item["cart_id"]] = Cart(**item)

    def find_by_cart_id(self, cart_id: int) -> Cart:
        return self._items.get(cart_id)

    def save(self, cart: Cart) -> Cart:
        self._items[cart.cart_id] = cart
        return cart
