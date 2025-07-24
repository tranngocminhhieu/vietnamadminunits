import json
import sqlite3
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from seleniumbase import Driver
from tqdm import tqdm
from datetime import datetime

warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_location(address, driver):
    driver.send_keys('#query-input', address)
    driver.click('#geocode-button')
    driver.find_element('#query-input').clear()
    time.sleep(10)  # Avoid rate limit and waiting for HTML is rendered
    html = driver.get_page_source()
    soup = BeautifulSoup(html, 'html.parser')

    # Result
    results_display = soup.find(id='results-display-div')

    # Location (Latitude, Longitude)
    result_location = results_display.find(class_='result-location')
    location = result_location.text.split()[1]

    # Bounds
    result_bounds = results_display.find(class_='result-bounds')
    result_viewport = results_display.find(class_='result-viewport')
    bounds_element = result_bounds or result_viewport
    if bounds_element:
        bounds = ' '.join(bounds_element.text.split()[1:])
    else:
        bounds = None

    # Formated Address
    result_formatted_address = results_display.find(class_='result-formatted-address')
    if result_formatted_address:
        formatted_address = result_formatted_address.text.split('\n')[-1].strip()
    else:
        formatted_address = None

    data = {
        'address': address,
        'latitude': location.split(',')[0],
        'longitude': location.split(',')[1],
        'bounds': bounds,
        'geo_address': formatted_address,
    }

    return data

if __name__ == '__main__':
    df = pd.read_csv(BASE_DIR / 'data/danhmuc_and_sapnhap.csv')
    df.sort_values(['isDividedWard'], ascending=False, inplace=True)

    level = 2
    if level == 3:
        df_63 = df[['province', 'district', 'ward']].drop_duplicates().reset_index(drop=True)
        df_63['address'] = np.where(df_63['ward'].notna(),
                                    df_63['ward'].fillna('') + ', ' + df_63['district'] + ', ' + df_63['province'],
                                    df_63['district'] + ', ' + df_63['province'])

    elif level == 2:
        df_63 = df[['province', 'district']].drop_duplicates().reset_index(drop=True)
        df_63['address'] = df_63['district'] + ', ' + df_63['province']

    else:
        df_63 = df[['province']].drop_duplicates().reset_index(drop=True)
        df_63['address'] = df_63['province']


    print(f"{df_63.shape[0]} addresses to scrape.")


    driver = Driver(uc=True, headless=True)
    driver.get('https://developers-dot-devsite-v2-prod.appspot.com/maps/documentation/utils/geocoder?hl=vi')

    location_data = []
    for index, row in tqdm(df_63.iterrows(), total=df_63.shape[0]):
        address = row['address']
        location = get_location(address, driver)
        data = {
            'address': address,
            'location': json.dumps(location)
        }
        location_data.append(data)

        if ((index + 1) % 15 == 0) or ((index + 1) == len(df_63)):
            df_data = pd.DataFrame(location_data)
            with sqlite3.connect(BASE_DIR / f'data/raw/63_provinces_location_level_{level}_{datetime.now().date()}.db') as conn:
                df_data.to_sql(name='location', con=conn, if_exists='append', index=False)
            location_data = []