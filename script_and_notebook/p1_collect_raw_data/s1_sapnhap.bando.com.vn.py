import pandas as pd
import requests
from tqdm import tqdm
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def is_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


# Scrap Province
res = requests.post('https://sapnhap.bando.com.vn/pcotinh', data={'id': 0})
res.raise_for_status()
data_province = res.json()
df_province = pd.DataFrame(data_province)
df_province = df_province[[col for col in df_province.columns if not is_number(col)]]
df_province.to_csv(BASE_DIR / 'data/sapnhap.bando.com.vn_province.csv', index=False)

# Scrap Ward
df_wards = []
for i in tqdm(range(1, 37)):
    res = requests.post('https://sapnhap.bando.com.vn/ptracuu', data={'id': i})
    res.raise_for_status()
    data_ward = res.json()
    _df_ward = pd.DataFrame(data_ward)
    df_wards.append(_df_ward)

df_ward = pd.concat(df_wards)
df_ward = df_ward[[col for col in df_ward.columns if not is_number(col)]]
df_ward.to_csv(BASE_DIR / 'data/sapnhap.bando.com.vn_ward.csv', index=False)