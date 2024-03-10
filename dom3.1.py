from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

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

def main():
    book = AddressBook()
    while True:
        command = input("Enter command: ").strip().lower()
        if command == "exit" or command == "close":
            print("Goodbye!")
            break
        elif command.startswith("add "):
            _, name, phone = command.split()
            record = Record(name, [phone])
            book.add_record(record)
            print(f"Contact {name} added.")
        elif command.startswith("change "):
            _, name, phone = command.split()
            if book.find(name):
                book.find(name).edit_phone(book.find(name).phones[0].value, phone)
                print(f"Contact {name}'s phone changed.")
            else:
                print("Contact not found.")
        elif command.startswith("phone "):
            _, name = command.split()
            if book.find(name):
                print(f"{name}'s phone: {book.find(name).phones[0]}")
            else:
                print("Contact not found.")
        elif command == "all":
            for name, record in book.items():
                print(record)
        elif command.startswith("add-birthday "):
            _, name, birthday = command.split()
            if book.find(name):
                book.find(name).add_birthday(birthday)
                print(f"{name}'s birthday added.")
            else:
                print("Contact not found.")
        elif command.startswith("show-birthday "):
            _, name = command.split()
            if book.find(name) and book.find(name).birthday:
                print(f"{name}'s birthday: {book.find(name).birthday}")
            else:
                print("Birthday not found.")
        elif command == "birthdays":
            birthdays = book.get_birthdays_per_week()
            if birthdays:
                for day, names in birthdays.items():
                    print(f"{day}: {', '.join(names)}")
            else:
                print("No birthdays next week.")
        elif command == "hello":
            print("Hello! How can I help you?")
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
