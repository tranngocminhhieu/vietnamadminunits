from .converter_63_34 import convert_address_63_to_34

def convert_address(address: str, from_mode :int=63, to_mode :int=34):
    if from_mode == 63 and to_mode == 34:
        return convert_address_63_to_34(address)
    else:
        raise Exception('Invalid mode. Currently, only 63 mode to 34 mode are supported.')