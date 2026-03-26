from CatalogManager import CatalogManager


class ConsoleUI:
    """Консольный пользовательский интерфейс."""
    def __init__(self, manager: CatalogManager):
        self.manager = manager
        self.fields = ["index", "product_id", "name", "quantity", "condition", 
                       "supplier", "manufacturer", "price", "location", "city"]

    def run(self):
        while True:
            print("\n1.Список 2.Добавить 3.Изменить 4.Удалить 0.Выход")
            cmd = input(">> ")
            if cmd == '1': self.show()
            elif cmd == '2': self.add()
            elif cmd == '3': self.edit()
            elif cmd == '4': self.delete()
            elif cmd == '0': break

    def show(self):
        for p in self.manager.products.values(): print(p)

    def add(self):
        data = {}
        try:
            for field in self.fields:
                data[field] = input(f"{field}: ")
            if self.manager.add(data): print("Успешно!")
            else: print("Ошибка: ID занят.")
        except ValueError: print("Ошибка: проверьте числовые поля.")

    def edit(self):
        p_id = input("ID товара: ")
        print("Введите новые значения (пусто - пропустить):")
        updates = {f: input(f"{f}: ") for f in self.fields if f != 'product_id'}
        if self.manager.update(p_id, **updates): print("Обновлено.")
        else: print("Не найден.")

    def delete(self):
        if self.manager.remove(input("ID для удаления: ")): print("Удалено.")
        else: print("Не найден.")