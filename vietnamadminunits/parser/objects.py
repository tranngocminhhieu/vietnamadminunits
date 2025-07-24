class AdminUnit:
    def __init__(self,
                 address=None,
                 province=None,
                 district=None,
                 ward=None,
                 street=None,

                 short_province=None,
                 short_district=None,
                 short_ward=None,

                 district_type=None,
                 ward_type=None,

                 province_key=None,
                 district_key=None,
                 ward_key=None,

                 latitude = None,
                 longitude = None,

                 show_district = False
                 ):
        self.address = address
        self.province = province
        self.district = district
        self.ward = ward
        self.street = street

        self.short_province = short_province
        self.short_district = short_district
        self.short_ward = short_ward

        self.district_type = district_type
        self.ward_type = ward_type
        self.province_key = province_key
        self.district_key = district_key
        self.ward_key = ward_key

        self.latitude = latitude
        self.longitude = longitude

        self.show_district = show_district

    def get_address(self):
        components = [self.street,  self.ward, self.district, self.province]
        components = [i for i in components if i]
        return ', '.join(components)

    def __repr__(self):
        def safe_format(value):
            return value if value is not None else ""

        attributes = [
            'province', 'district', 'ward', 'street',
            'short_province', 'short_district', 'short_ward',
            'district_type', 'ward_type', 'latitude', 'longitude',
        ]

        if not self.show_district:
            attributes = [a for a in attributes if 'district' not in  a]

        lines = [f"{'Attribute':<15} | {'Value':<25}", '-' * 40]
        for attr in attributes:
            lines.append(f"{attr:<15} | {safe_format(getattr(self, attr)):<25}")

        return f"Admin Unit: {self.get_address()}\n" + '\n'.join(lines)