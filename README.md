# Vietnam Admin Units
A shared effort to standardize and convert Vietnam's administrative units across major restructuring events.

## Introduction
This project is a personal contribution to the open-data and developer community in Vietnam.  
It aims to provide a reliable and up-to-date reference for Vietnam’s administrative units,  
especially in light of the 2025 province restructuring.

> I believe in building tools that help others solve problems faster — and this is one such attempt.
## Project Structure

### 📊 Datasets
- Located in [`data/processed/`](data/processed).
- Includes:
  - 63-province dataset.
  - 34-province dataset.
  - Mapping from 63 to 34 provinces dataset.

### 🐍 Python package

- Core logic is in the [`vietnamadminunits`](vietnamadminunits/) package.
- Includes `parse_address()`, `convert_address()` and more functions.

## Usage

### 📦 Installation
Install via pip:
```shell
pip install vietnamadminunits
```

### 🧾 parse_address
Parse an address to an `AdminUnit` object.
```python
from vietnamadminunits import parse_address

parse_address(address, mode=34, keep_street=True, level=2)
```

**Params**:

- `address`: The best structure is `(street), ward, (district), province`. Don't worry too much about case or spelling.
- `mode`: Modes `34` and `63` refer to administrative units. Mode `34` represents the new unit effective July 2025, while mode `63` refers to the former unit before the merger.
- `keep_street`: Keep the street after parsing, but this only works if the address includes enough commas: mode 63 requires at least 3 commas, while mode 34 requires at least 2.
- `level`: Use levels `1` and `2` with `mode=34`, and levels `1`, `2`, or `3` with `mode=63`, depending on the desired granularity.

**Returns**: `AdminUnit` object.

**Example**:

Parse an address with new administrative unit.

```python
address = '70 Nguyễn Sỹ Sách, Tan Son, tp.HCM'

admin_unit = parse_address(address=address, mode=34, keep_street=True, level=2)

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

Parse an address with old administrative unit.

```python
address = '70 nguyễn sỹ sách, p.15, Tân Bình, Tp.HCM' # Old administrative unit address structure

admin_unit = parse_address(address=address, mode=63, keep_street=True, level=3) # Changed mode and level

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

### 🔄 convert_address
Converts an address written in the **old (63-province)** structure into an `AdminUnit` object using the **new (34-province)** system.

```python
from vietnamadminunits import convert_address
```

**Params**:
- `address`: The best structure is `(street), ward, district, province`. Don't worry too much about case or spelling.

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
Standardizes province, district, and ward columns in a DataFrame using predefined administrative mappings.

```python
from vietnamadminunits.pandas import standardize_admin_unit_columns

standardize_admin_unit_columns(
    df, 
    province, 
    district=None, 
    ward=None, 
    mode=34, 
    inplace=False, 
    prefix='standardized_', 
    suffix='', 
    short_name=True, 
    convert_to_latest=False
)
```

**Params**:
- `df`: `pandas.DataFrame` object.
- `province`: Province column name.
- `district`: District column name.
- `ward`: Ward column name.
- `mode`: Modes `34` and `63` refer to administrative units. Mode `34` represents the new unit effective July 2025, while mode `63` refers to the former unit before the merger.
- `inplace`: Replace the original columns with standardized values instead of adding new ones.
- `prefix`: Add a prefix to the column names if `inplace=False`.
- `suffix`: Add a suffix to the column names if `inplace=False`.
- `short_name`: Use short or full names for standardized administrative units.
- `convert_to_latest`: Convert old administrative units to the latest structure.


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

print(df.to_markdown(index=False))
```
```text
| province      | ward             |
|:--------------|:-----------------|
| Thủ đô Hà Nội | Phường Hồng Hà   |
| Thủ đô Hà Nội | Phường Ba Đình   |
| Thủ đô Hà Nội | Phường Ngọc Hà   |
| Thủ đô Hà Nội | Phường Giảng Võ  |
| Thủ đô Hà Nội | Phường Hoàn Kiếm |
```

```python
standardized_df = standardize_admin_unit_columns(df=df, province='province', ward='ward', inplace=False, short_name=True)

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


Standardize and convert legacy administrative unit columns to the new 34-province system.

```python
data = [
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Tân Định'},
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Đa Kao'},
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Bến Nghé'},
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Bến Thành'},
    {'province': 'Thành phố Hồ Chí Minh', 'district': 'Quận 1', 'ward': 'Phường Nguyễn Thái Bình'}
]

df = pd.DataFrame(data)

print(df.to_markdown(index=False))
```
```text
| province              | district   | ward                    |
|:----------------------|:-----------|:------------------------|
| Thành phố Hồ Chí Minh | Quận 1     | Phường Tân Định         |
| Thành phố Hồ Chí Minh | Quận 1     | Phường Đa Kao           |
| Thành phố Hồ Chí Minh | Quận 1     | Phường Bến Nghé         |
| Thành phố Hồ Chí Minh | Quận 1     | Phường Bến Thành        |
| Thành phố Hồ Chí Minh | Quận 1     | Phường Nguyễn Thái Bình |
```

```python
standardized_df = standardize_admin_unit_columns(
    df=df, 
    province='province', 
    district='district', 
    ward='ward', 
    mode=63, 
    inplace=True, 
    short_name=True, 
    convert_to_latest=True
)

print(standardized_df.to_markdown(index=False))
```

```text
| province    | ward      |
|:------------|:----------|
| Hồ Chí Minh | Tân Định  |
| Hồ Chí Minh | Sài Gòn   |
| Hồ Chí Minh | Sài Gòn   |
| Hồ Chí Minh | Bến Thành |
| Hồ Chí Minh | Bến Thành |
```

### 🗃️ database

Retrieve administrative unit data from the database.
```python
from vietnamadminunits.database import get_data, query

get_data(fields='*', table='admin_units', limit=None)
```

**Params**:
- `fields`: Column name(s) to retrieve.
- `table`: Table name, either `'admin_units'` (34 provinces) or `'admin_units_63'` (legacy 63 provinces).

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

   - Although the resulting data is already reliable and highly usable, I originally intended to enrich it further by collecting **street names** that clearly fall within specific new wards. This would improve address resolution for wards that were split. However, due to the lack of trustworthy street-level data, this enhancement has not been implemented yet.

3. **Longevity of Legacy Data**  
   - The **63-province dataset** and the **mapping from 63 to 34 provinces dataset** are considered stable and will not be updated unless there are spelling corrections.

4. **Maintaining the Latest Data**  
   - The **34-province dataset** will be kept up to date as the Vietnamese government announces changes to administrative boundaries.

### Parser strategy





### Converter strategy

### Maintaining in the future


