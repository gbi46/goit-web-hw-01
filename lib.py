from abc import ABC, abstractmethod
from collections import UserDict
from datetime import date, datetime, timedelta

class View(ABC):
    @abstractmethod
    def show_contacts(self, contacts):
        pass
    
    @abstractmethod
    def show_help(self, commands):
        pass

class ConsoleView(View):
    def __init__(self):
        super().__init__()
        self.commands = {
            "add [name] [phone]": "Add a new contact",
            "birthdays" : "Show all upcoming birthdays",
            "add-birthday [name]" : "Add contact's birthday",
            "all": "Show all contacts",
            "change [name] [old_phone] [new_phone]" : "Change phone number",
            "phone [name]" : "Show contact phones",
            "hello" : "Hello message",
            "help": "Show this help message",
            "show-birthday [name]" : "Show contact's birthday"
        }

    def show_contacts(self, contacts):

        if not contacts:
            message = "No contacts available"
        else:
            message = "Contacts cards:\n\n"
            for contact in contacts.values():
                message = message + str(contact) + "\n"

        return message
    
    def show_help(self, commands):
        message = "\nAvailable commands:\n\n"

        for command, description in commands.items():
            message = message + f"{command}: {description}\n"

        return message

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
            raise ValueError("Phone format is not correct")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday
    
    def date_to_string(self, date):
        return date.strftime("%d.%m.%Y")
    
    def find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        days_ahead += 7
        
        return start_date + timedelta(days=days_ahead)

    def string_to_date(self, str):
        return datetime.strptime(str, "%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for i, p in enumerate(self.phones):
            if p.value == phone:
                del self.phones[i]
                return
        raise ValueError("Phone was not found")
    
    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
            return
        raise ValueError("Phone was not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def show_all_phones(self):
        return ';'.join(p.value for p in self.phones)

    def show_birthday(self):
        return self.birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {self.show_all_phones()}, birthday: {self.show_birthday()}"

class AddressBook(UserDict):
    def __init__(self, view: View):
        super().__init__()
        self.view = view

    def add_record(self, record):
        self.data[record.name.value] = record

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for contact in self.data:
            record = self.find(contact)
            birthday_obj = record.show_birthday()

            if not birthday_obj == None:
                birthday = birthday_obj.string_to_date(birthday_obj.value)
                
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year.date() < today:
                    birthday_this_year = birthday.replace(year = today.year+1)
                
                if 0 <= (birthday_this_year.date() - today).days <= days:
                    birthday_this_year = birthday_obj.adjust_for_weekend(birthday_this_year)
                    
                    congratulation_date_str = birthday_obj.date_to_string(birthday_this_year)
                    
                    upcoming_birthdays.append({"name": contact, "congratulation_date": congratulation_date_str})

        return upcoming_birthdays

    def delete(self, name):
        del self.data[name]

    def find(self, name):
        return self.data.get(name)
    
    def show_all_contacts(self):
        return self.view.show_contacts(self, self.data)
    
    def __str__(self):
        result = ""
        for name, record in self.items():
            result += str(record) + "\n"
        return result
