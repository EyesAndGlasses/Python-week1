from src.module1_task2.singleton import singleton_instance

print(singleton_instance.value)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value


class SingletonByNew:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value


# Проверка:
a = Singleton(10)
b = Singleton(20)
print(a is b)  # True
print(a.value)  # 10 (b ссылается на тот же объект)

# Проверка:
a = SingletonByNew(10)
b = SingletonByNew(20)
print(a is b)  # True
print(a.value)  # 20 (инициализатор перезаписывает значение)
