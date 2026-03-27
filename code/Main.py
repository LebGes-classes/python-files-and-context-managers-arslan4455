import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List


class ProductCard:
    """
    Представляет расширенную карточку товара.
    
    Атрибуты:
        index (str): Порядковый номер товара или внутренний индекс.
        product_id (str): Уникальный идентификатор товара (артикул).
        name (str): Наименование товара.
        quantity (int): Количество единиц товара в наличии.
        condition (str): Состояние товара (например, 'Отличное', 'Б/У').
        supplier (str): Поставщик товара.
        manufacturer (str): Производитель товара.
        price (float): Стоимость товара в рублях.
        location (str): Местоположение товара на складе (например, номер полки).
        city (str): Город, в котором находится товар.
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
        """
        Сериализует объект карточки товара в словарь.

        Возвращает:
            dict: Словарь со всеми атрибутами товара.
        """
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> 'ProductCard':
        """
        Десериализует словарь в объект ProductCard.

        Аргументы:
            data (dict): Словарь с данными о товаре.

        Возвращает:
            ProductCard: Экземпляр карточки товара.
        """
        return cls(**data)

    def __repr__(self) -> str:
        """
        Возвращает строковое представление карточки товара для вывода в консоль.
        """
        return (f"#{self.index} | ID:{self.product_id} | {self.name} | "
                f"{self.quantity}шт. | {self.price}р. | {self.city}")

class BaseSerializer(ABC):
    """Базовый абстрактный класс для сохранения данных (сериализации)."""
    
    @abstractmethod
    def serialize(self, products: List[ProductCard], filepath: str):
        """
        Сохраняет список товаров в файл.

        Аргументы:
            products (List[ProductCard]): Список объектов товаров для сохранения.
            filepath (str): Путь к файлу для сохранения.
        """
        pass

class BaseDeserializer(ABC):
    """Базовый абстрактный класс для загрузки данных (десериализации)."""
    
    @abstractmethod
    def deserialize(self, filepath: str) -> List[ProductCard]:
        """
        Загружает список товаров из файла.

        Аргументы:
            filepath (str): Путь к файлу для чтения.

        Возвращает:
            List[ProductCard]: Список загруженных объектов товаров.
        """
        pass

class JsonSerializer(BaseSerializer):
    """Реализация сериализатора для сохранения данных в формате JSON."""
    
    def serialize(self, products: List[ProductCard], filepath: str):
        """
        Записывает список товаров в JSON-файл с отступами для читаемости.

        Аргументы:
            products (List[ProductCard]): Список товаров.
            filepath (str): Путь к JSON-файлу.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in products], f, ensure_ascii=False, indent=4)

class JsonDeserializer(BaseDeserializer):
    """Реализация десериализатора для чтения данных из формата JSON."""
    
    def deserialize(self, filepath: str) -> List[ProductCard]:
        """
        Читает товары из JSON-файла.

        Аргументы:
            filepath (str): Путь к JSON-файлу.

        Возвращает:
            List[ProductCard]: Список товаров. Если файл не найден или поврежден, возвращает пустой список.
        """
        if not os.path.exists(filepath): return []
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return [ProductCard.from_dict(item) for item in data]
            except: 
                return []

class TxtDeserializer(BaseDeserializer):
    """Реализация десериализатора для чтения данных из текстового CSV-подобного файла (разделитель ';')."""
    
    def deserialize(self, filepath: str) -> List[ProductCard]:
        """
        Читает товары из TXT-файла с учетом заголовков и разделителей.

        Аргументы:
            filepath (str): Путь к TXT-файлу.

        Возвращает:
            List[ProductCard]: Список успешно загруженных товаров.
        """
        if not os.path.exists(filepath): 
            print(f"Файл {filepath} не найден!")
            return []
        products = []
        with open(filepath, 'r', encoding='utf-8') as f:
            header = next(f, None)
            print(f"Пропущена шапка: {header.strip() if header else 'пусто'}")
            for line_no, line in enumerate(f, 2):
                p = line.strip().split(';')
                if len(p) != 10:
                    print(f"Ошибка в строке {line_no}: Ожидалось 10 колонок, найдено {len(p)}")
                    continue
                try:
                    products.append(ProductCard(p[0], p[1], p[2], int(p[3]), 
                                              p[4], p[5], p[6], float(p[7][:-4]), 
                                              p[8], p[9]))
                except ValueError as e:
                    print(f"Ошибка типов в строке {line_no}: {e}")
        return products

class CatalogManager:
    """
    Менеджер для управления каталогом товаров.
    Обеспечивает операции CRUD (создание, чтение, обновление, удаление) и 
    автоматическую синхронизацию данных с JSON-файлом.
    """
    
    def __init__(self, json_file='catalog.json', txt_file='catalog.txt'):
        """
        Инициализирует менеджер каталога.

        Аргументы:
            json_file (str): Путь к основному JSON-файлу базы данных.
            txt_file (str): Путь к резервному/импортируемому TXT-файлу.
        """
        self.json_file = json_file
        self.txt_file = txt_file
        self.js_ser = JsonSerializer()
        self.js_des = JsonDeserializer()
        self.tx_des = TxtDeserializer()
        self.products: Dict[str, ProductCard] = self._initial_load()

    def _initial_load(self) -> Dict[str, ProductCard]:
        """
        Выполняет первичную загрузку данных. Сначала пытается загрузить из JSON,
        если он пуст или отсутствует — пытается импортировать из TXT.

        Возвращает:
            Dict[str, ProductCard]: Словарь товаров, где ключ — ID товара.
        """
        json_data = []
        if os.path.exists(self.json_file):
            json_data = self.js_des.deserialize(self.json_file)
        
        if not json_data:
            print("Поиск данных в TXT...") # Отладочное сообщение
            txt_data = self.tx_des.deserialize(self.txt_file)
            if txt_data:
                print(f"Загружено из TXT: {len(txt_data)} шт.")
                # Сразу сохраняем в JSON, чтобы в следующий раз брать оттуда
                self.js_ser.serialize(txt_data, self.json_file)
                return {p.product_id: p for p in txt_data}
            else:
                print("TXT файл тоже пуст или не найден.")
                return {}
            
        return {p.product_id: p for p in json_data}

    def _save(self):
        """Внутренний метод для сохранения текущего состояния каталога в JSON-файл."""
        self.js_ser.serialize(list(self.products.values()), self.json_file)

    def add(self, data: dict) -> bool:
        """
        Добавляет новый товар в каталог.

        Аргументы:
            data (dict): Словарь с данными нового товара.

        Возвращает:
            bool: True, если товар успешно добавлен. False, если товар с таким ID уже существует.
        """
        if data['product_id'] in self.products: return False
        self.products[data['product_id']] = ProductCard(**data)
        self._save()
        return True

    def update(self, p_id: str, **kwargs) -> bool:
        """
        Обновляет атрибуты существующего товара.

        Аргументы:
            p_id (str): ID товара, который нужно обновить.
            **kwargs: Произвольные именованные аргументы для обновления (например, price=100.0).

        Возвращает:
            bool: True, если товар найден и обновлен. False, если товар не найден.
        """
        if p_id not in self.products: return False
        product = self.products[p_id]
        for key, value in kwargs.items():
            if hasattr(product, key) and value:
                setattr(product, key, value)
        self._save()
        return True

    def remove(self, p_id: str) -> bool:
        """
        Удаляет товар из каталога по его ID.

        Аргументы:
            p_id (str): ID товара для удаления.

        Возвращает:
            bool: True, если товар был удален. False, если товар не найден.
        """
        if p_id in self.products:
            del self.products[p_id]
            self._save()
            return True
        return False

class ConsoleUI:
    """Консольный пользовательский интерфейс для взаимодействия с менеджером каталога."""
    
    def __init__(self, manager: CatalogManager):
        """
        Инициализирует интерфейс.

        Аргументы:
            manager (CatalogManager): Экземпляр менеджера каталога для выполнения операций.
        """
        self.manager = manager
        self.fields = ["index", "product_id", "name", "quantity", "condition", 
                       "supplier", "manufacturer", "price", "location", "city"]

    def run(self):
        """Запускает бесконечный цикл обработки команд пользователя."""
        while True:
            print("\n1.Список 2.Добавить 3.Изменить 4.Удалить 0.Выход")
            cmd = input(">> ")
            if cmd == '1': self.show()
            elif cmd == '2': self.add()
            elif cmd == '3': self.edit()
            elif cmd == '4': self.delete()
            elif cmd == '0': break

    def show(self):
        """Выводит список всех товаров в каталоге."""
        for p in self.manager.products.values(): print(p)

    def add(self):
        """Запускает интерактивный процесс добавления нового товара с вводом данных из консоли."""
        data = {}
        try:
            for field in self.fields:
                data[field] = input(f"{field}: ")
            if self.manager.add(data): print("Успешно!")
            else: print("Ошибка: ID занят.")
        except ValueError: print("Ошибка: проверьте числовые поля.")

    def edit(self):
        """Запускает интерактивный процесс редактирования существующего товара по его ID."""
        p_id = input("ID товара: ")
        print("Введите новые значения (пусто - пропустить):")
        updates = {f: input(f"{f}: ") for f in self.fields if f != 'product_id'}
        if self.manager.update(p_id, **updates): print("Обновлено.")
        else: print("Не найден.")

    def delete(self):
        """Запрашивает ID товара и удаляет его из каталога."""
        if self.manager.remove(input("ID для удаления: ")): print("Удалено.")
        else: print("Не найден.")

if __name__ == "__main__":
    if not os.path.exists('catalog.txt'):
        with open('catalog.txt', 'w', encoding='utf-8') as f:
            f.write("№;ID;Наименование;Количество;Состояние;Поставщик;Производитель;Стоимость;Местоположение;Город\n")
            f.write("1;TEST_ID;Тестовый товар;5;Отличное;Поставщик;Завод;99.9;Полка 1;Питер\n")
        print("Был создан тестовый catalog.txt, так как его не было.")

    manager = CatalogManager()
    print(f"Загружено товаров в память: {len(manager.products)}")
    
    ui = ConsoleUI(manager)
    ui.run()