from Parsers import JsonDeserializer, JsonSerializer, TxtDeserializer
from typing import Dict, Tuple
from ProductCard import ProductCard
import os


class CatalogManager:
    """Менеджер управления каталогом с синхронизацией в JSON."""
    def __init__(self, json_file='catalog.json', txt_file='data.txt'):
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