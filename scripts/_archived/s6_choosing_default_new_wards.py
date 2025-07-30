import warnings

import pandas as pd
from seleniumbase import Driver
from tqdm.notebook import tqdm

import sys

from pathlib import Path
import sys
BASE_DIR = Path().resolve().parent.parent
sys.path.append((BASE_DIR / 'vietnamadminunits/parser').as_posix())

from utils import check_point_in_polygon, find_nearest_point

warnings.filterwarnings('ignore')
from pathlib import Path
from s3_scrap_63_provinces_ward_location import get_location

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read divided wards
df = pd.read_csv(BASE_DIR / 'data/danhmuc_and_sapnhap.csv')
df_divided = df[df['isDividedWard'] == True].copy()
df_divided.sort_values(by=['province', 'district', 'ward', 'newWardAreaKm2'], inplace=True)
df_divided_ward = df_divided[['province', 'district', 'ward']].drop_duplicates()

# BEGIN GET LOCATION FOR DIVIDED WARDS
re_scrap = False
if re_scrap:
    # METHOD 1: Use GeoPy, But it is not give center location
    # for index, row in tqdm(df_divided_ward.iterrows(), total=len(df_divided_ward)):
    #     address = row['ward'] + ', ' + row['district'] + ', ' + row['province']
    #     location = geolocator.geocode(address)
    #     df_divided_ward.loc[index, ['wardLat', 'wardLon', 'wardFormattedAddress']] = location.latitude, location.longitude, location.address
    # df_divided_ward.to_csv(BASE_DIR / 'data/df_divided_ward.csv', index=False)

    # METHOD 2: Use Google API, It gives center location and bounds
    driver = Driver(uc=True)
    driver.get('https://developers-dot-devsite-v2-prod.appspot.com/maps/documentation/utils/geocoder?hl=vi')

    for index, row in tqdm(df_divided_ward[df_divided_ward['wardLat'].isna()].iterrows(),
                           total=len(df_divided_ward[df_divided_ward['wardLat'].isna()])):
        address = row['ward'] + ', ' + row['district'] + ', ' + row['province']
        location = get_location(address, driver)
        df_divided_ward.loc[index, ['wardLat', 'wardLon', 'wardBounds', 'wardFormattedAddress']] = location['wardLat'], \
        location['wardLon'], location['wardBounds'], location['wardFormattedAddress']
        print(location)
    df_divided_ward.to_csv(BASE_DIR / 'data/df_divided_ward.csv', index=False)

else:
    df_divided_ward_saved = pd.read_csv(BASE_DIR / 'data/df_divided_ward.csv')
    if df_divided_ward_saved.shape[0] != df_divided_ward.shape[0]:
        raise Exception('File lưu không đúng số lượng với hiện tại')
    else:
        df_divided_ward = df_divided_ward_saved
# END GET LOCATION FOR DIVIDED WARDS


# Assign default new ward for divided wards
for index, row in df_divided_ward.iterrows():
    province = row['province']
    district = row['district']
    ward = row['ward']
    ward_point = (row['wardLat'], row['wardLon'])

    new_wards = df[(df['province'] == province) & (df['district'] == district) & (df['ward'] == ward)]

    containing_points = []
    new_ward_points = []
    for new_ward_index, new_ward_row in new_wards.iterrows():
        new_ward_point = (new_ward_row['newWardLat'], new_ward_row['newWardLon'])
        new_ward_area_km2 = new_ward_row['newWardAreaKm2']
        new_ward_points.append(new_ward_point)

        is_contain = check_point_in_polygon(point=ward_point, polygon_center=new_ward_point,
                                            polygon_area_km2=new_ward_area_km2)
        if is_contain:
            containing_points.append(new_ward_point)
        df.loc[new_ward_index, 'isNewWardPolygonContainsWard'] = is_contain

    nearest_point = find_nearest_point(a_point=ward_point, list_of_b_points=new_ward_points)

    if len(containing_points) == 1:
        default_ward_point = containing_points[0]
    else:
        default_ward_point = nearest_point

    df.loc[(df['province'] == province) & (df['district'] == district) & (df['ward'] == ward) & (
                df['newWardLat'] == nearest_point[0]) & (
                       df['newWardLon'] == nearest_point[1]), 'isNearestNewWard'] = True
    df.loc[(df['province'] == province) & (df['district'] == district) & (df['ward'] == ward) & (
                df['newWardLat'] == default_ward_point[0]) & (
                       df['newWardLon'] == default_ward_point[1]), 'isDefaultNewWard'] = True

df.loc[(df['isDividedWard'] == True) & (df['isNearestNewWard'].isna()), 'isNearestNewWard'] = False
df.loc[(df['isDividedWard'] == True) & (df['isDefaultNewWard'].isna()), 'isDefaultNewWard'] = False

# Save
df.to_csv(BASE_DIR / 'data/danhmuc_and_sapnhap_has_default_new_ward.csv', index=False)
