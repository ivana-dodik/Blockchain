class LandBook:
    def __init__(self, surface_area, sale_price, previous_owner, current_owner, contract_date, address):
        self.surface_area = surface_area
        self.sale_price = sale_price
        self.previous_owner = previous_owner
        self.current_owner = current_owner
        self.contract_date = contract_date
        self.address = address
    
    def __json__(self):
        return {
            'surface_area': self.surface_area,
            'sale_price': self.sale_price,
            'previous_owner': self.previous_owner,
            'current_owner': self.current_owner,
            'contract_date': self.contract_date,
            'address': self.address
        }