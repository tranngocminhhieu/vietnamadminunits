from vietnamadminunits import parse_address, convert_address
from vietnamadminunits.pandas import standardize_admin_unit_columns, convert_address_column
import pandas as pd

print(parse_address('02 trường chinh, coopmart, p15 tan binh, hcm', mode='LEGACY'))

# print(convert_address('02 trường chinh, coopmart, p15 tan binh, hcm'))