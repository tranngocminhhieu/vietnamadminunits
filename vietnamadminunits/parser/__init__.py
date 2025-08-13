from .parser_from_2025 import parse_address_from_2025
from .parser_legacy import parse_address_legacy
from enum import Enum
from typing import Union

class ParseMode(Enum):
    LEGACY = "LEGACY"
    FROM_2025 = "FROM_2025"

    @classmethod
    def latest(cls):
        merger_modes = [m for m in cls if '_20' in m.name]
        return max(merger_modes, key=lambda m: int(m.value.split("_")[1]))

    @classmethod
    def available(cls, value=False):
        attrs = list(cls)
        if value:
            attrs = [a.value for a in attrs]
        return attrs

def parse_address(address: str, mode: Union[str, ParseMode]=ParseMode.latest(), keep_street: bool=True, level: int=0):
    '''
    Parse an address to an AdminUnit object.

    :param address: Best format *"(street), ward, (district), province"*. Case is ignored, accents are usually ignored except in rare cases.
    :param mode: `'FROM_2025'` (34-province) or `'LEGACY'` (63-province). Default `ParseMode.latest()`.
    :param keep_street: Keep the street in the result, works only if there are enough commas: 2+ for *FROM_2025* mode, 3+ for *LEGACY* mode.
    :param level: *FROM_2025* mode accepts `1` or `2`. *LEGACY* mode accepts `1`, `2`, or `3`. Default `0` for highest level automatically.
    :return: AdminUnit object.
    '''

    if mode in [ParseMode.FROM_2025, ParseMode.FROM_2025.value]:
        level = 2 if not level else level
        return parse_address_from_2025(address, keep_street=keep_street, level=level)
    elif mode in [ParseMode.LEGACY, ParseMode.LEGACY.value]:
        level = 3 if not level else level
        return parse_address_legacy(address, keep_street=keep_street, level=level)
    else:
        raise ValueError(f"Invalid mode. Available modes are {ParseMode.available(value=True)}.")