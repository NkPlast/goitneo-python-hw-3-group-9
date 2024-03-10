from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        self.value = self.validate(value)
    
    def validate(self, value):
        try:
            return datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Birthday must be in DD.MM.YYYY format")

class Record:
    def __init__(self, name, phones=[], birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = ', '.join([str(phone) for phone in self.phones])
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "Not provided"
        return f"Name: {self.name}, Phones: {phones_str}, Birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.now().date()
        next_week = [today + timedelta(days=i) for i in range(7)]
        birthdays_this_week = {}
        for record in self.data.values():
            if record.birthday and record.birthday.value.date().replace(year=today.year) in next_week:
                day = record.birthday.value.strftime("%A")
                if day not in birthdays_this_week:
                    birthdays_this_week[day] = []
                birthdays_this_week[day].append(record.name.value)
        return birthdays_this_week

# Пример использования
book = AddressBook()
john_record = Record("John", ["1234567890"], "15.03.1984")
book.add_record(john_record)
birthdays_next_week = book.get_birthdays_per_week()
for day, names in birthdays_next_week.items():
    print(f"{day}: {', '.join(names)}")
