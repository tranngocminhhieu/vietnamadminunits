from .parser.parser_34 import parse_address_34
from .parser.parser_63 import parse_address_63
from .converter.convert_63_to_34 import convert_63_to_34


def parse_address(address: str, mode: int=34, keep_street: bool=True, level: int=2):
    '''
    Parse an address to an AdminUnit object.

    :param address: street, ward, (district), province.
    :param mode: 34 or 63.
    :param keep_street: Keep street after parsing.
    :param level: [1, 2] with 34 mode, and [1, 2, 3] with 63 mode.
    :return: AdminUnit object.
    '''
    if mode == 34:
        return parse_address_34(address, keep_street=keep_street, level=level)
    elif mode == 63:
        return parse_address_63(address, keep_street=keep_street, level=level)
    else:
        raise ValueError("Invalid mode. Use 63 or 34.")


def convert_address(address: str):
    return convert_63_to_34(address)