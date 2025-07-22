from shapely.geometry import Polygon, Point
from geopy.distance import distance
from geopy.geocoders import ArcGIS
from geopy.distance import geodesic

geolocator = ArcGIS()

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