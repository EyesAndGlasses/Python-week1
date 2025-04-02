from datetime import datetime


class TimestampMeta(type):
    def __new__(cls, name, bases, class_dict):
        class_dict["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, class_dict)


class MyClass(metaclass=TimestampMeta):
    pass


class AnotherClass(metaclass=TimestampMeta):
    pass


print(MyClass.created_at)  # Дата и время создания класса MyClass
print(AnotherClass.created_at)  # Дата и время создания класса AnotherClass
