import json
from pathlib import Path
import re

if __name__ == '__main__':
    from utils import key_normalize, extract_street, replace_from_right, unicode_normalize
    from objects import AdminUnit
else:
    from .utils import key_normalize, extract_street, replace_from_right, unicode_normalize
    from .objects import AdminUnit


# LOAD PICKLE DATA
MODULE_DIR = Path(__file__).parent.parent
with open(MODULE_DIR / 'data/parser_63.json', 'r') as f:
    parser_data = json.load(f)

DICT_PROVINCE = parser_data['DICT_PROVINCE']
DICT_PROVINCE_DISTRICT = parser_data['DICT_PROVINCE_DISTRICT']
DICT_UNIQUE_DISTRICT_PROVINCE = parser_data['DICT_UNIQUE_DISTRICT_PROVINCE']
DICT_PROVINCE_DISTRICT_WARD_NO_ACCENTED = parser_data['DICT_PROVINCE_DISTRICT_WARD_NO_ACCENTED']
DICT_PROVINCE_DISTRICT_WARD_ACCENTED = parser_data['DICT_PROVINCE_DISTRICT_WARD_ACCENTED']


province_keywords = sorted(sum([DICT_PROVINCE[k]['provinceKeywords'] for k in DICT_PROVINCE], []), key=len, reverse=True)
PATTERN_PROVINCE = re.compile('|'.join(province_keywords), flags=re.IGNORECASE)

unique_district_keys = sorted(sum([DICT_UNIQUE_DISTRICT_PROVINCE[k]['districtKeywords'] for k in DICT_UNIQUE_DISTRICT_PROVINCE], []), key=len, reverse=True)
PATTERN_UNIQUE_DISTRICT = re.compile('|'.join(unique_district_keys), flags=re.IGNORECASE)


# MAIN FUNCTION
def parse_address_63(address, keep_street=True, level=3):
    unit = AdminUnit(show_district=True)

    address = unicode_normalize(address)
    address_key = key_normalize(address, keep=[','])
    address_key_accented = key_normalize(address, keep=[','], decode=False)

    district_key = None
    ward_key = None
    ward_keyword = None
    street = None

    # Find province
    match = PATTERN_PROVINCE.search(address_key)
    province_keyword = match.group(0) if match else None
    if province_keyword:
        address_key = replace_from_right(address_key, province_keyword, '')
    province_key = next((k for k, v in DICT_PROVINCE.items() if province_keyword and province_keyword in [kw for kw in v['provinceKeywords']]), None)

    if not province_key:
        match = PATTERN_UNIQUE_DISTRICT.search(address_key)
        district_keyword = match.group(0) if match else None
        if district_keyword:
            address_key = replace_from_right(address_key, district_keyword, '')
        district_key = next((k for k, v in DICT_UNIQUE_DISTRICT_PROVINCE.items() if district_keyword and district_keyword in [kw for kw in v['districtKeywords']]), None)
        if district_key:
            province_key = DICT_UNIQUE_DISTRICT_PROVINCE[district_key]['provinceKey']

    if not province_key:
        return unit
    else:
        unit.province_key = province_key
        unit.province = DICT_PROVINCE[province_key]['province']
        unit.short_province = DICT_PROVINCE[province_key]['provinceShort']

    if level == 1:
        return unit


    # Find district
    DICT_DISTRICT = DICT_PROVINCE_DISTRICT[province_key]
    if not district_key:
        district_keywords = sorted(sum([DICT_DISTRICT[k]['districtKeywords'] for k in DICT_DISTRICT], []), key=len, reverse=True)
        PATTERN_DISTRICT = re.compile('|'.join(re.escape(k) for k in district_keywords), flags=re.IGNORECASE)
        match = PATTERN_DISTRICT.search(address_key)
        district_keyword = match.group(0) if match else None
        if district_keyword:
            address_key = replace_from_right(address_key, district_keyword, '')
        district_key = next((k for k, v in DICT_DISTRICT.items() if district_keyword and district_keyword in [kw for kw in v['districtKeywords']]), None)

    if not district_key:
        return unit
    else:
        unit.district_key = district_key
        unit.district = DICT_DISTRICT[district_key]['district']
        unit.short_district = DICT_DISTRICT[district_key]['districtShort']
        unit.district_type = DICT_DISTRICT[district_key]['districtType']

    if level == 2:
        return unit


    # Find ward
    DICT_WARD_NO_ACCENTED =  DICT_PROVINCE_DISTRICT_WARD_NO_ACCENTED.get(province_key, {}).get(district_key)
    DICT_WARD_ACCENTED = DICT_PROVINCE_DISTRICT_WARD_ACCENTED.get(province_key, {}).get(district_key)

    def find_ward(address_key, DICT_WARD):
        ward_keywords = sorted(sum([DICT_WARD[k]['wardKeywords'] for k in DICT_WARD], []), key=len, reverse=True)
        PATTERN_WARD = re.compile('|'.join(ward_keywords), flags=re.IGNORECASE)
        match = PATTERN_WARD.search(address_key)
        ward_keyword = match.group(0) if match else None
        ward_key = next((k for k, v in DICT_WARD.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
        return ward_keyword, ward_key

    if DICT_WARD_NO_ACCENTED:
        ward_keyword, ward_key = find_ward(address_key=address_key, DICT_WARD=DICT_WARD_NO_ACCENTED)

    if not ward_key and DICT_WARD_ACCENTED:
        ward_keyword, ward_key = find_ward(address_key=address_key_accented, DICT_WARD=DICT_WARD_ACCENTED)

    if ward_key:
        accented = ward_key and ward_key != key_normalize(ward_key)
        DICT_WARD = DICT_WARD_ACCENTED if accented else DICT_WARD_NO_ACCENTED

        unit.ward_key = ward_key
        unit.ward = DICT_WARD[ward_key]['ward']
        unit.short_ward = DICT_WARD[ward_key]['wardShort']
        unit.ward_type = DICT_WARD[ward_key]['wardType']
        address_key = replace_from_right(address_key, ward_keyword, '')

    # Keep street
    if keep_street and ',' in address_key:
        street = extract_street(address=address, address_key=address_key)
    if street:
        unit.street = street

    return unit

if __name__ == '__main__':
    print(parse_address_63('52 Đường Số 4, Linh Chiểu, q9'))