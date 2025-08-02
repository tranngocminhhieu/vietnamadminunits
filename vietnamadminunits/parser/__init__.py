from .parser_34 import parse_address_34
from .parser_63 import parse_address_63

def parse_address(address: str, mode: int=34, keep_street: bool=True, level: int=2):
    '''
    Parse an address to an AdminUnit object.

    :param address: The best structure is `(street), ward, (district), province`. Don't worry too much about case or spelling.
    :param mode: Modes `34` and `63` refer to administrative units. Mode `34` represents the new unit effective July 2025, while mode `63` refers to the former unit before the merger.
    :param keep_street: Keep the street after parsing, but this only works if the address includes enough commas: mode 63 requires at least 3 commas, while mode 34 requires at least 2.
    :param level: Use levels `1` and `2` with `mode=34`, and levels `1`, `2`, or `3` with `mode=63`, depending on the desired granularity.
    :return: AdminUnit object.
    '''
    if mode == 34:
        return parse_address_34(address, keep_street=keep_street, level=level)
    elif mode == 63:
        return parse_address_63(address, keep_street=keep_street, level=level)
    else:
        raise ValueError("Invalid mode. Use 63 or 34.")