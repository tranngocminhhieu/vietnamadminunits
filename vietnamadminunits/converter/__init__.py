from .converter_63_34 import convert_address_63_to_34
from enum import Enum
from typing import Union


class ConvertMode(Enum):
    CONVERT_2025 = "CONVERT_2025"  # From LEGACY → MERGER_2025

    @classmethod
    def available(cls, value=False):
        attrs = list(cls)
        if value:
            attrs = [a.value for a in attrs]
        return attrs


def convert_address(address: str, mode: Union[str, ConvertMode]=ConvertMode.CONVERT_2025):
    '''
    Converts an address written in the **old (63-province)** structure into an `AdminUnit` object using the **new (34-province)** system.

    :param address: The best structure is `(street), ward, district, province`. Don't worry too much about case or spelling.
    :return: AdminUnit object.
    '''

    if mode in [ConvertMode.CONVERT_2025, ConvertMode.CONVERT_2025.value]:
        return convert_address_63_to_34(address)
    else:
        raise Exception(f"Invalid mode. Available modes are {ConvertMode.available(value=True)}.")