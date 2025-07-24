
import pickle
from pathlib import Path
import re

if __name__ == '__main__':
    from utils import key_normalize, extract_street, replace_from_right
    from objects import Unit
else:
    from .utils import key_normalize, extract_street, replace_from_right
    from .objects import Unit

# LOAD PICKLE DATA
CURRENT_DIR = Path(__file__).parent
with open(CURRENT_DIR / 'data/v34provinces/pickle_data.pkl', 'rb') as f:
    pickle_data = pickle.load(f)

DICT_PROVINCE = pickle_data['DICT_PROVINCE']
DICT_PROVINCE_WARD_NO_ACCENTED = pickle_data['DICT_PROVINCE_WARD_NO_ACCENTED']
DICT_PROVINCE_WARD_ACCENTED = pickle_data['DICT_PROVINCE_WARD_ACCENTED']
DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED = pickle_data['DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED']
DICT_UNIQUE_WARD_PROVINCE_ACCENTED = pickle_data['DICT_UNIQUE_WARD_PROVINCE_ACCENTED']


province_keywords = sorted(sum([DICT_PROVINCE[k]['provinceKeywords'] for k in DICT_PROVINCE], []), key=len, reverse=True)
PATTERN_PROVINCE = re.compile('|'.join(province_keywords), flags=re.IGNORECASE)

unique_ward_no_accented_keywords = sorted(sum([DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED[k]['wardKeywords'] for k in DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED], []), key=len, reverse=True)
PATTERN_UNIQUE_WARD_PROVINCE_NO_ACCENTED = re.compile('|'.join(unique_ward_no_accented_keywords), flags=re.IGNORECASE)

unique_ward_accented_keywords = sorted(sum([DICT_UNIQUE_WARD_PROVINCE_ACCENTED[k]['wardKeywords'] for k in DICT_UNIQUE_WARD_PROVINCE_ACCENTED], []), key=len, reverse=True)
PATTERN_UNIQUE_WARD_PROVINCE_ACCENTED = re.compile('|'.join(unique_ward_accented_keywords), flags=re.IGNORECASE)




# MAIN FUNCTION
def parse_address(address, keep_street=True, level=2):
    '''
    Parse an 34 provinces address to a unit.

    :param address: street, ward, province.
    :param keep_street: boolean.
    :param level: [1,2]
    :return: Unit object.
    '''
    unit = Unit()


    address_key = key_normalize(address, keep=[','])
    address_key_accented = key_normalize(address, keep=[','], decode=False)
    ward_keyword = None
    ward_key = None
    street = None

    # Find province
    match = PATTERN_PROVINCE.search(address_key)
    province_keyword = match.group(0) if match else None

    # Xóa từ khóa ở chổ này là hợp lý (không mang xuống dưới), vì trường hợp 2 fallback ở dưới dành cho không tìm ra keyword trong address.
    if province_keyword:
        address_key = replace_from_right(address_key, province_keyword, '')

    province_key = next((k for k, v in DICT_PROVINCE.items() if province_keyword and province_keyword in [kw for kw in v['provinceKeywords']]), None)

    if not province_key:
        match = PATTERN_UNIQUE_WARD_PROVINCE_NO_ACCENTED.search(address_key)
        ward_keyword = match.group(0) if match else None
        ward_key = next((k for k, v in DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
        if ward_key:
            province_key = DICT_UNIQUE_WARD_PROVINCE_NO_ACCENTED[ward_key]['provinceKey']

    if not province_key:
        match = PATTERN_UNIQUE_WARD_PROVINCE_ACCENTED.search(address_key_accented)
        ward_keyword = match.group(0) if match else None
        ward_key = next((k for k, v in DICT_UNIQUE_WARD_PROVINCE_ACCENTED.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
        if ward_key:
            province_key = DICT_UNIQUE_WARD_PROVINCE_ACCENTED[ward_key]['provinceKey']

    if not province_key:
        return unit
    else:
        unit.province_key = province_key
        unit.province = DICT_PROVINCE[province_key]['province']
        unit.short_province = DICT_PROVINCE[province_key]['provinceShort']
    if level == 1:
        return unit


    # Find ward
    DICT_WARD_NO_ACCENTED = DICT_PROVINCE_WARD_NO_ACCENTED.get(province_key)
    DICT_WARD_ACCENTED = DICT_PROVINCE_WARD_ACCENTED.get(province_key)

    def find_ward(address_key, DICT_WARD):
        ward_keywords = sorted(sum([DICT_WARD[k]['wardKeywords'] for k in DICT_WARD], []), key=len, reverse=True)
        PATTERN_WARD = re.compile('|'.join(ward_keywords), flags=re.IGNORECASE)
        match = PATTERN_WARD.search(address_key)
        ward_keyword = match.group(0) if match else None
        if not ward_keyword:
            return None, None
        ward_key = next((k for k, v in DICT_WARD.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
        return ward_keyword, ward_key

    if not ward_key and DICT_WARD_NO_ACCENTED:
        ward_keyword, ward_key = find_ward(address_key, DICT_WARD_NO_ACCENTED)

    if not ward_key and DICT_WARD_ACCENTED:
        ward_keyword, ward_key = find_ward(address_key_accented, DICT_WARD_ACCENTED)

    if ward_key:
        accented = ward_key and ward_key != key_normalize(ward_key)
        DICT_WARD = DICT_WARD_ACCENTED if accented else DICT_WARD_NO_ACCENTED
        unit.ward_key = ward_key
        unit.ward = DICT_WARD[ward_key]['ward']
        unit.short_ward = DICT_WARD[ward_key]['wardShort']
        unit.ward_type = DICT_WARD[ward_key]['wardType']

        address_key = replace_from_right(address_key, key_normalize(ward_keyword), '')

    # Keep street
    if keep_street and ',' in address_key:
        street = extract_street(address=address, address_key=address_key)
    if street:
        unit.street = street

    return unit

if __name__ == '__main__':
    print(parse_address('văn lang , thai nguyen'))