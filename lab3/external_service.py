from abc import ABC, abstractmethod


class ExternalService(ABC):
    """Абстрактный интерфейс сторонней зависимости."""

    @abstractmethod
    def send(self, message):
        """Имитация отправки данных."""
        pass


class EmailService(ExternalService):
    """Имитация отправки на email-сервер."""

    def send(self, message):
        # имитация: реальной отправки нет
        print(f"[EMAIL] Отправлено: {message}")
        return True