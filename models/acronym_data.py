
from dataclasses import dataclass


@dataclass
class AcronymData:
    acronym: str
    definition: str
    context: str
    example: str
    importance: str
    related: list[str]