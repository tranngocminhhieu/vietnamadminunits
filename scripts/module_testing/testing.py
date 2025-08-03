from vietnamadminunits import parse_address
from vietnamadminunits.parser.parser_legacy import parse_address_legacy

# print(parse_address('nguyen thai binh, quan 1, ho chi minh', mode='LEGACY'))
print(parse_address_legacy('Phường Nguyễn Thái Bình, Quận 01 ,Thành Phố Hồ Chí Minh'))