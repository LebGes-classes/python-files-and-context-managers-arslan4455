from abc import ABC, abstractmethod
from ItemCard import ItemCard
import json

class BaseSerializer(ABC):
    @abstractmethod
    def serialize_object(self, obj):
        pass

class BaseDeserializer(ABC):
    @abstractmethod
    def deserialize_object(self, obj):
        pass

class FileInfo:
    __format_of_file = None

    def __init__(self, filename):
        self.__filename = filename

    def get_file_name(self):
        return self.__filename
    
    def set_file_name(self, filename):
        self.__filename = filename
    
    def set_format_of_file(self, format_of_file):
        self.__format_of_file = format_of_file

    def get_format_of_file(self):

        return self.__format_of_file
    
    

class TextParser(FileInfo, BaseDeserializer):

    __format_of_file = '.txt'

    def deserialize_object(self):
        products = []

        with open (self.__filename, 'r', encoding='utf-8') as fos:
            lines = fos.readlines()
            lines = lines.remove(0)

        for line in lines:
            product = Product().set_from_str(line.strip())

            products.append(product)


class JSONParser(FileInfo, BaseDeserializer):

    __format_of_file = '.json'

    def serialize_list

    def serialize_object(self, item_card: ItemCard) -> None:

        data_list = self.deserialize_list()
        new_data_list = list()

        if item_card not in data_list:
            data_list.append(product)
        else:
            for data in data_list:
                if data.get_id() == item_card.get_id():
                    new_data_list.append(item_card)
                else:
                    new_data_list.append(data)

        self.serialize_list(new_data_list)


    def deserialize_list(self, ids: list[str] = None) -> list[ItemCard]:
        item_cards = []

        with open(self.get_full_file_name(), 'r') as fos:
            data_dict = json.load(fos)

        if ids:
            for current_id in ids:
                item_card = ItemCard()
                item_card.set_from_dict(data_dict[current_id])

                item_cards.append(item_card)
        else:
            for data in data_dict:
                item_card = ItemCard()
                item_card.set_from_dict(data)

                item_cards.append(item_card)

        return item_cards
        