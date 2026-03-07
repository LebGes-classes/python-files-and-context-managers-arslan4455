"""
Главный модуль программы.

Создаёт карточку товара, сохраняет её в JSON файл,
а затем читает список товаров из файла и выводит их на экран.
"""

from ItemCard import ItemCard, run_ui
from Parsers import JSONParser


def main():
    """
    Точка входа программы.

    Создаёт объект ItemCard, сохраняет его в JSON файл
    и выводит все товары из файла.
    """

    item = ItemCard(
        article_number=1001,
        name="Ноутбук",
        quantity=10,
        location="Склад A",
        supplier="ООО Поставщик",
        manufacturer="Lenovo",
        price=75000.0,
        category="Техника",
        subcategory="Ноутбуки"
    )

    print(item)

    parser = JSONParser("products.json")

    parser.serialize_object(item)

    items = parser.deserialize_list()

    for product in items:
        print(product)


if __name__ == "__main__":
    main()
    run_ui()