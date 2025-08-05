from shapely.geometry import Polygon, Point
from geopy.distance import distance
from geopy.geocoders import ArcGIS
from geopy.distance import geodesic

from unidecode import unidecode
import re
import unicodedata

geolocator = ArcGIS()


def get_geo_location(address):
    return geolocator.geocode(address)


def generate_square_polygon(center: tuple, area_km2: float):
    '''
    :param center: (latitude, longitude)
    :param area_km2: float
    :return: shapely.geometry.Polygon in (longitude, latitude) order
    '''
    side_km = area_km2 ** 0.5
    half_side_km = side_km / 2

    # Tạo 4 góc vuông quanh tâm (theo các hướng chính)
    north = distance(kilometers=half_side_km).destination(center, 0).latitude
    south = distance(kilometers=half_side_km).destination(center, 180).latitude
    east  = distance(kilometers=half_side_km).destination(center, 90).longitude
    west  = distance(kilometers=half_side_km).destination(center, 270).longitude

    # Theo thứ tự (lon, lat) nếu dùng GeoJSON hoặc shapely
    polygon_coords = [
        (west, south),
        (west, north),
        (east, north),
        (east, south),
        (west, south),  # Đóng polygon
    ]

    return Polygon(polygon_coords)


def check_point_in_polygon(point: tuple, polygon_center: tuple, polygon_area_km2: float):
    '''
    :param point: (latitude, longitude)
    :param polygon_center: (latitude, longitude)
    :param polygon_area_km2: float
    :return: boolean
    '''
    polygon = generate_square_polygon(center=polygon_center, area_km2=polygon_area_km2)
    point = Point(point[1], point[0])
    return polygon.contains(point)


def find_nearest_point(a_point: tuple, list_of_b_points: list):
    '''
    :param a_point: (latitude, longitude)
    :param list_of_b_points: list of tuples (latitude, longitude)
    :return: (latitude, longitude)
    '''
    return min(list_of_b_points, key=lambda b: geodesic(a_point, b).meters)


def correct_typos(text):
    '''
    :param text: str
    :return: str or np.nan
    '''

    typos = {
        r'\bHoà\b': 'Hòa',
        r'\bHoá\b': 'Hóa',
        r'\bHoả\b': 'Hỏa',
        r'\bHoè\b': 'Hòe',
        r'\bThuỷ\b': 'Thủy',
        r'\bThuỵ\b': 'Thụy',
        r'\bUý\b': 'Úy',
        r'\bKhoá\b': 'Khóa',
    }

    if isinstance(text, str):
        for typo in typos:
            text = re.sub(typo, typos[typo], text)
    return text



def uppercase_first_letters(text: str, all_first_letters=False):
    if isinstance(text, str):
        if all_first_letters:
            text = ' '.join(word[0].upper() + word[1:] if word else '' for word in text.split())
        else:
            text = text[0].upper() + text[1:]
    return text



def unicode_normalize(text):
    '''
    - Chuyển Unicode tổ hợp sang Unicode dựng sẵn (lỗi gõ dấu bằng ký tự đặc biệt)
    - Fix quote đặc biệt
    - Fix dash dính liền
    - Fix double space
    :param text: str
    :return: str or np.nan
    '''
    if isinstance(text, str):
        text = unicodedata.normalize('NFC', text)
        text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"') # Normalize quotes
        text = text.replace('-', ' - ')
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\'\s+', "'", text)
        return text.strip()
    return text


def key_normalize(text: str, keep: list=[], decode=True):
    '''
    Loại bỏ tất cả ký tự không phải chữ/số/keep
    :param text: str
    :param keep: list
    :param decode: bool, bỏ dấu tiếng Việt hay không
    :return: str or np.nan
    '''
    if isinstance(text, str):
        keep_set = ''.join(re.escape(c) for c in keep)
        pattern = rf"[^\w{keep_set}]+"  # \w là a-zA-Z0-9_
        text = re.sub(pattern, '', unidecode(text) if decode else text).lower()
        text = re.sub(r'\s+', ' ', text)
    return text


def replace_from_right(text: str, old: str, new: str='', for_text: str=None):
    '''
    Help remove keyword in address key.

    :param text: Text to search.
    :param old: Pattern to search.
    :param new: Value to replace.
    :param for_text: Actual text to replace. For example: text is no-accented but for_text is accented.
    :return: New text
    '''
    pos = text.rfind(old)
    text = for_text if for_text else text
    if pos != -1:
        text = text[:pos] + new + text[pos + len(old):]
    return text.strip()


def extract_street(address: str, address_key: str):
    first_address_key_part = address_key.split(',')[0].strip()
    first_address_part = address.split(',')[0].strip()

    first_address_part_norm = key_normalize(first_address_part)
    first_address_key_part_norm = key_normalize(first_address_key_part)

    # Tìm phần giao nhau giữa normalized key và normalized text
    common_prefix = ''
    for i in range(min(len(first_address_part_norm), len(first_address_key_part_norm))):
        if first_address_part_norm[i] == first_address_key_part_norm[i]:
            common_prefix += first_address_part_norm[i]
        else:
            break

    # Dùng common_prefix để dò lại chuỗi gốc tương ứng trong first_address_part
    match_result = ''
    for char in first_address_part:
        if key_normalize(match_result + char) == common_prefix[:len(key_normalize(match_result + char))]:
            match_result += char
        else:
            break

    return match_result.strip().title() if match_result else None


if __name__ == '__main__':
    # print(key_normalize('Bà Rịa-   Vũng,Tàu', keep=[',', ' '], decode=False))
    print(find_nearest_point(a_point=(10.770063796439, 106.704416669302), list_of_b_points=[(10.7713, 106.694), (10.7805, 106.704)]))