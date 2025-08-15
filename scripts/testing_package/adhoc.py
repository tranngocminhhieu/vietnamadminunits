from vietnamadminunits import parse_address, convert_address
from vietnamadminunits.pandas import standardize_admin_unit_columns, convert_address_column
import pandas as pd


print(parse_address('nt Liên Sơn	Văn Chấn	Yên Bái', mode='LEGACY'))