# 2025-08-04 (Version 0.8.0)
[vietnamadminunits/data/parser_legacy.json](vietnamadminunits/data/parser_legacy.json): Add more than 700 alias keywords for ward level.

[vietnamadminunits/parser/parser_legacy.py](vietnamadminunits/parser/parser_legacy.py):
- Support old divided districts and duplicated short districts. Example:
  - "Kỳ Anh, Hà Tĩnh" -> "Thị xã Kỳ Anh, Tỉnh Hà Tĩnh"
  - "Kỳ Khang, Kỳ Anh, Hà Tĩnh" -> "Xã Kỳ Khang, Huyện Kỳ Anh, Tỉnh Hà Tĩnh"

- Support `province_code`, `district_code`, `ward_code` attributes.

[vietnamadminunits/parser/objects.py](vietnamadminunits/parser/objects.py): AdminUnit have `province_code`, `district_code`, `ward_code` attributes

[vietnamadminunits/parser/parser_from_2025.py](vietnamadminunits/parser/parser_from_2025.py):
- Support `province_code`, `district_code`, `ward_code` attributes.


Update correct province code, ward code for from-2025 dataset and package data.

# 2025-08-04 (Version 0.7.0)
[vietnamadminunits/pandas/main.py](vietnamadminunits/pandas/main.py): Support show progress bar with arg `show_progress`.

# 2025-08-04 (Version 0.6.0)
[vietnamadminunits/parser/__init__.py](vietnamadminunits/parser/__init__.py): Support `level=0` in `parse_address()` to choose the highest level automatically.

[vietnamadminunits/parser/utils.py](vietnamadminunits/parser/utils.py): Improve accuracy of `extract_street()`.

Old:
```python
def extract_street(address, address_key):
    remaining_parts = [part.strip() for part in address_key.split(',') if part.strip()]
    for part in remaining_parts:
        norm_part = key_normalize(part)
        words = address.split(',')
        for word in words:
            if key_normalize(word).startswith(norm_part):
                return word.strip().title()
    return None
```

New:
```python
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
```

[vietnamadminunits/parser/parser_legacy.py](vietnamadminunits/parser/parser_legacy.py):
Allow bypass check comma count when ward_key is existed.

[vietnamadminunits/parser/parser_from_2025.py](vietnamadminunits/parser/parser_from_2025.py):
Allow bypass check comma count when ward_key is existed.

# 2025-08-04 (Version 0.5.0)
[vietnamadminunits/parser/objects.py](vietnamadminunits/parser/objects.py): Support `short_name` arg for `AdminUnit`'s `get_address()`.

[vietnamadminunits/pandas/main.py](vietnamadminunits/pandas/main.py): Add a new function `convert_address_column()`.

# 2025-08-03 (Version 0.4.0)
[vietnamadminunits/data/parser_legacy.json](vietnamadminunits/data/parser_legacy.json):
- Add more alias keywords for district and ward level.
- Add 0 for numeric districts and numeric wards. Eg: quan01, phuong01.

[vietnamadminunits/converter/converter_2025.py](vietnamadminunits/converter/converter_2025.py): Fix wrong arg in `nearest_point = find_nearest_point(a_point=old_point, list_of_b_points=new_ward_points)`

# 2025-08-02 (Version 0.2.0)
Public [vietnamadminunits](vietnamadminunits)