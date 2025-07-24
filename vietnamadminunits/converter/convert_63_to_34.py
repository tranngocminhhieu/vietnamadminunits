from ..parser.parser_63 import parse_address_63
from ..parser.parser_34 import parse_address_34

DICT_CONVERT_PROVINCE = {}
DICT_CONVERT_PROVINCE_DISTRICT_WARD = {}

def convert_63_to_34(address: str):
    unit = parse_address_63(address, keep_street=True, level=3)
    # DO CONVERT
    return unit