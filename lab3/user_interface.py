from abc import ABC, abstractmethod


class UserInterface(ABC):
    """Абстрактный интерфейс взаимодействия с пользователем."""

    @abstractmethod
    def get_input(self):
        """Возвращает кортеж (a, b, c)."""
        pass


class ConsoleUserInterface(UserInterface):
    """Реализация через консоль (input)."""

    def get_input(self):
        a = float(input("Введите сторону a: "))
        b = float(input("Введите сторону b: "))
        c = float(input("Введите сторону c: "))
        return a, b, c