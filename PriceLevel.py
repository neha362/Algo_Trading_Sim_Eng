'''
- Price Level class
    - order objects at the same price
'''

class PriceLevel: 
    def __init__(self, price):
        self.price = price
        self.orders = []
        self.total_volume = 0