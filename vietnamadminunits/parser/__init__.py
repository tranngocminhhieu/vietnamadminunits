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

def parse_address(address: str, mode: Union[str, ParseMode]=ParseMode.latest(), keep_street: bool=True, level: int=2):
    '''
    Parse an address to an AdminUnit object.

    :param address: The best structure is `(street), ward, (district), province`. Don't worry too much about case or accenting.
    :param mode: One of the `ParseMode` values. Use `'LEGACY'` for the 63-province format (pre-merger), or `'FROM_2025'` for the new 34-province format. Default is `ParseMode.latest()`.
    :param keep_street: Keep the street after parsing, but this only works if the address includes enough commas: `'LEGACY'` mode requires at least 3 commas, while `'FROM_2025'` mode requires at least 2.
    :param level: Use levels `1` and `2` with `'FROM_2025'` mode, and levels `1`, `2`, or `3` with `'LEGACY'` mode, depending on the desired granularity.
    :return: AdminUnit object.
    '''

    if mode in [ParseMode.FROM_2025, ParseMode.FROM_2025.value]:
        return parse_address_from_2025(address, keep_street=keep_street, level=level)
    elif mode in [ParseMode.LEGACY, ParseMode.LEGACY.value]:
        return parse_address_legacy(address, keep_street=keep_street, level=level)
    else:
        raise ValueError(f"Invalid mode. Available modes are {ParseMode.available(value=True)}.")