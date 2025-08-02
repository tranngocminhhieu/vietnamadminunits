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
with open(MODULE_DIR / 'data/parser_legacy.json', 'r') as f:
    parser_data = json.load(f)

DICT_PROVINCE = parser_data['DICT_PROVINCE']
DICT_PROVINCE_DISTRICT = parser_data['DICT_PROVINCE_DISTRICT']
DICT_UNIQUE_DISTRICT_PROVINCE = parser_data['DICT_UNIQUE_DISTRICT_PROVINCE']
DICT_PROVINCE_DISTRICT_WARD_NO_ACCENTED = parser_data['DICT_PROVINCE_DISTRICT_WARD_NO_ACCENTED']
DICT_PROVINCE_DISTRICT_WARD_ACCENTED = parser_data['DICT_PROVINCE_DISTRICT_WARD_ACCENTED']
DICT_PROVINCE_DISTRICT_WARD_SHORT_ACCENTED = parser_data['DICT_PROVINCE_DISTRICT_WARD_SHORT_ACCENTED']

province_keywords = sorted(sum([DICT_PROVINCE[k]['provinceKeywords'] for k in DICT_PROVINCE], []), key=len, reverse=True)
PATTERN_PROVINCE = re.compile('|'.join(province_keywords), flags=re.IGNORECASE)

unique_district_keys = sorted(sum([DICT_UNIQUE_DISTRICT_PROVINCE[k]['districtKeywords'] for k in DICT_UNIQUE_DISTRICT_PROVINCE], []), key=len, reverse=True)
PATTERN_UNIQUE_DISTRICT = re.compile('|'.join(unique_district_keys), flags=re.IGNORECASE)


# MAIN FUNCTION
def parse_address_legacy(address: str, keep_street :bool=True, level :int=3) -> AdminUnit:

    if level not in [1, 2, 3]:
        raise ValueError('Level must be 1, 2, or 3')

    unit = AdminUnit(show_district=True)

    address = unicode_normalize(address)
    address_key = key_normalize(address, keep=[','])
    address_key_accented = key_normalize(address, keep=[','], decode=False)

    district_key = None
    ward_key = None
    ward_keyword = None
    street = None

    # Find province

    # match = PATTERN_PROVINCE.search(address_key)
    # province_keyword = match.group(0) if match else None
    # Failed with 'Huyện Quảng Bình, Tỉnh Hà Giang' -> 'Tỉnh Quảng Bình'
    province_keyword = next((m.group() for m in reversed(list(PATTERN_PROVINCE.finditer(address_key)))), None)

    if province_keyword:
        # Ưu tiên address_key_accented trước vì address_key là tham số
        address_key_accented = replace_from_right(text=address_key, old=province_keyword, new='', for_text=address_key_accented)
        address_key = replace_from_right(text=address_key, old=province_keyword, new='')


    province_key = next((k for k, v in DICT_PROVINCE.items() if province_keyword and province_keyword in [kw for kw in v['provinceKeywords']]), None)

    if not province_key:
        district_keyword = next((m.group() for m in reversed(list(PATTERN_UNIQUE_DISTRICT.finditer(address_key)))), None)

        if district_keyword:
            address_key_accented = replace_from_right(text=address_key, old=district_keyword, new='', for_text=address_key_accented)
            address_key = replace_from_right(text=address_key, old=district_keyword, new='')

        district_key = next((k for k, v in DICT_UNIQUE_DISTRICT_PROVINCE.items() if district_keyword and district_keyword in [kw for kw in v['districtKeywords']]), None)

        if district_key:
            province_key = DICT_UNIQUE_DISTRICT_PROVINCE[district_key]['provinceKey']

    if not province_key:
        return unit
    else:
        unit.province_key = province_key
        unit.province = DICT_PROVINCE[province_key]['province']
        unit.short_province = DICT_PROVINCE[province_key]['provinceShort']
        unit.latitude = DICT_PROVINCE[province_key]['provinceLat']
        unit.longitude = DICT_PROVINCE[province_key]['provinceLon']


    if level in [2,3]:
        # Find district
        DICT_DISTRICT = DICT_PROVINCE_DISTRICT[province_key]
        if not district_key:
            district_keywords = sorted(sum([DICT_DISTRICT[k]['districtKeywords'] for k in DICT_DISTRICT], []), key=len, reverse=True)
            PATTERN_DISTRICT = re.compile('|'.join(re.escape(k) for k in district_keywords), flags=re.IGNORECASE)

            district_keyword = next((m.group() for m in reversed(list(PATTERN_DISTRICT.finditer(address_key)))), None)

            if district_keyword:
                address_key_accented = replace_from_right(text=address_key, old=district_keyword, new='', for_text=address_key_accented)
                address_key = replace_from_right(text=address_key, old=district_keyword, new='')

            district_key = next((k for k, v in DICT_DISTRICT.items() if district_keyword and district_keyword in [kw for kw in v['districtKeywords']]), None)

        if not district_key:
            return unit
        else:
            unit.district_key = district_key
            unit.district = DICT_DISTRICT[district_key]['district']
            unit.short_district = DICT_DISTRICT[district_key]['districtShort']
            unit.district_type = DICT_DISTRICT[district_key]['districtType']
            unit.latitude = DICT_DISTRICT[district_key]['districtLat']
            unit.longitude = DICT_DISTRICT[district_key]['districtLon']


    if level == 3:
        # Find ward
        DICT_WARD_NO_ACCENTED =  DICT_PROVINCE_DISTRICT_WARD_NO_ACCENTED.get(province_key, {}).get(district_key)
        DICT_WARD_ACCENTED = DICT_PROVINCE_DISTRICT_WARD_ACCENTED.get(province_key, {}).get(district_key)
        DICT_WARD_SHORT_ACCENTED = DICT_PROVINCE_DISTRICT_WARD_SHORT_ACCENTED.get(province_key, {}).get(district_key)

        def find_ward(address_key, DICT_WARD):
            ward_keywords = sorted(sum([DICT_WARD[k]['wardKeywords'] for k in DICT_WARD], []), key=len, reverse=True)
            PATTERN_WARD = re.compile('|'.join(ward_keywords), flags=re.IGNORECASE)

            ward_keyword = next((m.group() for m in reversed(list(PATTERN_WARD.finditer(address_key)))), None)

            ward_key = next((k for k, v in DICT_WARD.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
            return ward_keyword, ward_key

        if DICT_WARD_NO_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key=address_key, DICT_WARD=DICT_WARD_NO_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_NO_ACCENTED

        if not ward_key and DICT_WARD_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key=address_key_accented, DICT_WARD=DICT_WARD_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_ACCENTED

        if not ward_key and DICT_WARD_SHORT_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key=address_key_accented, DICT_WARD=DICT_WARD_SHORT_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_SHORT_ACCENTED

        if ward_key:
            unit.ward_key = ward_key
            unit.ward = DICT_WARD[ward_key]['ward']
            unit.short_ward = DICT_WARD[ward_key]['wardShort']
            unit.ward_type = DICT_WARD[ward_key]['wardType']
            unit.latitude = DICT_WARD[ward_key]['wardLat']
            unit.longitude = DICT_WARD[ward_key]['wardLon']

            # Không dùng address_key_accented bên dưới nữa nên chỉ remove cho address_key
            address_key = replace_from_right(text=address_key, old=key_normalize(ward_keyword), new='')

    # Keep street
    if keep_street and address_key.count(',') >= 3:
        street = extract_street(address=address, address_key=address_key)
    if street:
        unit.street = street

    return unit

if __name__ == '__main__':
    # print(parse_address_63('tân thạnh, tan thanh, long an'))
    print(parse_address_63('Xã Minh Quán, Huyện Trấn Yên, Tỉnh Yên Bái'))