import json
from pathlib import Path
import re

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
DICT_PROVINCE_DISTRICT_DIVIDED = parser_data['DICT_PROVINCE_DISTRICT_DIVIDED']


# CREATE PATTERNS
province_keywords = sorted(sum([DICT_PROVINCE[k]['provinceKeywords'] for k in DICT_PROVINCE], []), key=len, reverse=True)
PATTERN_PROVINCE = re.compile('|'.join(province_keywords), flags=re.IGNORECASE)

unique_district_keys = sorted(sum([DICT_UNIQUE_DISTRICT_PROVINCE[k]['districtKeywords'] for k in DICT_UNIQUE_DISTRICT_PROVINCE], []), key=len, reverse=True)
PATTERN_UNIQUE_DISTRICT = re.compile('|'.join(unique_district_keys), flags=re.IGNORECASE)


# MAIN FUNCTION
def parse_address_legacy(address: str, keep_street :bool=True, level :int=3) -> AdminUnit:
    '''
    Parse a 63-province address to an AdminUnit object.

    :param address: (street), ward, district, province.
    :param keep_street: boolean.
    :param level: [1,2,3]
    
    :return: AdminUnit object.
    '''

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
    tmp_hidden_keyword = None


    # ----- PARSE PROVINCE -----

    # Old method:
    # match = PATTERN_PROVINCE.search(address_key)
    # province_keyword = match.group(0) if match else None
    # Sai vì nó match trúng từ khóa đầu tiên: 'Huyện Quảng Bình, Tỉnh Hà Giang' -> 'Tỉnh Quảng Bình'
    

    # 1st attempt: Tìm province_keyword
    province_keyword = next((m.group() for m in reversed(list(PATTERN_PROVINCE.finditer(address_key)))), None)

    # Suy province_keyword ra province_key
    province_key = next((k for k, v in DICT_PROVINCE.items() if province_keyword and province_keyword in [kw for kw in v['provinceKeywords']]), None)

    # Nếu tìm ra province_keyword thì lặp tức xóa nó khỏi địa chỉ để tránh các level sau bắt nhầm từ khóa
    if province_keyword:
        address_key_accented = replace_from_right(text=address_key, old=province_keyword, new='', for_text=address_key_accented) # Ưu tiên address_key_accented trước vì address_key là tham số
        address_key = replace_from_right(text=address_key, old=province_keyword, new='')

    
    # 2nd attempt: Nếu không tìm được province_keyword thì tìm district_keyword, đây là những district mà tên của nó là duy nhất, có thể suy ra được province.
    if not province_key:
        district_keyword = next((m.group() for m in reversed(list(PATTERN_UNIQUE_DISTRICT.finditer(address_key)))), None)

        # Suy district_keyword ra district_key
        district_key = next((k for k, v in DICT_UNIQUE_DISTRICT_PROVINCE.items() if district_keyword and district_keyword in [kw for kw in v['districtKeywords']]), None)

        # Suy district_key ra province_key
        province_key = DICT_UNIQUE_DISTRICT_PROVINCE.get(district_key, {}).get('provinceKey')

        # Nếu tìm ra district_keyword thì lặp tức xóa nó khỏi địa chỉ để tránh level sau bắt nhầm từ khóa
        if district_keyword:
            address_key_accented = replace_from_right(text=address_key, old=district_keyword, new='', for_text=address_key_accented)
            address_key = replace_from_right(text=address_key, old=district_keyword, new='')

        
    # Gán thông tin của province vào unit
    if province_key:
        unit.province_key = province_key
        unit.province = DICT_PROVINCE[province_key]['province']
        unit.short_province = DICT_PROVINCE[province_key]['provinceShort']
        unit.province_code = DICT_PROVINCE[province_key]['provinceCode']
        unit.latitude = DICT_PROVINCE[province_key]['provinceLat']
        unit.longitude = DICT_PROVINCE[province_key]['provinceLon']


    # ----- PARSE DISTRICT -----
    if level in [2,3] and province_key:
        
        if province_key == 'thanhphohue':
            # Tạm ẩn một số phường vì nó gây nhiễu, nhầm từ khóa
            tmp_hidden_keywords = [ # Nếu có từ khóa này nó sẽ nhầm vào các quận của Huế trong trường hợp district là Thành phố Huế (cũ)
                'phuongthuanhoa', # Quận Thuận Hóa, Thành phố Huế
                'phuongthuybieu', # Thị xã Hương Thủy, Thành phố Huế
                'phuongthuyvan', # Thị xã Hương Thủy, Thành phố Huế
                'phuongthuyxuan', # Thị xã Hương Thủy, Thành phố Huế
            ]
            if any(word in address_key_accented for word in ['thuậnhòa', 'thuậnhoà']): # Quận Thuận Hóa, Thành phố Huế
                tmp_hidden_keywords.append('thuanhoa') # VN chỉ có duy nhất một district là thuanhoa thôi

            PATTERN_TMP_HIDDEN = re.compile('|'.join(re.escape(k) for k in tmp_hidden_keywords), flags=re.IGNORECASE)
            tmp_hidden_keyword = next((m.group() for m in list(PATTERN_TMP_HIDDEN.finditer(address_key))), None) # No need to reverse because it is a ward keyword
            if tmp_hidden_keyword:
                address_key = address_key.replace(tmp_hidden_keyword, 'TMP_HIDDEN_KEYWORD')

        # 1st attempt: Bắt đầu một cách đơn giản nhất cho phần lớn district
        DICT_DISTRICT = DICT_PROVINCE_DISTRICT[province_key]
        if not district_key:

            # Tìm district_keyword
            district_keywords = sorted(sum([DICT_DISTRICT[k]['districtKeywords'] for k in DICT_DISTRICT], []), key=len, reverse=True)
            PATTERN_DISTRICT = re.compile('|'.join(re.escape(k) for k in district_keywords), flags=re.IGNORECASE)
            district_keyword = next((m.group() for m in reversed(list(PATTERN_DISTRICT.finditer(address_key)))), None)

            # Suy district_keyword ra district_key
            district_key = next((k for k, v in DICT_DISTRICT.items() if district_keyword and district_keyword in [kw for kw in v['districtKeywords']]), None)

            # Nếu tìm ra district_keyword thì lặp tức xóa nó khỏi địa chỉ để tránh level sau bắt nhầm từ khóa
            if district_keyword:
                address_key_accented = replace_from_right(text=address_key, old=district_keyword, new='', for_text=address_key_accented)
                address_key = replace_from_right(text=address_key, old=district_keyword, new='')

            
        # 2nd attempt: Trường hợp không tìm được district_keyword vì tên cũ không còn trong bản mới nhất, district cũ bị chia thành 2 district mới.
        # Lưu ý: Nếu để phần này ở trên sẽ bị sai với 'Xã Thạch Hạ, Thành Phố Hà Tĩnh, Hà Tĩnh'. Nó bắt trúng 'thachha' của ward mà nhầm của district
        DICT_DISTRICT_DIVIDED = DICT_PROVINCE_DISTRICT_DIVIDED.get(province_key, {})
        if not district_key:
            
            # Tìm divided_district_key
            if DICT_DISTRICT_DIVIDED:
                divided_district_keywords = sorted(sum([DICT_DISTRICT_DIVIDED[k]['dividedDistrictKeywords'] for k in DICT_DISTRICT_DIVIDED], []), key=len, reverse=True)
                PATTERN_DISTRICT_DIVIDED = re.compile('|'.join(re.escape(k) for k in divided_district_keywords), flags=re.IGNORECASE)
                divided_district_keyword = next((m.group() for m in reversed(list(PATTERN_DISTRICT_DIVIDED.finditer(address_key)))), None)
                divided_district_key = next((k for k, v in DICT_DISTRICT_DIVIDED.items() if divided_district_keyword and divided_district_keyword in [kw for kw in v['dividedDistrictKeywords']]), None)

                # Nếu tìm ra divided_district_keyword thì lặp tức xóa nó khỏi địa chỉ để tránh level sau bắt nhầm từ khóa
                if divided_district_key:
                    address_key_accented = replace_from_right(text=address_key, old=divided_district_keyword, new='', for_text=address_key_accented)
                    address_key = replace_from_right(text=address_key, old=divided_district_keyword, new='')

                    # Trả lại từ khóa đã tạm ẩn trước khi tìm ward
                    if tmp_hidden_keyword:
                        address_key = address_key.replace('TMP_HIDDEN_KEYWORD', tmp_hidden_keyword)
                        tmp_hidden_keyword = None

                    # Nếu có divided_district_key, dựa vào ward_keyword để chọn district_key
                    DICT_DISTRICT_WARD = DICT_DISTRICT_DIVIDED[divided_district_key]['districts']
                    ward_keywords = sorted(sum([DICT_DISTRICT_WARD[k]['wardKeywords'] for k in DICT_DISTRICT_WARD], []), key=len, reverse=True)
                    PATTERN_WARD = re.compile('|'.join(ward_keywords), flags=re.IGNORECASE)
                    ward_keyword = next((m.group() for m in reversed(list(PATTERN_WARD.finditer(address_key)))), None)
                    district_key = next((k for k, v in DICT_DISTRICT_WARD.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)
                    
                    # Nếu không có ward, chọn district mặc định
                    if not district_key:
                        district_key = next((k for k in DICT_DISTRICT_WARD if DICT_DISTRICT_WARD[k]['districtDefault'] == True), None)


        # Xử lý các case đặc biệt:
        # District vẫn còn nhưng vài ward bị đem wa district khác
        # District có tên ngắn bị trùng, chỉ khác type
        elif district_key in DICT_DISTRICT_DIVIDED:
            
            # Đưa giá trị của district_key cho divided_district_key
            divided_district_key = district_key
            district_key = None

            # Trả lại từ khóa đã tạm ẩn trước khi tìm ward
            if tmp_hidden_keyword:
                address_key = address_key.replace('TMP_HIDDEN_KEYWORD', tmp_hidden_keyword)
                tmp_hidden_keyword = None

            # Dựa vào ward_keyword để chọn district_key
            DICT_DISTRICT_WARD = DICT_DISTRICT_DIVIDED[divided_district_key]['districts']
            ward_keywords = sorted(sum([DICT_DISTRICT_WARD[k]['wardKeywords'] for k in DICT_DISTRICT_WARD], []), key=len, reverse=True)
            PATTERN_WARD = re.compile('|'.join(ward_keywords), flags=re.IGNORECASE)
            ward_keyword = next((m.group() for m in reversed(list(PATTERN_WARD.finditer(address_key)))), None)
            district_key = next((k for k, v in DICT_DISTRICT_WARD.items() if ward_keyword and ward_keyword in [kw for kw in v['wardKeywords']]), None)

            # Nếu không có ward, chọn district mặc định
            if not district_key:
                district_key = next((k for k in DICT_DISTRICT_WARD if DICT_DISTRICT_WARD[k]['districtDefault'] == True), None)


        # Gán thông tin của district vào unit
        if district_key:
            unit.district_key = district_key
            unit.district = DICT_DISTRICT[district_key]['district']
            unit.short_district = DICT_DISTRICT[district_key]['districtShort']
            unit.district_type = DICT_DISTRICT[district_key]['districtType']
            unit.district_code = DICT_DISTRICT[district_key]['districtCode']
            unit.latitude = DICT_DISTRICT[district_key]['districtLat']
            unit.longitude = DICT_DISTRICT[district_key]['districtLon']


    # ----- PARSE WARD -----
    if level == 3 and district_key:
        
        # Trả lại từ khóa đã tạm ẩn trước khi tìm ward
        if tmp_hidden_keyword:
            address_key = address_key.replace('TMP_HIDDEN_KEYWORD', tmp_hidden_keyword)
            tmp_hidden_keyword = None

        # Có đến 3 bộ ward
        DICT_WARD_NO_ACCENTED =  DICT_PROVINCE_DISTRICT_WARD_NO_ACCENTED.get(province_key, {}).get(district_key) # Không dấu
        DICT_WARD_ACCENTED = DICT_PROVINCE_DISTRICT_WARD_ACCENTED.get(province_key, {}).get(district_key) # Có dấu mới phân biệt được, ví dụ: Phường Sa Pa và Phường Sa Pả
        DICT_WARD_SHORT_ACCENTED = DICT_PROVINCE_DISTRICT_WARD_SHORT_ACCENTED.get(province_key, {}).get(district_key) # Các ward này khi không dấu mà có type thì không sao, nhưng khi không có type thì không phân biệt được, ví dụ: Thị trấn Ba Tơ và Xã Ba Tô

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
        if DICT_WARD_NO_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key=address_key, DICT_WARD=DICT_WARD_NO_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_NO_ACCENTED

        # 2nd attempt: Tìm có dấu
        if not ward_key and DICT_WARD_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key=address_key_accented, DICT_WARD=DICT_WARD_ACCENTED)
            if ward_key:
                DICT_WARD = DICT_WARD_ACCENTED

        # 3rd attempt: Tìm có dấu với tên ngắn
        if not ward_key and DICT_WARD_SHORT_ACCENTED:
            ward_keyword, ward_key = find_ward(address_key=address_key_accented, DICT_WARD=DICT_WARD_SHORT_ACCENTED)
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
    special_zone = ['huyenbachlongvi', 'huyenconco', 'huyenhoangsa', 'huyenlyson', 'huyencondao'] # Mấy cái đảo thì không có ward

    if keep_street and (ward_key or (address_key.count(',') >= 3) or (district_key in special_zone)):
        street = extract_street(address=address, address_key=address_key, highest_level_keyword=ward_keyword)
    if street:
        unit.street = street

    return unit