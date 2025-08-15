import json
from pathlib import Path
import re

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


# CREATE PATTERNS
province_keywords = sorted(sum([DICT_PROVINCE[k]['provinceKeywords'] for k in DICT_PROVINCE], []), key=len, reverse=True)
PATTERN_PROVINCE = re.compile('|'.join(province_keywords), flags=re.IGNORECASE)

unique_ward_no_accented_keywords = sorted(sum([DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED[k]['wardKeywords'] for k in DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED], []), key=len, reverse=True)
PATTERN_UNIQUE_WARD_PROVINCE_NO_ACCENTED = re.compile('|'.join(unique_ward_no_accented_keywords), flags=re.IGNORECASE)

unique_ward_accented_keywords = sorted(sum([DICT_UNIQUE_WARD_PROVINCE_ACCENTED[k]['wardKeywords'] for k in DICT_UNIQUE_WARD_PROVINCE_ACCENTED], []), key=len, reverse=True)
PATTERN_UNIQUE_WARD_PROVINCE_ACCENTED = re.compile('|'.join(unique_ward_accented_keywords), flags=re.IGNORECASE)


# MAIN FUNCTION
def parse_address_from_2025(address: str, keep_street :bool=True, level: int=2) -> AdminUnit:
    '''
    Parse an 34-province address to an AdminUnit object.

    :param address: (street), ward, province.
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


    # ----- PARSE PROVINCE -----

    # 1st attempt: Tìm province_keyword
    province_keyword = next((m.group() for m in reversed(list(PATTERN_PROVINCE.finditer(address_key)))), None)

    # Suy province_keyword ra province_key
    province_key = next((k for k, v in DICT_PROVINCE.items() if province_keyword and province_keyword in [kw for kw in v['provinceKeywords']]), None)

    # Nếu tìm ra province_keyword thì lặp tức xóa nó khỏi địa chỉ để tránh các level sau bắt nhầm từ khóa
    if province_keyword:
        address_key_accented = replace_from_right(text=address_key, old=province_keyword, new='', for_text=address_key_accented) #  Ưu tiên address_key_accented trước vì address_key là tham số
        address_key = replace_from_right(text=address_key, old=province_keyword, new='')


    # 2nd attempt: Nếu không tìm được province_keyword thì tìm ward_keyword (NO_ACCENTED), đây là những ward mà tên của nó là duy nhất, có thể suy ra được province
    if not province_key:
        ward_keyword = next((m.group() for m in reversed(list(PATTERN_UNIQUE_WARD_PROVINCE_NO_ACCENTED.finditer(address_key)))), None)

        # Suy ward_keyword ra ward_key
        ward_key = next((k for k, v in DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)

        # Suy ward_key ra province_key
        province_key = DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED.get(ward_key, {}).get('provinceKey')

        if province_key:
            DICT_WARD = DICT_PROVINCE_WARD_NO_ACCENTED.get(province_key) # Không dấu


    # 3rd attempt: Nếu không tìm được province_keyword thì tìm ward_keyword (ACCENTED), đây là những ward mà tên của nó là duy nhất, có thể suy ra được province
    if not province_key:
        ward_keyword = next((m.group() for m in reversed(list(PATTERN_UNIQUE_WARD_PROVINCE_ACCENTED.finditer(address_key_accented)))), None)

        # Suy ward_keyword ra ward_key
        ward_key = next((k for k, v in DICT_UNIQUE_WARD_PROVINCE_ACCENTED.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)

        # Suy ward_key ra province_key
        province_key = DICT_UNIQUE_WARD_PROVINCE_ACCENTED.get(ward_key, {}).get('provinceKey')

        if province_key:
            DICT_WARD = DICT_PROVINCE_WARD_ACCENTED.get(province_key) # Có dấu


    # Gán thông tin của province vào unit
    if province_key:
        unit.province_key = province_key
        unit.province = DICT_PROVINCE[province_key]['province']
        unit.short_province = DICT_PROVINCE[province_key]['provinceShort']
        unit.province_code = DICT_PROVINCE[province_key]['provinceCode']
        unit.latitude = DICT_PROVINCE[province_key]['provinceLat']
        unit.longitude = DICT_PROVINCE[province_key]['provinceLon']


    # ----- PARSE WARD -----
    if level == 2 and province_key:

        # Có đến 3 bộ ward
        DICT_WARD_NO_ACCENTED = DICT_PROVINCE_WARD_NO_ACCENTED.get(province_key) # Không dấu
        DICT_WARD_ACCENTED = DICT_PROVINCE_WARD_ACCENTED.get(province_key) # Có dấu
        DICT_WARD_SHORT_ACCENTED = DICT_PROVINCE_WARD_SHORT_ACCENTED.get(province_key) # Các ward này khi không dấu mà có type thì không sao, nhưng khi không có type thì không phân biệt được
        
        # Tạo một hàm vì tái sử dụng nhiều lần
        def find_ward(address_key, DICT_WARD):

            # Tìm ward_keyword
            ward_keywords = sorted(sum([DICT_WARD[k]['wardKeywords'] for k in DICT_WARD], []), key=len, reverse=True)
            PATTERN_WARD = re.compile('|'.join(ward_keywords), flags=re.IGNORECASE)
            ward_keyword = next((m.group() for m in reversed(list(PATTERN_WARD.finditer(address_key)))), None)

            # Suy ward_keyword ra ward_key
            ward_key = next((k for k, v in DICT_WARD.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
            return ward_keyword, ward_key


        # 1st attempt: Tìm không dấu trước vì nó là đa số
        if not ward_key and DICT_WARD_NO_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key, DICT_WARD_NO_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_NO_ACCENTED

        # 2nd attempt: Tìm có dấu
        if not ward_key and DICT_WARD_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key_accented, DICT_WARD_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_ACCENTED

        # 3rd attempt: Tìm có dấu với tên ngắn
        if not ward_key and DICT_WARD_SHORT_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key_accented, DICT_WARD_SHORT_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_SHORT_ACCENTED


        # Gán thông tin ward vào unit
        if ward_key:
            unit.ward_key = ward_key
            unit.ward = DICT_WARD[ward_key]['ward']
            unit.short_ward = DICT_WARD[ward_key]['wardShort']
            unit.ward_type = DICT_WARD[ward_key]['wardType']
            unit.ward_code = DICT_WARD[ward_key]['wardCode']
            unit.latitude = DICT_WARD[ward_key]['wardLat']
            unit.longitude = DICT_WARD[ward_key]['wardLon']


    # ----- STREET -----
    if keep_street and (ward_key or address_key.count(',') >= 2):
        street = extract_street(address=address, address_key=address_key, highest_level_keyword=ward_keyword)
    if street:
        unit.street = street

    return unit