from phonebook_bot import AddressBook
from phonebook_bot import Record

contacts = AddressBook()


def input_error(error):
    def wrapper(*args, **kwargs):
        try:
            return error(*args, **kwargs)
        except KeyError:
            return "Name is wrong"
        except IndexError:
            return "Add name and phone number"
        except ValueError as red:
            return red.args[0]

    return wrapper

@input_error
def first_step():
    return "How can I help you?"

@input_error
def add_contacts(data):
    name, *phones = data.strip().split(" ")
    if name in contacts:
        raise ValueError("This name is exist")
    new_record = Record(name)

    for phone in phones:
        new_record.add_phone(phone)

    contacts.add_record(new_record)
    return f"You created {name}:{phones}"

@input_error
def change_phone_funk(data):
    name, *phones = data.strip().split(" ")
    record = contacts[name]
    record.change_phones(phones)
    return "Phone number was changed"

@input_error
def find_phone(key):
    return contacts.search(key.strip()).get_info()

@input_error
def show_all_funk():
    contact = ""
    for name, record in contacts.data.items():
        contact += f"{record.get_info()}\n"
    return contact

@input_error
def quit_funk():
    print("Good bye. See you soon!")
    exit()


@input_error
def del_funk(name):
    name = name.strip()
    contacts.remove_record(name)
    return f"{name} deleted"


@input_error
def del_phone_funk(data):
    name, phone = data.strip().split(" ")

    record = contacts[name]
    if record.delete_phone(phone):
        return f"{phone} deleted"
    return f"{phone} phone number exist "

def func_help():
    print('Commands:')
    print('hello')
    print('add <name> <phone>')
    print('change phone <name> <phone>')
    print('delete <name>')
    print('delete phone <name> <phone>')
    print('find <name>')
    print('show all')
    print('good bye || close || exit')
    return True

COMMANDS = {
    "hello": first_step,
    "add": add_contacts,
    "change phone": change_phone_funk,
    "find": find_phone,
    "show all": show_all_funk,
    "good bye": quit_funk,
    "close": quit_funk,
    "exit": quit_funk,
    "delete phone": del_phone_funk,
    "delete": del_funk,
    'help': func_help
}

def return_func(data):
    return COMMANDS.get(data, error_func)

def error_func():
    return "Wrong command"

def edits(input_data):
    key_part = input_data
    data_part = ""
    for command in COMMANDS:
        if input_data.strip().lower().startswith(command):
            key_part = command
            data_part = input_data[len(key_part):]
            break
    if data_part:
        return return_func(key_part)(data_part)
    else:
        return return_func(key_part)()

def main():
    while True:
        user_input = input("Input your command (start with help): ")
        res = edits(user_input)
        print(res)
        if res == "See you next time":
            break

if __name__ == "__main__":
    main()