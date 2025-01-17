class House:
    PRICE_PER_SQUARE_FOOT = 3.0
    def __init__(self, size, num_beds, num_baths):
        self.size = size
        self.num_beds = num_beds 
        self.num_baths = num_baths
    @property
    def price(self):
        return self.size * self.PRICE_PER_SQUARE_FOOT


home_asg = House(4, 2, 2)
print(home_asg.price)
