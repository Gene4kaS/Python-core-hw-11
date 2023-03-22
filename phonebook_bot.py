from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not all((value.startswith('+'), len(value) == 13, value[1:].isdigit())):
            raise ValueError("Введіть номер в форматі '+380111111111'")
        self.__value = value


class Record:
    def __init__(self, name, phone, birthday):
        self.name = Name(name)

        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = ''

        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []

    def get_info(self):
        for phon in self.phones:
            phon_info = "".join(f"{phon.value}")
        return f"{self.name.value} : {phon_info}"

    def add_phone(self, phon):
        self.phones.append(Phone(phon))

    def change_phones(self, phones):
        for phone in phones:
            if not self.delete_phone(phone):
                self.add_phone(phone)

    def delete_phone(self, phone):
        for record_phone in self.phones:
            if record_phone.value == phone:
                self.phones.remove(record_phone)
                return True
        return False

    def days_to_birthday(self):
        date_now = datetime.now()
        try:
            date_birthday = datetime(year=date_now.year, month=self.month, day=self.day)
        except:
            date_birthday = datetime(year=date_now.year, month=self.month, day=self.day - 1)

        if date_birthday < date_now:
            try:
                date_birthday = datetime(year=date_now.year + 1, month=self.month, day=self.day)
            except:
                date_birthday = datetime(year=date_now.year + 1, month=self.month, day=self.day - 1)

        return (date_birthday - date_now).days

class Birthday(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return datetime.strftime(self.__value, '%d.%m.%Y')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            date_birthday = datetime.strptime(value, '%d.%m.%Y')
            self.__value = date_birthday
        except:
            raise ValueError("Введіть день народження в форматі 'дд.мм.ггг' (наприклад 01.01.1990)")

class AddressBook(UserDict):
    N = 10
    current_index = 0

    def iterator(self):
        names = sorted([name for name in self.data])
        while AddressBook.current_index < len(self.data):
            text_records = ''
            for name in names[AddressBook.current_index:min(len(self.data), AddressBook.current_index + AddressBook.N)]:
                record = self.data[name]
                record_name = record.name.value
                record_birthday = str(record.birthday)
                for phone in record.phones:
                    text_records += '{:<20}{:>20}{:>20}\n'.format(record_name, phone.value, record_birthday)
                    record_name = ''
                    record_birthday = ''
                if record_name:
                    text_records += '{:<20}{:>20}{:>20}\n'.format(record_name, '', record_birthday)

            yield text_records
            AddressBook.current_index += AddressBook.N

    def add_record(self, record):
        self.data[record.name.value] = record

    def has_record(self, name):
        for name in self.data:
            return bool(self.data.get(name))

    def remove_record(self, name):
       del self.data[name]

    def search(self, value):
        if self.has_record(value):
            return self.data.get(value)

        for record in self.data.values():
            for phone in record.phones:
                if phone.value == value:
                    return record
        raise ValueError("Error")