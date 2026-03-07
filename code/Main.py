from ItemCard import ItemCard
from Parsers import JSONParser


def main():
    
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

    for i in items:
        print(i)


if __name__ == "__main__":
    main()