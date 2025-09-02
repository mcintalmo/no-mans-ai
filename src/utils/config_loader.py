import yaml
from typing import Any


def load_config(path: str) -> Any:
    with open(path, "r") as f:
        return yaml.safe_load(f)
