# 2025-08-04 (Version 0.5.0)
[ietnamadminunits/parser/objects.py](vietnamadminunits/parser/objects.py): Support `short_name` arg for `AdminUnit`'s `get_address()`.

[vietnamadminunits/pandas/main.py](vietnamadminunits/pandas/main.py): Add a new function `convert_address_column()`.

# 2025-08-03 (Version 0.4.0)
[vietnamadminunits/data/parser_legacy.json](vietnamadminunits/data/parser_legacy.json):
- Add more alias keywords for district and ward level.
- Add 0 for numeric districts and numeric wards. Eg: quan01, phuong01.

[vietnamadminunits/converter/converter_2025.py](vietnamadminunits/converter/converter_2025.py): Fix wrong arg in `nearest_point = find_nearest_point(a_point=old_point, list_of_b_points=new_ward_points)`

# 2025-08-02 (Version 0.2.0)
Public [vietnamadminunits](vietnamadminunits)