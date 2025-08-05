import requests
import json
from datetime import datetime

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

res = requests.get('https://production.cas.so/address-kit/2025-07-01/communes')
data = res.json()


with open(BASE_DIR / f'data/raw/production.cas.so_3221_wards_{datetime.today().date()}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)