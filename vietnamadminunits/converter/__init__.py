from .converter_63_34 import convert_address_63_to_34

def convert_address(address: str, from_mode :int=63, to_mode :int=34):
    '''
    Converts an address written in the **old (63-province)** structure into an `AdminUnit` object using the **new (34-province)** system.

    :param address: The best structure is `(street), ward, district, province`. Don't worry too much about case or spelling.
    :param from_mode: Default to 63,
    :param to_mode: Default to 34.
    :return: AdminUnit object.
    '''
    if from_mode == 63 and to_mode == 34:
        return convert_address_63_to_34(address)
    else:
        raise Exception('Invalid mode. Currently, only 63 mode to 34 mode are supported.')