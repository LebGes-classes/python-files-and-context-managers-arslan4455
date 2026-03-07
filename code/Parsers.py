"""
Модуль сериализации и десериализации данных товаров.

Содержит абстрактные классы для парсеров
и реализации для TXT и JSON файлов.
"""

from abc import ABC, abstractmethod
from ItemCard import ItemCard
import json
import os


class BaseSerializer(ABC):
    """
    Абстрактный базовый класс для сериализации объектов.
    """

    @abstractmethod
    def serialize_object(self, obj):
        """Сохраняет объект в файл."""
        pass


class BaseDeserializer(ABC):
    """
    Абстрактный базовый класс для десериализации объектов.
    """

    @abstractmethod
    def deserialize_object(self):
        """Читает объект из файла."""
        pass


class FileInfo:
    """
    Класс для хранения информации о файле.
    """

    def __init__(self, filename):
        """
        Args:
            filename: имя файла
        """
        self.__filename = filename

    def get_file_name(self):
        """Возвращает имя файла."""
        return self.__filename

    def set_file_name(self, filename):
        """Устанавливает новое имя файла."""
        self.__filename = filename


class TextParser(FileInfo, BaseDeserializer):
    """
    Парсер текстового файла (.txt).
    """

    def deserialize_object(self):
        """
        Читает товары из текстового файла.

        Returns:
            list[ItemCard]: список товаров
        """

        products = []

        with open(self.get_file_name(), 'r', encoding='utf-8') as fos:
            lines = fos.readlines()

        for line in lines:
            item = ItemCard(0, "", 0, "", "", "", 1.0, "", "")
            item.set_from_str(line.strip())

            products.append(item)

        return products


class JSONParser(FileInfo, BaseSerializer):
    """
    Парсер JSON файлов для хранения карточек товаров.
    """

    def serialize_list(self, item_cards):
        """
        Сохраняет список товаров в JSON файл.

        Args:
            item_cards: список объектов ItemCard
        """

        data = [item.to_dict() for item in item_cards]

        with open(self.get_file_name(), "w", encoding="utf-8") as fos:
            json.dump(data, fos, indent=4, ensure_ascii=False)

    def serialize_object(self, item_card: ItemCard):
        """
        Сохраняет один объект товара в JSON файл.

        Если товар с таким артикулом уже существует —
        он будет обновлён.

        Args:
            item_card: объект ItemCard
        """

        data_list = []

        if os.path.exists(self.get_file_name()):
            data_list = self.deserialize_list()

        found = False

        for i, item in enumerate(data_list):
            if item.get_article_number() == item_card.get_article_number():
                data_list[i] = item_card
                found = True

        if not found:
            data_list.append(item_card)

        self.serialize_list(data_list)

    def deserialize_list(self):
        """
        Читает список товаров из JSON файла.

        Returns:
            list[ItemCard]: список карточек товаров
        """

        item_cards = []

        if not os.path.exists(self.get_file_name()):
            return item_cards

        with open(self.get_file_name(), 'r', encoding='utf-8') as fos:
            data_list = json.load(fos)

        for data in data_list:
            item = ItemCard(0, "", 0, "", "", "", 1.0, "", "")
            item.set_from_dict(data)

            item_cards.append(item)

        return item_cards
    def load_or_create(self) -> list:

        try:
            return self.deserialize_list()
        except FileNotFoundError:
            return []