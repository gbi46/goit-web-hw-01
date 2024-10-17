from lib import AddressBook, ConsoleView, Record
from functools import wraps
import pickle, pathlib

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Index of arguments is out of range"
        except KeyError:
            return "The name does not exists!"
        except ValueError:
            return "Enter correct number of arguments, please: name and phone."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split() 
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)

    if not record:
        message = "Contact not found."
    else:
        record.add_birthday(birthday)
        message = "Birthday added."

    return message

@input_error
def add_contact(args, book):
    name, phone, *_ = args

    record = book.find(name)
    message = "Contact updated"

    if record is None: 
        record = Record(name)
        message = "Contact added"
        
    record.add_phone(phone)
    book.add_record(record)
    
    return message

@input_error
def change_phone(args, book):
    name, old_phone, new_phone = args

    contact = book.find(name)
    contact.edit_phone(old_phone, new_phone)

    return "Contact updated."

def show_all(book):
    return book.show_all_contacts()

@input_error
def show_all_birthdays(book):
    return book.get_upcoming_birthdays()

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise IndexError("Index of arguments is out of range")
    contact_name = ''.join(args)
    record = book.find(contact_name)

    return record.show_birthday()

def show_help(args, view):
    if len(args) != 0:
        raise IndexError("Index of arguments is out of range")
    
    return view.show_help(view.commands)

@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise IndexError("Index of arguments is out of range")
    username = ''.join(args)
    contact = book.find(username)

    return contact.show_all_phones()

@input_error
def shutdown(args):
    if len(args) != 0:
        raise IndexError("Index of arguments is out of range")
    
    return "Goodbye!"

def save_data(book, filename="addressbook.pkl"):

    curr_dir = pathlib.Path(__file__).parent
    filename = curr_dir / filename
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):

    curr_dir = pathlib.Path(__file__).parent
    filename = curr_dir / filename

    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook(ConsoleView)
    
def main():
    print("Welcome to the assistent bot!")

    book = load_data()
    view = ConsoleView()

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            print(shutdown(args))
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            print(show_help(args, view))
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == 'phone':
            print(show_phone(args, book))
        elif command == 'all':
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(show_all_birthdays(book))
        else:
            print("Invalid command!")

    save_data(book)

if __name__ == "__main__":
    main()
