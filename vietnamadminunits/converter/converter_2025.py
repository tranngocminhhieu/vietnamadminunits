import json
import sys
from pathlib import Path
import re

from distributed.comm.inproc import new_address

MODULE_DIR = Path(__file__).parent.parent

if __name__ == '__main__':
    sys.path.append(MODULE_DIR.as_posix())
    from parser import parse_address, ParseMode
    from parser.objects import AdminUnit
    from parser.utils import get_geo_location, check_point_in_polygon, find_nearest_point

else:
    from ..parser import parse_address, ParseMode
    from ..parser.objects import AdminUnit
    from ..parser.utils import get_geo_location, check_point_in_polygon, find_nearest_point


# LOAD DATA
with open(MODULE_DIR / 'data/converter_2025.json', 'r') as f:
    converter_data = json.load(f)


DICT_PROVINCE = converter_data['DICT_PROVINCE']
DICT_PROVINCE_WARD_NO_DIVIDED = converter_data['DICT_PROVINCE_WARD_NO_DIVIDED']
DICT_PROVINCE_WARD_DIVIDED = converter_data['DICT_PROVINCE_WARD_DIVIDED']


# MAIN FUNCTION
def convert_address_2025(address: str):

    new_ward_key = None

    # Parse old address to old admin unit
    old_unit = parse_address(address, mode=ParseMode.LEGACY, keep_street=True, level=3)

    # Get new province key and old province_district_ward key
    new_province_key = next((k for k, v in DICT_PROVINCE.items() if old_unit.province_key and old_unit.province_key in v), None)

    # Find new ward key if old ward key is found, else: allow find new province instead of raise error
    if old_unit.ward_key:
        old_province_district_ward_key = f"{old_unit.province_key}_{old_unit.district_key}_{old_unit.ward_key}"

        # Priority find new ward key in no-divided dict
        DICT_WARD_NO_DIVIDED = DICT_PROVINCE_WARD_NO_DIVIDED[new_province_key]
        new_ward_key = next((k for k, v in DICT_WARD_NO_DIVIDED.items() if old_province_district_ward_key and old_province_district_ward_key in v), None)


        # Find new ward key if old ward is divided
        if not new_ward_key:
            new_wards = DICT_PROVINCE_WARD_DIVIDED.get(new_province_key, {}).get(old_province_district_ward_key, [])

            # Priority use default new ward if address is not provided
            if not old_unit.street:
                new_ward_key = next((ward['newWardKey'] for ward in new_wards if ward['isDefaultNewWard']), None)

            # If address is provided, get old location and compare to each new ward polygon and point to choose the best new ward
            else:
                old_location = get_geo_location(old_unit.get_address())
                old_point = (old_location.latitude, old_location.longitude)

                containing_points = []
                new_ward_points = []

                for ward in new_wards:
                    new_point = (ward['newWardLat'], ward['newWardLon'])
                    new_ward_points.append(new_point)
                    is_contain = check_point_in_polygon(point=old_point, polygon_center=new_point, polygon_area_km2=ward['newWardAreaKm2'])
                    if is_contain:
                        containing_points.append(new_point)

                nearest_point = find_nearest_point(a_point=old_point, list_of_b_points=containing_points)

                if len(containing_points) == 1:
                    default_ward_point = containing_points[0]
                else:
                    default_ward_point = nearest_point

                new_ward_key = next((ward['newWardKey'] for ward in new_wards if (ward['newWardLat'], ward['newWardLon']) == default_ward_point), None)


    # Convert to new admin unit
    new_address_components = [i for i in (old_unit.street, new_ward_key, new_province_key) if i]
    new_address = ','.join(new_address_components)
    new_unit = parse_address(new_address, mode=ParseMode.FROM_2025, keep_street=True, level=2)

    return new_unit



if __name__ == '__main__':
    print(convert_address_2025('Phường 9, Quận 5'))
    # print(convert_63_to_34('Ho Chi Minh'))