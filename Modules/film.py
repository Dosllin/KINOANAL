from dataclasses import dataclass, field
from typing import List

# Определение класса Film
@dataclass(kw_only=True)
class Film:
    id_film: int
    title: str
    genre: List[str] = field(default_factory=list)
    director: str
    year: int
    rating: List[int] = field(default_factory=list)
    description: str
    image: str
