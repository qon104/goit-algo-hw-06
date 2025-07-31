import re
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Ім'я повинно бути непорожнім рядком")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Телефон повинен містити рівно 10 цифр")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_str):
        phone = Phone(phone_str)
        self.phones.append(phone)

    def remove_phone(self, phone_str):
        self.phones = [phone for phone in self.phones if phone.value != phone_str]

    def edit_phone(self, old_phone_str, new_phone_str):
        new_phone = Phone(new_phone_str)
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone_str:
                self.phones[i] = new_phone
                return

    def find_phone(self, phone_str):
        for phone in self.phones:
            if phone.value == phone_str:
                return phone
        return None

    def __str__(self):
        phones_str = "; ".join(phone.value for phone in self.phones)
        return f"Ім'я контакту: {self.name.value}, телефони: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        if not self.data:
            return "Адресна книга порожня"
        return "\n".join(str(record) for record in self.data.values())


def input_name():
    while True:
        name = input("Введіть ім'я контакту: ").strip()
        try:
            valid_name = Name(name)
            return valid_name.value
        except ValueError as e:
            print(f"Помилка: {e}. Спробуйте ще раз.")

def input_phone():
    while True:
        phone = input("Введіть номер телефону (10 цифр): ").strip()
        try:
            valid_phone = Phone(phone)
            return valid_phone.value
        except ValueError as e:
            print(f"Помилка: {e}. Спробуйте ще раз.")

# Приклад використання:
if __name__ == "__main__":
    book = AddressBook()

    # Вводимо ім'я та телефони з перевіркою
    name = input_name()
    record = Record(name)

    while True:
        phone = input_phone()
        record.add_phone(phone)

        more = input("Додати ще один телефон? (так/ні): ").strip().lower()
        if more != "так":
            break

    book.add_record(record)

    print("\nПоточна адресна книга:")
    print(book)
