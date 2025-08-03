import json
from pathlib import Path
import re

if __name__ == '__main__':
    from utils import key_normalize, extract_street, replace_from_right, unicode_normalize
    from objects import AdminUnit
else:
    from .utils import key_normalize, extract_street, replace_from_right, unicode_normalize
    from .objects import AdminUnit

# LOAD DATA
MODULE_DIR = Path(__file__).parent.parent
with open(MODULE_DIR / 'data/parser_from_2025.json', 'r') as f:
    parser_data = json.load(f)

DICT_PROVINCE = parser_data['DICT_PROVINCE']
DICT_PROVINCE_WARD_NO_ACCENTED = parser_data['DICT_PROVINCE_WARD_NO_ACCENTED']
DICT_PROVINCE_WARD_ACCENTED = parser_data['DICT_PROVINCE_WARD_ACCENTED']
DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED = parser_data['DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED']
DICT_UNIQUE_WARD_PROVINCE_ACCENTED = parser_data['DICT_UNIQUE_WARD_PROVINCE_ACCENTED']
DICT_PROVINCE_WARD_SHORT_ACCENTED = parser_data['DICT_PROVINCE_WARD_SHORT_ACCENTED']


province_keywords = sorted(sum([DICT_PROVINCE[k]['provinceKeywords'] for k in DICT_PROVINCE], []), key=len, reverse=True)
PATTERN_PROVINCE = re.compile('|'.join(province_keywords), flags=re.IGNORECASE)

unique_ward_no_accented_keywords = sorted(sum([DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED[k]['wardKeywords'] for k in DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED], []), key=len, reverse=True)
PATTERN_UNIQUE_WARD_PROVINCE_NO_ACCENTED = re.compile('|'.join(unique_ward_no_accented_keywords), flags=re.IGNORECASE)

unique_ward_accented_keywords = sorted(sum([DICT_UNIQUE_WARD_PROVINCE_ACCENTED[k]['wardKeywords'] for k in DICT_UNIQUE_WARD_PROVINCE_ACCENTED], []), key=len, reverse=True)
PATTERN_UNIQUE_WARD_PROVINCE_ACCENTED = re.compile('|'.join(unique_ward_accented_keywords), flags=re.IGNORECASE)




# MAIN FUNCTION
def parse_address_from_2025(address: str, keep_street :bool=True, level: int=2) -> AdminUnit:
    '''
    Parse an 34-province address to a unit.

    :param address: street, ward, province.
    :param keep_street: boolean.
    :param level: [1,2]
    :return: AdminUnit object.
    '''


    if level not in [1, 2]:
        raise ValueError('Level must be 1, or 2')

    unit = AdminUnit()

    address = unicode_normalize(address)
    address_key = key_normalize(address, keep=[','])
    address_key_accented = key_normalize(address, keep=[','], decode=False)
    ward_keyword = None
    ward_key = None
    street = None


    # Find province
    # match = PATTERN_PROVINCE.search(address_key)
    # province_keyword = match.group(0) if match else None
    province_keyword = next((m.group() for m in reversed(list(PATTERN_PROVINCE.finditer(address_key)))), None)

    # Xóa từ khóa ở chổ này là hợp lý (không mang xuống dưới), vì trường hợp 2 fallback ở dưới dành cho không tìm ra keyword trong address.
    if province_keyword:
        # Ưu tiên address_key_accented trước vì address_key là tham số
        address_key_accented = replace_from_right(text=address_key, old=province_keyword, new='', for_text=address_key_accented)
        address_key = replace_from_right(text=address_key, old=province_keyword, new='')

    province_key = next((k for k, v in DICT_PROVINCE.items() if province_keyword and province_keyword in [kw for kw in v['provinceKeywords']]), None)

    if not province_key:
        # match = PATTERN_UNIQUE_WARD_PROVINCE_NO_ACCENTED.search(address_key)
        # ward_keyword = match.group(0) if match else None
        ward_keyword = next((m.group() for m in reversed(list(PATTERN_UNIQUE_WARD_PROVINCE_NO_ACCENTED.finditer(address_key)))), None)

        ward_key = next((k for k, v in DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
        if ward_key:
            province_key = DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED[ward_key]['provinceKey']

    if not province_key:
        # match = PATTERN_UNIQUE_WARD_PROVINCE_ACCENTED.search(address_key_accented)
        # ward_keyword = match.group(0) if match else None
        ward_keyword = next((m.group() for m in reversed(list(PATTERN_UNIQUE_WARD_PROVINCE_ACCENTED.finditer(address_key_accented)))), None)

        ward_key = next((k for k, v in DICT_UNIQUE_WARD_PROVINCE_ACCENTED.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
        if ward_key:
            province_key = DICT_UNIQUE_WARD_PROVINCE_ACCENTED[ward_key]['provinceKey']

    if not province_key:
        return unit
    else:
        unit.province_key = province_key
        unit.province = DICT_PROVINCE[province_key]['province']
        unit.short_province = DICT_PROVINCE[province_key]['provinceShort']
        unit.latitude = DICT_PROVINCE[province_key]['provinceLat']
        unit.longitude = DICT_PROVINCE[province_key]['provinceLon']


    # Find ward
    if level == 2:
        DICT_WARD_NO_ACCENTED = DICT_PROVINCE_WARD_NO_ACCENTED.get(province_key)
        DICT_WARD_ACCENTED = DICT_PROVINCE_WARD_ACCENTED.get(province_key)
        DICT_WARD_SHORT_ACCENTED = DICT_PROVINCE_WARD_SHORT_ACCENTED.get(province_key)

        def find_ward(address_key, DICT_WARD):
            ward_keywords = sorted(sum([DICT_WARD[k]['wardKeywords'] for k in DICT_WARD], []), key=len, reverse=True)
            PATTERN_WARD = re.compile('|'.join(ward_keywords), flags=re.IGNORECASE)

            # match = PATTERN_WARD.search(address_key)
            # ward_keyword = match.group(0) if match else None
            ward_keyword = next((m.group() for m in reversed(list(PATTERN_WARD.finditer(address_key)))), None)

            if not ward_keyword:
                return None, None
            ward_key = next((k for k, v in DICT_WARD.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
            return ward_keyword, ward_key

        if not ward_key and DICT_WARD_NO_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key, DICT_WARD_NO_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_NO_ACCENTED

        if not ward_key and DICT_WARD_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key_accented, DICT_WARD_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_ACCENTED

        if not ward_key and DICT_WARD_SHORT_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key_accented, DICT_WARD_SHORT_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_SHORT_ACCENTED

        if ward_key:
            unit.ward_key = ward_key
            unit.ward = DICT_WARD[ward_key]['ward']
            unit.short_ward = DICT_WARD[ward_key]['wardShort']
            unit.ward_type = DICT_WARD[ward_key]['wardType']
            unit.latitude = DICT_WARD[ward_key]['wardLat']
            unit.longitude = DICT_WARD[ward_key]['wardLon']

            address_key = replace_from_right(address_key, key_normalize(ward_keyword), '')


    # Keep street
    if keep_street and address_key.count(',') >= 2:
        street = extract_street(address=address, address_key=address_key)
    if street:
        unit.street = street

    return unit

if __name__ == '__main__':
    # print(parse_address_34('Xã Nguyễn, Tỉnh Cao Bằng'))
    print(parse_address_from_2025('phuongandong,hcm'))