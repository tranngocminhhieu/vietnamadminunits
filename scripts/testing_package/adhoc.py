from vietnamadminunits import parse_address, convert_address
from vietnamadminunits.pandas import standardize_admin_unit_columns, convert_address_column
import pandas as pd

# print(parse_address('02 trường chinh, coopmart, ok ok p15 tan binh, hcm', mode='LEGACY'))

# print(convert_address('02 trường chinh, coopmart, tan binh, hcm'))


# data = [
#     {'province': 'zz', 'ward': 'hong ha'},
#     {'province': 'hanoi', 'ward': 'ba đình'},
#     {'province': 'ha noi', 'ward': 'giang vo'},
#     {'province': 'ha noi', 'ward': 'hoan kiem'},
#     {'province': 'Hà Nội', 'ward': 'Ngọc Hà'},
# ]

# df = pd.DataFrame(data)
# sd_df = standardize_admin_unit_columns(df, province='province', ward='ward')
# print(sd_df.to_markdown(index=False))

print(parse_address('Thôn 2 Xã Long Bình, Xã Long Bình, Huyện Phú Riềng, Bình Phước', mode='LEGACY'))