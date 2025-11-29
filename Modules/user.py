from dataclasses import dataclass, field
from typing import List

# Определение класса User
@dataclass(kw_only=True)
class User:
    id_user: int
    user_name: str
    user_viewed_films: List[str] = field(default_factory=list)
    user_genre: List[str] = field(default_factory=list)
    user_wish_list: List[str] = field(default_factory=list)
