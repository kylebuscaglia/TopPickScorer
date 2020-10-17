from typing import List

from pydantic import BaseModel


class PlayerStats(BaseModel):
    first_name: str
    last_name: str
    week: int


class PlayerStatsDto(BaseModel):
    players: List[PlayerStats]

