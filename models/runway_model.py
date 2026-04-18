from dataclasses import dataclass

@dataclass
class Runway:
    bearing_1 : int
    bearing_2 : int
    ident_1 : str
    ident_2 : str
    length_ft : int
    lights : bool
    surface : str

    