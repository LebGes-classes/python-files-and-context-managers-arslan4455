import os, json
from abc import ABC, abstractmethod
from typing import List
from ProductCard import ProductCard

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
                                              p[4], p[5], p[6], float(p[7]), 
                                              p[8], p[9]))
        return products