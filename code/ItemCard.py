class ItemCard:
    """
    Класс, представляющий карточку товара на складе.

    Хранит информацию о товаре:
    - артикул
    - название
    - количество
    - локацию
    - поставщика
    - производителя
    - цену
    - категорию
    - подкатегорию
    - статус
    """

    def __init__(self, article_number: int, name: str, quantity: int,
                 location: str, supplier: str, manufacturer: str,
                 price: float, category: str, subcategory: str,
                 status: str = "в наличии"):
        """
        Инициализирует новый объект карточки товара.

        Args:
            article_number: артикул товара
            name: название товара
            quantity: количество на складе
            location: место хранения
            supplier: поставщик
            manufacturer: производитель
            price: цена
            category: категория
            subcategory: подкатегория
            status: статус товара
        """

        self.__article_number = article_number
        self.__name = name
        self.__quantity = quantity
        self.__location = location
        self.__supplier = supplier
        self.__manufacturer = manufacturer
        self.__price = price
        self.__category = category
        self.__subcategory = subcategory
        self.__status = status

    # -------- ГЕТТЕРЫ --------

    def get_article_number(self) -> int:
        """Возвращает артикул товара."""
        return self.__article_number

    def get_name(self) -> str:
        """Возвращает название товара."""
        return self.__name

    def get_quantity(self) -> int:
        """Возвращает количество товара."""
        return self.__quantity

    def get_price(self) -> float:
        """Возвращает цену товара."""
        return self.__price

    def get_status(self) -> str:
        """Возвращает статус товара."""
        return self.__status

    def get_location(self) -> str:
        """Возвращает местоположение товара."""
        return self.__location

    def get_supplier(self) -> str:
        """Возвращает поставщика товара."""
        return self.__supplier

    def get_manufacturer(self) -> str:
        """Возвращает производителя товара."""
        return self.__manufacturer

    def get_category(self) -> str:
        """Возвращает категорию товара."""
        return self.__category

    def get_subcategory(self) -> str:
        """Возвращает подкатегорию товара."""
        return self.__subcategory

    # -------- СЕТТЕРЫ --------

    def set_article_number(self, article_number: int):
        """Устанавливает новый артикул товара."""
        if article_number <= 0:
            raise ValueError("Артикул должен быть положительным.")
        self.__article_number = article_number

    def set_name(self, name: str):
        """Устанавливает новое название товара."""
        if not name.strip():
            raise ValueError("Название не может быть пустым.")
        self.__name = name

    def set_quantity(self, quantity: int):
        """Устанавливает новое количество товара."""
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным.")
        self.__quantity = quantity

    def set_price(self, price: float):
        """Устанавливает новую цену товара."""
        if price <= 0:
            raise ValueError("Цена должна быть больше 0.")
        self.__price = price

    def set_location(self, location: str):
        """Устанавливает новую локацию товара."""
        if not location.strip():
            raise ValueError("Локация не может быть пустой.")
        self.__location = location

    def set_supplier(self, supplier: str):
        """Устанавливает нового поставщика."""
        if not supplier.strip():
            raise ValueError("Поставщик не может быть пустым.")
        self.__supplier = supplier

    def set_manufacturer(self, manufacturer: str):
        """Устанавливает нового производителя."""
        if not manufacturer.strip():
            raise ValueError("Производитель не может быть пустым.")
        self.__manufacturer = manufacturer

    def set_category(self, category: str):
        """Устанавливает категорию товара."""
        if not category.strip():
            raise ValueError("Категория не может быть пустой.")
        self.__category = category

    def set_subcategory(self, subcategory: str):
        """Устанавливает подкатегорию товара."""
        if not subcategory.strip():
            raise ValueError("Подкатегория не может быть пустой.")
        self.__subcategory = subcategory

    def set_status(self, status: str):
        """Устанавливает статус товара."""
        if not status.strip():
            raise ValueError("Статус не может быть пустым.")
        self.__status = status

    def write_off(self):
        """
        Списывает товар со склада.

        После списания:
        - количество = 0
        - статус = "списано"
        """

        if self.__status == "списано":
            raise ValueError("Товар уже списан.")

        self.__quantity = 0
        self.__status = "списано"

    def __str__(self):
        """Возвращает строковое представление товара."""
        return (
            f"\n--- КАРТОЧКА ТОВАРА ---\n"
            f"Артикул: {self.__article_number}\n"
            f"Наименование: {self.__name}\n"
            f"Количество: {self.__quantity}\n"
            f"Цена: {self.__price} руб.\n"
            f"Статус: {self.__status}\n"
            f"Локация: {self.__location}\n"
            f"Поставщик: {self.__supplier}\n"
            f"Производитель: {self.__manufacturer}\n"
            f"Категория: {self.__category}\n"
            f"Подкатегория: {self.__subcategory}\n"
            f"-----------------------"
        )

    def set_from_str(self, line: str):
        """
        Заполняет объект из строки.

        Формат строки:
        name:article:quantity:price
        """

        elements = line.split(":")

        self.set_name(elements[0])
        self.set_article_number(int(elements[1]))
        self.set_quantity(int(elements[2]))
        self.set_price(float(elements[3]))

    def set_from_dict(self, data: dict):
        """
        Заполняет объект из словаря.

        Args:
            data: словарь с данными товара
        """

        self.__article_number = data["article_number"]
        self.__name = data["name"]
        self.__quantity = data["quantity"]
        self.__location = data["location"]
        self.__supplier = data["supplier"]
        self.__manufacturer = data["manufacturer"]
        self.__price = data["price"]
        self.__category = data["category"]
        self.__subcategory = data["subcategory"]
        self.__status = data["status"]

    def to_dict(self) -> dict:
        """
        Преобразует объект товара в словарь.

        Returns:
            dict: словарь со всеми данными товара
        """

        return {
            "article_number": self.__article_number,
            "name": self.__name,
            "quantity": self.__quantity,
            "location": self.__location,
            "supplier": self.__supplier,
            "manufacturer": self.__manufacturer,
            "price": self.__price,
            "category": self.__category,
            "subcategory": self.__subcategory,
            "status": self.__status
        }

def run_ui():
    """Запускает консольный интерфейс управления карточкой товара."""

    print("Добро пожаловать в систему складского учета!")

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

    is_running = True
    while is_running:
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

        choice = input("\nВыберите действие: ")

        
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

            else:
                print("Неверный ввод. Попробуйте снова.")

        except ValueError:
            print("Ошибка: введены некорректные данные (тип числа).")