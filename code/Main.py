import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional

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

# --- Абстрактные интерфейсы ---

class BaseSerializer(ABC):
    """Базовый интерфейс для сохранения данных."""
    @abstractmethod
    def serialize(self, products: List[ProductCard], filepath: str): pass

class BaseDeserializer(ABC):
    """Базовый интерфейс для загрузки данных."""
    @abstractmethod
    def deserialize(self, filepath: str) -> List[ProductCard]: pass

# --- Реализация JSON ---

class JsonSerializer(BaseSerializer):
    """Класс для записи данных в JSON-формат."""
    def serialize(self, products: List[ProductCard], filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in products], f, ensure_ascii=False, indent=4)

class JsonDeserializer(BaseDeserializer):
    """Класс для чтения данных из JSON-формата."""
    def deserialize(self, filepath: str) -> List[ProductCard]:
        if not os.path.exists(filepath): return []
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return [ProductCard.from_dict(item) for item in data]
            except: return []

# --- Реализация TXT ---

class TxtDeserializer(BaseDeserializer):
    """Класс для чтения из TXT с пропуском заголовка."""
    def deserialize(self, filepath: str) -> List[ProductCard]:
        if not os.path.exists(filepath): return []
        products = []
        with open(filepath, 'r', encoding='utf-8') as f:
            next(f, None)  # ПРОПУСК ПЕРВОЙ СТРОКИ (заголовка)
            for line in f:
                p = line.strip().split(';')
                if len(p) == 10:
                    products.append(ProductCard(p[0], p[1], p[2], int(p[3]), 
                                              p[4], p[5], p[6], float(p[7][:-5]), 
                                              p[8], p[9]))
        return products

# --- Менеджер и Интерфейс ---

class CatalogManager:
    """Менеджер управления каталогом с синхронизацией в JSON."""
    def __init__(self, json_file='catalog.json', txt_file='catalog.txt'):
        self.json_file = json_file
        self.txt_file = txt_file
        self.js_ser = JsonSerializer()
        self.js_des = JsonDeserializer()
        self.tx_des = TxtDeserializer()
        self.products: Dict[str, ProductCard] = self._initial_load()

    def _initial_load(self):
        if os.path.exists(self.json_file):
            return {p.product_id: p for p in self.js_des.deserialize(self.json_file)}
        elif os.path.exists(self.txt_file):
            prods = self.tx_des.deserialize(self.txt_file)
            self.js_ser.serialize(prods, self.json_file)
            return {p.product_id: p for p in prods}
        return {}

    def _save(self):
        self.js_ser.serialize(list(self.products.values()), self.json_file)

    def add(self, data: dict):
        if data['product_id'] in self.products: return False
        self.products[data['product_id']] = ProductCard(**data)
        self._save()
        return True

    def update(self, p_id: str, **kwargs):
        if p_id not in self.products: return False
        product = self.products[p_id]
        for key, value in kwargs.items():
            if hasattr(product, key) and value:
                setattr(product, key, value)
        self._save()
        return True

    def remove(self, p_id: str):
        if p_id in self.products:
            del self.products[p_id]
            self._save()
            return True
        return False

class ConsoleUI:
    """Консольный пользовательский интерфейс."""
    def __init__(self, manager: CatalogManager):
        self.manager = manager
        self.fields = ["index", "product_id", "name", "quantity", "condition", 
                       "supplier", "manufacturer", "price", "location", "city"]

    def run(self):
        while True:
            print("\n1.Список 2.Добавить 3.Изменить 4.Удалить 0.Выход")
            cmd = input(">> ")
            if cmd == '1': self.show()
            elif cmd == '2': self.add()
            elif cmd == '3': self.edit()
            elif cmd == '4': self.delete()
            elif cmd == '0': break

    def show(self):
        for p in self.manager.products.values(): print(p)

    def add(self):
        data = {}
        try:
            for field in self.fields:
                data[field] = input(f"{field}: ")
            if self.manager.add(data): print("Успешно!")
            else: print("Ошибка: ID занят.")
        except ValueError: print("Ошибка: проверьте числовые поля.")

    def edit(self):
        p_id = input("ID товара: ")
        print("Введите новые значения (пусто - пропустить):")
        updates = {f: input(f"{f}: ") for f in self.fields if f != 'product_id'}
        if self.manager.update(p_id, **updates): print("Обновлено.")
        else: print("Не найден.")

    def delete(self):
        if self.manager.remove(input("ID для удаления: ")): print("Удалено.")
        else: print("Не найден.")

if __name__ == "__main__":
    ui = ConsoleUI(CatalogManager())
    ui.run()