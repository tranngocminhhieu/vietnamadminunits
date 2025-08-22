from vietnamadminunits import parse_address, convert_address
from vietnamadminunits.pandas import standardize_admin_unit_columns, convert_address_column
import pandas as pd


print(parse_address('Long Thành, thu thua, long an', mode='LEGACY'))