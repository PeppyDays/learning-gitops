import os
from types import SimpleNamespace

import yaml

from cart.domain import CartRepository
from cart.infrastructure import FakeCartRepository


def _override_envs_to_database_config(config: dict) -> None:
    for key, value in config.items():
        if not isinstance(value, str):
            continue

        if value.startswith("${") and value.endswith("}"):
            env_key = value[2:-1]
            env_value = os.environ.get(env_key)

            if not env_value:
                raise ValueError(f"Environment variable {env_key} is not defined.")

            config[key] = env_value


config_file = "config.yaml"

with open(config_file, "r", encoding="utf8") as f:
    _config = SimpleNamespace(**yaml.safe_load(f))

_override_envs_to_database_config(_config.database)
_config.database["port"] = int(_config.database["port"])

for item in _config.items:
    item["cart_id"] = int(item["cart_id"])
    item["user_id"] = int(item["user_id"])
    item["price"] = int(item["price"])

_repository = FakeCartRepository(
    username=_config.database["username"],
    password=_config.database["password"],
    items=_config.items,
)


def get_repository() -> CartRepository:
    return _repository
