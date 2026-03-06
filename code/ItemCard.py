class ItemCard:
    """
    Класс, представляющий карточку товара на складе.

    Хранит информацию о товаре:
    артикул, название, количество, локацию, поставщика,
    производителя, цену, категорию, подкатегорию и статус.
    """

    def __init__(self, article_number: int, name: str, quantity: int,
                 location: str, supplier: str, manufacturer: str,
                 price: float, category: str, subcategory: str,
                 status: str = "в наличии"):
        """
        Инициализирует новый объект карточки товара.
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
        """Устанавливает новый артикул."""
        try:
            if article_number <= 0:
                raise ValueError("Артикул должен быть положительным.")
            self.__article_number = article_number
            print("Артикул обновлён.")
        except ValueError as e:
            print("Ошибка:", e)


    def set_name(self, name: str):
        """Устанавливает новое название."""
        try:
            if not name.strip():
                raise ValueError("Название не может быть пустым.")
            self.__name = name
            print("Название обновлено.")
        except ValueError as e:
            print("Ошибка:", e)


    def set_quantity(self, quantity: int):
        """Устанавливает новое количество."""
        try:
            if quantity < 0:
                raise ValueError("Количество не может быть отрицательным.")
            self.__quantity = quantity
            print("Количество обновлено.")
        except ValueError as e:
            print("Ошибка:", e)


    def set_price(self, price: float):
        """Устанавливает новую цену."""
        try:
            if price <= 0:
                raise ValueError("Цена должна быть больше 0.")
            self.__price = price
            print("Цена обновлена.")
        except ValueError as e:
            print("Ошибка:", e)


    def set_location(self, location: str):
        """Устанавливает новую локацию."""
        try:
            if not location.strip():
                raise ValueError("Локация не может быть пустой.")
            self.__location = location
            print("Локация обновлена.")
        except ValueError as e:
            print("Ошибка:", e)


    def set_supplier(self, supplier: str):
        """Устанавливает нового поставщика."""
        try:
            if not supplier.strip():
                raise ValueError("Поставщик не может быть пустым.")
            self.__supplier = supplier
            print("Поставщик обновлён.")
        except ValueError as e:
            print("Ошибка:", e)


    def set_manufacturer(self, manufacturer: str):
        """Устанавливает нового производителя."""
        try:
            if not manufacturer.strip():
                raise ValueError("Производитель не может быть пустым.")
            self.__manufacturer = manufacturer
            print("Производитель обновлён.")
        except ValueError as e:
            print("Ошибка:", e)


    def set_category(self, category: str):
        """Устанавливает новую категорию."""
        try:
            if not category.strip():
                raise ValueError("Категория не может быть пустой.")
            self.__category = category
            print("Категория обновлена.")
        except ValueError as e:
            print("Ошибка:", e)


    def set_subcategory(self, subcategory: str):
        """Устанавливает новую подкатегорию."""
        try:
            if not subcategory.strip():
                raise ValueError("Подкатегория не может быть пустой.")
            self.__subcategory = subcategory
            print("Подкатегория обновлена.")
        except ValueError as e:
            print("Ошибка:", e)


    def set_status(self, status: str):
        """Устанавливает новый статус."""
        try:
            if not status.strip():
                raise ValueError("Статус не может быть пустым.")
            self.__status = status
            print("Статус обновлён.")
        except ValueError as e:
            print("Ошибка:", e)


    def write_off(self):
        """
        Списывает товар со склада.
        Количество становится 0, статус — 'списано'.
        """
        try:
            if self.__status == "списано":
                raise ValueError("Товар уже списан.")

            self.__quantity = 0
            self.__status = "списано"
            print("Товар успешно списан.")

        except ValueError as e:
            print("Ошибка:", e)

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
    
    def from_str(self, line: str) -> None:
        elements = line.strip(':')

        self.set_article_number(elements[1])
        self.set_name(elements[0])