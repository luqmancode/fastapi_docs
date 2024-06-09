from pydantic import BaseModel
from enum import Enum
from typing import Union

class ItemModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    has_offer: Union[bool, None] = None
    tags: list[str] | None = None

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    leenet = "leenet"