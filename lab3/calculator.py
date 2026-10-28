class TriangleCalculator:
    """Класс вычислений / валидации (из ЛР №1)."""

    def calculate(self, a, b, c):
        """Возвращает (тип_треугольника, сообщение_об_ошибке)."""
        # проверка на положительность
        if a <= 0 or b <= 0 or c <= 0:
            return None, "Стороны должны быть положительными"

        # проверка неравенства треугольника
        if a + b <= c or a + c <= b or b + c <= a:
            return None, "Треугольник не существует"

        # определение типа
        sides = sorted([a, b, c])
        if sides[0] == sides[1] == sides[2]:
            return "равносторонний", None
        elif sides[0] == sides[1] or sides[1] == sides[2]:
            return "равнобедренный", None
        else:
            return "разносторонний", None