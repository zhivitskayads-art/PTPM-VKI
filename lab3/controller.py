class Controller:
    """Бизнес-логика сквозного сценария."""

    def __init__(self, calculator, database, user_interface, external_service):
        self.calculator = calculator
        self.database = database
        self.user_interface = user_interface
        self.external_service = external_service

    def run(self):
        # 1. получить данные от пользователя
        a, b, c = self.user_interface.get_input()

        # 2. проверить БД
        cached = self.database.get(a, b, c)
        if cached is not None:
            triangle_type, error_message = cached
        else:
            triangle_type, error_message = self.calculator.calculate(a, b, c)
            self.database.add(a, b, c, triangle_type, error_message)

        # 3. сформировать строку-результат
        if error_message:
            result = f"Ошибка: {error_message}"
        else:
            result = f"Тип треугольника: {triangle_type}"

        # 4. отправить сторонней зависимости
        self.external_service.send(result)

        # 5. вернуть результат
        return result