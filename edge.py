from typing import Any


class Edge(object):
    def __init__(self, weight: int, value: Any) -> None:
        self._weight = weight
        self._value = value

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("TODO")
        self._weight = value

    @property
    def value(self) -> Any:
        return self._value

    def normalized(self, maximum: int) -> float:
        return self._weight / maximum

    def __repr__(self):
        return f"Weight: {self._weight} Translations: {self._value}"