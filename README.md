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
- Located in [`data/processed/`](data/processed).
- Includes:
  - 63-province dataset.
  - 34-province dataset.
  - Mapping from 63-province to 34-province dataset.

### 🐍 Python package

- Core logic is in the [`vietnamadminunits`](vietnamadminunits/) package.
- Includes `parse_address()`, `convert_address()` and more functions.

## Usage

### 📦 Installation
Install via pip:
```shell
pip install vietnamadminunits
```
Update to latest version:
```shell
pip install --upgrade vietnamadminunits
```

### 🧾 parse_address()
Parse an address to an `AdminUnit` object.
```python
from vietnamadminunits import parse_address, ParseMode

parse_address(address, mode=ParseMode.latest(), keep_street=True, level=2)
```

**Params**:

- `address`: The best structure is `(street), ward, (district), province`. Don't worry too much about case or accenting.
- `mode`: One of the `ParseMode` values. Use `'LEGACY'` for the 63-province format (pre-merger), or `'FROM_2025'` for the new 34-province format. Default is `ParseMode.latest()`.
- `keep_street`: Keep the street after parsing, but this only works if the address includes enough commas: `'LEGACY'` mode requires at least 3 commas, while `'FROM_2025'` mode requires at least 2.
- `level`: Use levels `1` and `2` with `'FROM_2025'` mode, and levels `1`, `2`, or `3` with `'LEGACY'` mode, depending on the desired granularity.

**Returns**: `AdminUnit` object.

**Example**:

Parse a new address (from 2025).

```python
address = '70 Nguyễn Sỹ Sách, Tan Son, tp.HCM'

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
address = '70 nguyễn sỹ sách, p.15, Tân Bình, Tp.HCM' # Old administrative unit address structure

admin_unit = parse_address(address, mode='LEGACY', level=3) # Use 'LEGACY' or ParseMode.LEGACY for mode

print(admin_unit)
```
```text
Admin Unit: 70 Nguyễn Sỹ Sách, Phường 15, Quận Tân Bình, Thành phố Hồ Chí Minh
Attribute       | Value                    
----------------------------------------
province        | Thành phố Hồ Chí Minh    
district        | Quận Tân Bình            
ward            | Phường 15                
street          | 70 Nguyễn Sỹ Sách        
short_province  | Hồ Chí Minh              
short_district  | Tân Bình                 
short_ward      | Phường 15                
district_type   | Quận                     
ward_type       | Phường                   
latitude        | 10.823333                
longitude       | 106.63616                
```

### 🔄 convert_address()
Converts an address from the old 63-province format to a standardized 34-province `AdminUnit`.

```python
from vietnamadminunits import convert_address

convert_address(address, mode='CONVERT_2025')
```

**Params**:
- `address`: The best structure is `(street), ward, district, province`. Don't worry too much about case or accenting.
- `mode`: One of the `ConvertMode` values. Currently, only `'CONVERT_2025'` is supported.

**Returns**: `AdminUnit` object.

**Example**:

```python
address = '70 nguyễn sỹ sách, p.15, Tân Bình, Tp.HCM' # Old administrative unit address structure

admin_unit = convert_address(address)

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
latitude        | 10.8224                  
longitude       | 106.65                   
```

### 🐼 Pandas
#### standardize_admin_unit_columns()

Standardizes administrative unit columns (`province`, `district`, `ward`) in a DataFrame.

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
- `parse_mode`: One of the `ParseMode` values. Use `'LEGACY'` for the 63-province format (pre-merger), or `'FROM_2025'` for the new 34-province format. Default is `ParseMode.latest()`.
- `convert_mode`: One of the `ConvertMode` values. Currently, only `'CONVERT_2025'` is supported.
- `inplace`: Replace the original columns with standardized values instead of adding new ones.
- `prefix`, `suffix` — Add to column names if `inplace=False`.
- `short_name`: Use short or full names for administrative units.
- `show_progress`: Show progress bar.


**Returns**: `pandas.DataFrame` object.

**Example**:

Standardize administrative unit columns in a DataFrame.

```python
import pandas as pd

data = [
    {'province': 'Thủ đô Hà Nội', 'ward': 'Phường Hồng Hà'},
    {'province': 'Thủ đô Hà Nội', 'ward': 'Phường Ba Đình'},
    {'province': 'Thủ đô Hà Nội', 'ward': 'Phường Ngọc Hà'},
    {'province': 'Thủ đô Hà Nội', 'ward': 'Phường Giảng Võ'},
    {'province': 'Thủ đô Hà Nội', 'ward': 'Phường Hoàn Kiếm'},
]

df = pd.DataFrame(data)

standardized_df = standardize_admin_unit_columns(df, province='province', ward='ward')

print(standardized_df.to_markdown(index=False))
```

```text
| province      | ward             | standardized_province   | standardized_ward   |
|:--------------|:-----------------|:------------------------|:--------------------|
| Thủ đô Hà Nội | Phường Hồng Hà   | Hà Nội                  | Hồng Hà             |
| Thủ đô Hà Nội | Phường Ba Đình   | Hà Nội                  | Ba Đình             |
| Thủ đô Hà Nội | Phường Ngọc Hà   | Hà Nội                  | Ngọc Hà             |
| Thủ đô Hà Nội | Phường Giảng Võ  | Hà Nội                  | Giảng Võ            |
| Thủ đô Hà Nội | Phường Hoàn Kiếm | Hà Nội                  | Hoàn Kiếm           |

```

Standardize and convert 63-province format administrative unit columns to the new 34-province format.

```python
data = [
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Tân Định'},
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Đa Kao'},
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Bến Nghé'},
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Bến Thành'},
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Nguyễn Thái Bình'}
]

df = pd.DataFrame(data)

standardized_df = standardize_admin_unit_columns(df, province='province', district='district', ward='ward', convert_mode='CONVERT_2025')

print(standardized_df.to_markdown(index=False))
```
```text
| province              | district   | ward                    | standardized_province   | standardized_ward   |
|:----------------------|:-----------|:------------------------|:------------------------|:--------------------|
| Thành phố Hồ Chí Minh | Quận 1     | Phường Tân Định         | Hồ Chí Minh             | Tân Định            |
| Thành phố Hồ Chí Minh | Quận 1     | Phường Đa Kao           | Hồ Chí Minh             | Sài Gòn             |
| Thành phố Hồ Chí Minh | Quận 1     | Phường Bến Nghé         | Hồ Chí Minh             | Sài Gòn             |
| Thành phố Hồ Chí Minh | Quận 1     | Phường Bến Thành        | Hồ Chí Minh             | Bến Thành           |
| Thành phố Hồ Chí Minh | Quận 1     | Phường Nguyễn Thái Bình | Hồ Chí Minh             | Bến Thành           |
```

#### convert_address_column()
Convert an address column in a DataFrame.

```python
from vietnamadminunits.pandas import convert_address_column

convert_address_column(df, address, convert_mode='CONVERT_2025', inplace=False, prefix='converted_', suffix='', short_name=True, show_progress=True)
```
**Params**:
- `df`: pandas.DataFrame object.
- `address`: Address column name. The address value must be in format `(street), ward, district, province`.
- `convert_mode`: One of the `ConvertMode` values. Currently, only `'CONVERT_2025'` is supported.
- `inplace`: Replace the original columns with converted values instead of adding new ones.
- `prefix`: Add a prefix to the column names if `inplace=False`.
- `suffix`: Add a suffix to the column names if `inplace=False`.
- `short_name`: Use short or full names for administrative unit in address.
- `show_progress`: Show progress bar.

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
```text
| address                                                                         | converted_address                                        |
|:--------------------------------------------------------------------------------|:---------------------------------------------------------|
| Ngã 4 xóm ao dài, thôn Tự Khoát, Xã Ngũ Hiệp, Huyện Thanh Trì, Hà Nội           | Ngã 4 Xóm Ao Dài, Xã Thanh Trì, Thủ đô Hà Nội            |
| 50 ngõ 133 thái hà, hà nội, Phường Trung Liệt, Quận Đống Đa, Hà Nội             | 50 Ngõ 133 Thái Hà, Phường Đống Đa, Thủ đô Hà Nội        |
| P402 CT9A KĐT VIỆT HƯNG, Phường Đức Giang, Quận Long Biên, Hà Nội               | P402 Ct9A Kđt Việt Hưng, Phường Việt Hưng, Thủ đô Hà Nội |
| 169/8A, Thoại Ngọc Hầu, Phường Phú Thạnh, Quận Tân Phú, TP. Hồ Chí Minh         | 169/8A, Phường Phú Thạnh, Thành phố Hồ Chí Minh          |
| 02 lê đại hành, phường 15, quận 11, tp.hcm, Phường 15, Quận 11, TP. Hồ Chí Minh | 02 Lê Đại Hành, Phường Phú Thọ, Thành phố Hồ Chí Minh    |
```


### 🗃️ database

Retrieve administrative unit data from the database.
```python
from vietnamadminunits.database import get_data, query

get_data(fields='*', table='admin_units', limit=None)
```

**Params**:
- `fields`: Column name(s) to retrieve.
- `table`: Table name, either `'admin_units'` (34 provinces) or `'admin_units_legacy'` (legacy 63 provinces).

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
   The data was cleaned, normalized, enriched, and saved to [`data/processed/`](data/processed).  
   These finalized datasets are designed for community sharing and are directly used by the [`vietnamadminunits`](https://pypi.org/project/vietnamadminunits) Python package.

   - For **wards that were split into multiple new wards**, a flag `isDefaultNewWard=True` is assigned to the most appropriate match.  
     The matching strategy is based on the **location (latitude/longitude)** of the old ward:

     - If only one new ward polygon contains the old ward’s location → that ward is set as default.
     - If multiple polygons match or none match → the new ward with the closest center point is selected as default.

   - Although the resulting data is already reliable and highly usable, there was an intent to enrich the dataset with precise street-level mappings for split wards.  
However, due to lack of reliable sources, this has not yet been implemented.

3. **Longevity of Legacy Data**  
   - The **63-province dataset** and the **mapping from 63-province to 34-province dataset** are considered stable and will not be updated unless there are spelling corrections.

4. **Maintaining the Latest Data**  
   - The **34-province dataset** will be kept up to date as the Vietnamese government announces changes to administrative boundaries.

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
The mapping approach is identical to the [**Parser Strategy**](#-parser-strategy) described earlier — keyword matching is sufficient.

#### Step 3: Handle divided wards (`isDividedWard=True`)
If a ward has been split into multiple new wards:

- **Without street information**:  
  The converter defaults to the ward with `isDefaultNewWard=True`.

- **With street information**:  
  The converter uses [**geopy**](https://pypi.org/project/geopy/) to geocode the address into latitude/longitude.  
  Then it compares this location with the centroids and polygons of new wards:

  - If exactly one new ward contains the location → that ward is selected.
  - If multiple wards match or none match → the new ward whose center is closest to the location is selected.


## Contributing
Contributions, issues and feature requests are welcome!  
Feel free to submit a pull request or open an issue.
