class Unit:
    def __init__(self,
                 address=None,
                 province=None,
                 district=None,
                 ward=None,
                 street=None
                 ):
        self.address = address
        self.province = province
        self.district = district
        self.ward = ward
        self.street = street

    def __str__(self):
        components = [self.street,  self.ward, self.district, self.province]
        components = [i for i in components if i]
        return ', '.join(components)

    def __repr__(self):
        components = [self.street, self.ward, self.district, self.province]
        components = [i for i in components if i]
        return ', '.join(components)