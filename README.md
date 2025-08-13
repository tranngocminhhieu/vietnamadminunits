# Vietnam Administrative Units Parser & Converter
A Python library and open dataset for parsing, converting, and standardizing Vietnam's administrative units — built to support changes such as the 2025 province merger and beyond.

![Made in Vietnam](https://raw.githubusercontent.com/webuild-community/badge/master/svg/made.svg)
[![Pypi](https://img.shields.io/pypi/v/vietnamadminunits?label=pip&logo=PyPI&logoColor=white)](https://pypi.org/project/vietnamadminunits)

## Introduction
This project began as a personal initiative to help myself and others navigate the complexities of Vietnam's administrative unit changes, especially leading up to the 2025 restructuring.  
After cleaning, mapping, and converting large amounts of data from various sources, I realized it could benefit a wider community.

My hope is that this work not only saves you time but also helps bring more consistency and accuracy to your projects involving Vietnamese administrative data.

> Built to simplify your workflow and support open-data collaboration.
## Project Structure

### 📊 Datasets
- Located in [data/processed/](data/processed).
- Includes:
  - 63-province dataset.
  - 34-province dataset.
  - Mapping from 63-province to 34-province dataset.

### 🐍 Python package

- Core logic is in the [`vietnamadminunits`](vietnamadminunits/) package.
- Includes `parse_address()`, `convert_address()` and more functions.
- Quick test link: [Google Colab](https://colab.research.google.com/drive/1Qe30zBqPjMTyLKp80OmPbDG4eyeBLzhL).

## Usage

### 📦 Installation
Install via pip:
```shell
pip install vietnamadminunits
```
Update to the latest version:
```shell
pip install --upgrade vietnamadminunits
```

### 🧾 parse_address()
Parse an address to an `AdminUnit` object.
```python
from vietnamadminunits import parse_address
# from vietnamadminunits import ParseMode -- It helps to choose mode quickly

parse_address(address, mode='FROM_2025', keep_street=True, level=0)
```

**Params**:

- `address`: Best format *"(street), ward, (district), province"*. Case is ignored, accents are usually ignored except in rare cases.
- `mode`: `'FROM_2025'` (34-province) or `'LEGACY'` (63-province). Default `ParseMode.latest()`.
- `keep_street`: Keep the street in the result, works only if there are enough commas: 2+ for *FROM_2025* mode, 3+ for *LEGACY* mode.
- `level`: *FROM_2025* mode accepts `1` or `2`. *LEGACY* mode accepts `1`, `2`, or `3`. Default `0` for highest level automatically.

**Returns**: `AdminUnit` object.

**Example**:

Parse a new address (from 2025).

```python
address = '70 nguyễn sỹ sách, tan son, hcm'
admin_unit = parse_address(address)
print(admin_unit)
```

```text
Admin Unit: 70 Nguyễn Sỹ Sách, Phường Tân Sơn, Thành phố Hồ Chí Minh
Attribute       | Value                    
----------------------------------------
province        | Thành phố Hồ Chí Minh    
ward            | Phường Tân Sơn           
street          | 70 Nguyễn Sỹ Sách        
short_province  | Hồ Chí Minh              
short_ward      | Tân Sơn                  
ward_type       | Phường                   
province_code   | 79                       
ward_code       | 27007                    
latitude        | 10.8224                  
longitude       | 106.65                          
```

Use `AdminUnit`'s attributions.

```python
print(admin_unit.get_address())
```
```text
70 Nguyễn Sỹ Sách, Phường Tân Sơn, Thành phố Hồ Chí Minh
```

```python
print(admin_unit.short_province)
```

```text
Hồ Chí Minh
```

Parse an old address (before 2025).

```python
address = 'đường 15, long bình, quận 9, hcm' # Old address
admin_unit = parse_address(address, mode='LEGACY', level=3) # Use 'LEGACY' or ParseMode.LEGACY for mode
print(admin_unit)
```
```text
Admin Unit: Đường 15, Phường Long Bình, Thành phố Thủ Đức, Thành phố Hồ Chí Minh
Attribute       | Value                    
----------------------------------------
province        | Thành phố Hồ Chí Minh    
district        | Thành phố Thủ Đức        
ward            | Phường Long Bình         
street          | Đường 15                 
short_province  | Hồ Chí Minh              
short_district  | Thủ Đức                  
short_ward      | Long Bình                
district_type   | Thành phố                
ward_type       | Phường                   
province_code   | 79                       
district_code   | 769                      
ward_code       | 26830                    
latitude        | 10.890938                
longitude       | 106.828313              
```

### 🔄 convert_address()
Converts an address from the 63-province format to a standardized 34-province `AdminUnit`.

```python
from vietnamadminunits import convert_address

convert_address(address, mode='CONVERT_2025')
```

**Params**:
- `address`: Best format *"(street), ward, district, province"*. Case is ignored, accents are usually ignored except in rare cases.
- `mode`: Currently, only `'CONVERT_2025'` is supported.

**Returns**: `AdminUnit` object.

**Example**:

```python
address = '59 nguyễn sỹ sách , p15, tan binh, hcm' # Old address
admin_unit = convert_address(address)
print(admin_unit)
```
```text
Admin Unit: 59 Nguyễn Sỹ Sách, Phường Tân Sơn, Thành phố Hồ Chí Minh
Attribute       | Value                    
----------------------------------------
province        | Thành phố Hồ Chí Minh    
ward            | Phường Tân Sơn           
street          | 59 Nguyễn Sỹ Sách        
short_province  | Hồ Chí Minh              
short_ward      | Tân Sơn                  
ward_type       | Phường                   
province_code   | 79                       
ward_code       | 27007                    
latitude        | 10.8224                  
longitude       | 106.65                    
```

### 🐼 Pandas
#### standardize_admin_unit_columns()

Standardizes administrative unit columns *(province, district, ward)* in a DataFrame.

```python
from vietnamadminunits.pandas import standardize_admin_unit_columns

standardize_admin_unit_columns(
    df, 
    province, 
    district=None, 
    ward=None, 
    parse_mode=ParseMode.latest(), 
    convert_mode=None,
    inplace=False, 
    prefix='standardized_', 
    suffix='', 
    short_name=True,
    show_progress=True
)
```

**Params**:
- `df`: `pandas.DataFrame` object.
- `province`: Province column name.
- `district`: District column name.
- `ward`: Ward column name.
- `parse_mode`: `'FROM_2025'` (34-province) or `'LEGACY'` (63-province). Default `ParseMode.latest()`.
- `convert_mode`: Currently, only `'CONVERT_2025'` is supported. Using this will ignore `parse_mode`. Default `None`.
- `inplace`:  Replace the original columns with standardized values; otherwise add new columns. Default `False`.
- `prefix`, `suffix` — Added to new column names if `inplace=False`.
- `short_name`: Use short or full names for administrative units. Default `True`.
- `show_progress`: Display a progress bar during processing. Default `True`.


**Returns**: `pandas.DataFrame` object.

**Example**:

Standardize administrative unit columns in a DataFrame.

```python
import pandas as pd

data = [
    {'province': 'ha noi', 'ward': 'hong ha'},
    {'province': 'hà nội', 'ward': 'ba đình'},
    {'province': 'Hà Nội', 'ward': 'Ngọc Hà'},
    {'province': 'ha noi', 'ward': 'giang vo'},
    {'province': 'ha noi', 'ward': 'hoan kiem'},
]

df = pd.DataFrame(data)
sd_df = standardize_admin_unit_columns(df, province='province', ward='ward')
print(sd_df.to_markdown(index=False))
```

| province   | ward      | standardized_province   | standardized_ward   |
|:-----------|:----------|:------------------------|:--------------------|
| ha noi     | hồng hà   | Hà Nội                  | Hồng Hà             |
| hà nội     | ba đình   | Hà Nội                  | Ba Đình             |
| Hà Nội     | Ngọc Hà   | Hà Nội                  | Ngọc Hà             |
| ha noi     | giảng võ  | Hà Nội                  | Giảng Võ            |
| ha noi     | hoàn kiếm | Hà Nội                  | Hoàn Kiếm           |


Standardize and convert 63-province format administrative unit columns to the new 34-province format.

```python
data = [
    {'province': 'Hải Dương', 'district': 'Thị Xã Kinh Môn', 'ward': 'Xã Lê Ninh'},
    {'province': 'Quảng Ngãi', 'district': 'Huyện Tư Nghĩa', 'ward': 'Thị Trấn La Hà'},
    {'province': 'HCM', 'district': 'Quận 1', 'ward': 'Phường Bến Nghé'},
    {'province': 'Hòa Bình', 'district': 'Huyện Kim Bôi', 'ward': 'Xã Xuân Thủy'},
    {'province': 'Lạng Sơn', 'district': 'Huyện Hữu Lũng', 'ward': 'Xã Thiện Tân'}
]

df = pd.DataFrame(data)
standardized_df = standardize_admin_unit_columns(df, province='province', district='district', ward='ward', convert_mode='CONVERT_2025')
print(standardized_df.to_markdown(index=False))
```

| province   | district        | ward            | standardized_province   | standardized_ward   |
|:-----------|:----------------|:----------------|:------------------------|:--------------------|
| Hải Dương  | Thị Xã Kinh Môn | Xã Lê Ninh      | Hải Phòng               | Bắc An Phụ          |
| Quảng Ngãi | Huyện Tư Nghĩa  | Thị Trấn La Hà  | Quảng Ngãi              | Tư Nghĩa            |
| HCM        | Quận 1          | Phường Bến Nghé | Hồ Chí Minh             | Sài Gòn             |
| Hòa Bình   | Huyện Kim Bôi   | Xã Xuân Thủy    | Phú Thọ                 | Nật Sơn             |
| Lạng Sơn   | Huyện Hữu Lũng  | Xã Thiện Tân    | Lạng Sơn                | Thiện Tân           |


#### convert_address_column()
Convert an address column in a DataFrame.

```python
from vietnamadminunits.pandas import convert_address_column

convert_address_column(df, address, convert_mode='CONVERT_2025', inplace=False, prefix='converted_', suffix='', short_name=True, show_progress=True)
```
**Params**:
- `df`: `pandas.DataFrame` object.
- `address`: Address column name. Best value format *"(street), ward, district, province"*.
- `convert_mode`: Currently, only `'CONVERT_2025'` is supported.
- `inplace`: Replace the original columns with standardized values; otherwise add new columns. Default `False`.
- `prefix`, `suffix` — Added to new column names if `inplace=False`.
- `short_name`: Use short or full names for administrative units. Default `True`.
- `show_progress`: Display a progress bar during processing. Default `True`.

**Returns**: `pandas.DataFrame` object.

**Example**:
```python
data = {
    'address': [
        'Ngã 4 xóm ao dài, thôn Tự Khoát, Xã Ngũ Hiệp, Huyện Thanh Trì, Hà Nội',
        '50 ngõ 133 thái hà, hà nội, Phường Trung Liệt, Quận Đống Đa, Hà Nội',
        'P402 CT9A KĐT VIỆT HƯNG, Phường Đức Giang, Quận Long Biên, Hà Nội',
        '169/8A, Thoại Ngọc Hầu, Phường Phú Thạnh, Quận Tân Phú, TP. Hồ Chí Minh',
        '02 lê đại hành, phường 15, quận 11, tp.hcm, Phường 15, Quận 11, TP. Hồ Chí Minh'
    ]
}

df = pd.DataFrame(data)

converted_df = convert_address_column(df, address='address', short_name=False)
print(converted_df.to_markdown(index=False))
```

| address                                                                         | converted_address                                        |
|:--------------------------------------------------------------------------------|:---------------------------------------------------------|
| Ngã 4 xóm ao dài, thôn Tự Khoát, Xã Ngũ Hiệp, Huyện Thanh Trì, Hà Nội           | Ngã 4 Xóm Ao Dài, Xã Thanh Trì, Thủ đô Hà Nội            |
| 50 ngõ 133 thái hà, hà nội, Phường Trung Liệt, Quận Đống Đa, Hà Nội             | 50 Ngõ 133 Thái Hà, Phường Đống Đa, Thủ đô Hà Nội        |
| P402 CT9A KĐT VIỆT HƯNG, Phường Đức Giang, Quận Long Biên, Hà Nội               | P402 Ct9A Kđt Việt Hưng, Phường Việt Hưng, Thủ đô Hà Nội |
| 169/8A, Thoại Ngọc Hầu, Phường Phú Thạnh, Quận Tân Phú, TP. Hồ Chí Minh         | 169/8A, Phường Phú Thạnh, Thành phố Hồ Chí Minh          |
| 02 lê đại hành, phường 15, quận 11, tp.hcm, Phường 15, Quận 11, TP. Hồ Chí Minh | 02 Lê Đại Hành, Phường Phú Thọ, Thành phố Hồ Chí Minh    |



### 🗃️ database

Retrieve administrative unit data from the database.
```python
from vietnamadminunits.database import get_data, query

get_data(fields='*', table='admin_units', limit=None)
```

**Params**:
- `fields`: Column name(s) to retrieve.
- `table`: Table name, either `'admin_units'` (34-province) or `'admin_units_legacy'` (63-province).

**Returns**: Data as a list of JSON-like dictionaries. It is compatible with `pandas.DataFrame`.

**Example**:
```python
data = get_data(fields=['province', 'ward'], limit=5)

the_same_date = query("SELECT province, ward FROM admin_units LIMIT 5")

print(data)
```
```text
[{'province': 'Thủ đô Hà Nội', 'ward': 'Phường Hồng Hà'}, {'province': 'Thủ đô Hà Nội', 'ward': 'Phường Ba Đình'}, {'province': 'Thủ đô Hà Nội', 'ward': 'Phường Ngọc Hà'}, {'province': 'Thủ đô Hà Nội', 'ward': 'Phường Giảng Võ'}, {'province': 'Thủ đô Hà Nội', 'ward': 'Phường Hoàn Kiếm'}]
```

## My Approach

### 🛠️ Dataset Preparation

1. **Data Sources**  
   Raw data was collected from reputable sources:  
   - [danhmuchanhchinh.gso.gov.vn](https://danhmuchanhchinh.gso.gov.vn)  
   - [sapnhap.bando.com.vn](https://sapnhap.bando.com.vn)  
   - [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview)

2. **Cleaning, Mapping & Enrichment**  
   The data was cleaned, normalized, enriched, and saved to [data/processed/](data/processed).  
   These finalized datasets are designed for community sharing and are directly used by the [`vietnamadminunits`](https://pypi.org/project/vietnamadminunits) Python package.
   
   For **wards that were divided into multiple new wards**, a flag `isDefaultNewWard=True` is assigned to the most appropriate match using [this solution](CHALLENGES.md#convert-2025).

3. **Longevity of Legacy Data**  
   The **63-province dataset** and the **mapping from 63-province to 34-province dataset** are considered stable and will not be updated unless there are spelling corrections.

4. **Maintaining the Latest Data**  
   The **34-province dataset** will be kept up to date as the Vietnamese government announces changes to administrative boundaries.

### 🧠 Parser Strategy

The parser resolves administrative units by matching address strings to known keywords.  
Here's a simplified step-by-step demonstration of how the parser identifies a province from a given address:

```python
import re

# Step 1: Define a keyword dictionary for each province.
DICT_PROVINCE = {
    'thudohanoi': {
        'provinceKeywords': ['thudohanoi', 'hanoi', 'hn'],
        'province': 'Thủ đô Hà Nội',
        'provinceShort': 'Hà Nội',
        'provinceLat': 21.0001,
        'provinceLon': 105.698
    },
    'tinhtuyenquang': {
        'provinceKeywords': ['tinhtuyenquang', 'tuyenquang'],
        'province': 'Tỉnh Tuyên Quang',
        'provinceShort': 'Tuyên Quang',
        'provinceLat': 22.4897,
        'provinceLon': 105.099
    }
}

# Step 2: Build a regex pattern from keywords, sorted by length (descending)
province_keywords = sorted(sum([v['provinceKeywords'] for v in DICT_PROVINCE.values()], []), key=len, reverse=True)

# Step 3: Compile a regex pattern to match any keyword
PATTERN_PROVINCE = re.compile('|'.join(province_keywords), flags=re.IGNORECASE)

# Step 4: Normalize the input address (e.g. remove accents, convert to lowercase, etc.)
address_key = 'hoangkiem,hn'

# Step 5: Search for the last matching keyword in the address
province_keyword = next((m.group() for m in reversed(list(PATTERN_PROVINCE.finditer(address_key)))), None)

# Step 6: Map keyword back to province key and metadata.
province_key = next((k for k, v in DICT_PROVINCE.items() if province_keyword in v['provinceKeywords']), None)

# Output
print(province_key)                              # thudohanoi
print(DICT_PROVINCE[province_key]['province'])   # Thủ đô Hà Nội
```


### 🔁 Converter Strategy

The converter transforms an address written in the **old (63-province)** format into a corresponding `AdminUnit` object based on the **new (34-province)** structure.

#### Step 1: Parse the old address  
The old address is first parsed into an `AdminUnit` object using the 63-province format. This allows us to extract:
- `province_key`
- `district_key`
- `ward_key`
- `street` (if available)

#### Step 2: Handle provinces and non-divided wards
The mapping approach is identical to the [Parser Strategy](#-parser-strategy) described earlier — keyword matching is sufficient.

#### Step 3: Handle divided wards (`isDividedWard=True`)
If a ward has been split into multiple new wards:

- **Without street information**: The converter defaults to the ward with `isDefaultNewWard=True`.

- **With street information**: Use [this solution](CHALLENGES.md#convert-2025).
  
## Contributing
Contributions, issues and feature requests are welcome!  
Feel free to submit a pull request or open an issue.
