from .v63provinces import parse_address as parse_address63
from .v34provinces import parse_address as parse_address34

def parse_address(address: str, keep_street=True, ver=34):
    if ver == 34:
        return parse_address34(address, keep_street=keep_street)
    else:
        return parse_address63(address, keep_street=keep_street)
