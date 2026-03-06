from abc import ABC, abstractmethod
from ItemCard import ItemCard

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
    
    def get_format_of_file:
    
    def set_format_of_file:
    

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
