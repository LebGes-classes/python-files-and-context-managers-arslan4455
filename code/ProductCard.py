class ProductCard:
    """
    Представляет расширенную карточку товара.
    
    Поля: №, ID, Наименование, Количество, Состояние, 
    Поставщик, Производитель, Стоимость, Местоположение, Город.
    """
    
    def __init__(self, index: str, product_id: str, name: str, quantity: int, 
                 condition: str, supplier: str, manufacturer: str, 
                 price: float, location: str, city: str):
        self.index = index
        self.product_id = product_id
        self.name = name
        self.quantity = int(quantity)
        self.condition = condition
        self.supplier = supplier
        self.manufacturer = manufacturer
        self.price = float(price)
        self.location = location
        self.city = city

    def to_dict(self) -> dict:
        """Сериализация объекта в словарь."""
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> 'ProductCard':
        """Десериализация словаря в объект."""
        return cls(**data)

    def __repr__(self):
        return (f"#{self.index} | ID:{self.product_id} | {self.name} | "
                f"{self.quantity}шт. | {self.price}р. | {self.city}")