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

def print_menu():
    """Выводит меню управления товаром."""
    print("\n====== МЕНЮ УПРАВЛЕНИЯ ======")
    print("1. Показать информацию о товаре")
    print("2. Изменить артикул")
    print("3. Изменить название")
    print("4. Изменить количество")
    print("5. Изменить цену")
    print("6. Изменить локацию")
    print("7. Изменить поставщика")
    print("8. Изменить производителя")
    print("9. Изменить категорию")
    print("10. Изменить подкатегорию")
    print("11. Изменить статус")
    print("12. Списать товар")
    print("0. Выход")


def run_ui():
    """
    Консольный интерфейс управления складом.

    Загружает товар из JSON файла и сохраняет изменения.
    """

    parser = JSONParser("products.json")

    items = parser.load_or_create()

    if items:
        item = items[0]
    else:
        item = ItemCard(
            1001,
            "Ноутбук",
            5,
            "Секция 1",
            "Asus Store",
            "Asus",
            75000.0,
            "Техника",
            "Ноутбуки"
        )
        parser.serialize_object(item)

    print("Добро пожаловать в систему складского учета!")

    is_running = True

    while is_running:

        print_menu()

        choice = input("Выберите действие: ")

        try:

            if choice == "1":
                print(item)

            elif choice == "2":
                new_article = int(input("Введите новый артикул: "))
                item.set_article_number(new_article)

            elif choice == "3":
                new_name = input("Введите новое название: ")
                item.set_name(new_name)

            elif choice == "4":
                new_qty = int(input("Введите новое количество: "))
                item.set_quantity(new_qty)

            elif choice == "5":
                new_price = float(input("Введите новую цену: "))
                item.set_price(new_price)

            elif choice == "6":
                new_location = input("Введите новую локацию: ")
                item.set_location(new_location)

            elif choice == "7":
                new_supplier = input("Введите нового поставщика: ")
                item.set_supplier(new_supplier)

            elif choice == "8":
                new_manufacturer = input("Введите нового производителя: ")
                item.set_manufacturer(new_manufacturer)

            elif choice == "9":
                new_category = input("Введите новую категорию: ")
                item.set_category(new_category)

            elif choice == "10":
                new_subcategory = input("Введите новую подкатегорию: ")
                item.set_subcategory(new_subcategory)

            elif choice == "11":
                new_status = input("Введите новый статус: ")
                item.set_status(new_status)

            elif choice == "12":
                confirm = input("Вы уверены, что хотите списать товар? (y/n): ")

                if confirm.lower() == "y":
                    item.write_off()

            elif choice == "0":
                print("Завершение работы...")
                is_running = False
                continue

            else:
                print("Неверный ввод.")
                continue

            # сохраняем изменения
            parser.serialize_object(item)

        except ValueError:
            print("Ошибка: введены некорректные данные.")

if __name__ == "__main__":
    main()
    run_ui()