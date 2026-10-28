import unittest
from unittest.mock import MagicMock, patch
from calculator import TriangleCalculator
from database import TriangleDatabase
from user_interface import ConsoleUserInterface
from external_service import EmailService
from controller import Controller


class TestTriangleCalculator(unittest.TestCase):
    """Юнит-тесты калькулятора."""

    def setUp(self):
        self.calc = TriangleCalculator()

    def test_equilateral(self):
        t, e = self.calc.calculate(3, 3, 3)
        self.assertEqual(t, "равносторонний")
        self.assertIsNone(e)

    def test_invalid_triangle(self):
        t, e = self.calc.calculate(1, 2, 10)
        self.assertIsNone(t)
        self.assertEqual(e, "Треугольник не существует")

    def test_negative_side(self):
        t, e = self.calc.calculate(-1, 2, 2)
        self.assertIsNone(t)
        self.assertEqual(e, "Стороны должны быть положительными")


class TestDatabase(unittest.TestCase):
    """Юнит-тесты БД."""

    def setUp(self):
        self.db = TriangleDatabase()

    def tearDown(self):
        self.db.close()

    def test_add_and_get(self):
        self.db.add(3, 4, 5, "разносторонний", None)
        result = self.db.get(3, 4, 5)
        self.assertEqual(result, ("разносторонний", None))

    def test_get_missing(self):
        self.assertIsNone(self.db.get(9, 9, 9))

    def test_delete(self):
        self.db.add(3, 4, 5, "разносторонний", None)
        self.db.delete(3, 4, 5)
        self.assertIsNone(self.db.get(3, 4, 5))


class TestIntegrationController(unittest.TestCase):
    """Интеграционные тесты (с реальными объектами + заглушки для ввода/внешнего сервиса)."""

    def setUp(self):
        self.db = TriangleDatabase()
        self.calc = TriangleCalculator()
        self.external = EmailService()

    def tearDown(self):
        self.db.close()

    @patch("builtins.input", side_effect=["3", "3", "3"])
    def test_full_scenario_equilateral(self, mock_input):
        """Интеграция: UI -> Controller -> Calculator -> DB -> ExternalService."""
        ui = ConsoleUserInterface()
        controller = Controller(self.calc, self.db, ui, self.external)

        result = controller.run()

        self.assertEqual(result, "Тип треугольника: равносторонний")
        # проверяем, что запись появилась в БД
        self.assertEqual(self.db.get(3, 3, 3), ("равносторонний", None))

    @patch("builtins.input", side_effect=["1", "2", "10"])
    def test_full_scenario_invalid(self, mock_input):
        """Интеграция: ошибка проходит через все слои и пишется в БД."""
        ui = ConsoleUserInterface()
        controller = Controller(self.calc, self.db, ui, self.external)

        result = controller.run()

        self.assertEqual(result, "Ошибка: Треугольник не существует")
        self.assertEqual(
            self.db.get(1, 2, 10), (None, "Треугольник не существует")
        )

    @patch("builtins.input", side_effect=["3", "3", "3", "3", "3", "3"])
    def test_uses_cache_on_second_run(self, mock_input):
        """Интеграция: второй вызов берёт результат из БД (калькулятор не вызывается)."""
        ui = ConsoleUserInterface()
        controller = Controller(self.calc, self.db, ui, self.external)

        # первый запуск — считает и пишет в БД
        controller.run()

        # второй запуск — должен взять из БД
        with patch.object(self.calc, "calculate") as mock_calc:
            result = controller.run()
            mock_calc.assert_not_called()

        self.assertEqual(result, "Тип треугольника: равносторонний")

    @patch("builtins.input", side_effect=["5", "5", "6"])
    def test_external_service_called(self, mock_input):
        """Интеграция: проверяем, что результат уходит во внешний сервис (заглушка)."""
        ui = ConsoleUserInterface()
        external_mock = MagicMock()
        controller = Controller(self.calc, self.db, ui, external_mock)

        controller.run()

        external_mock.send.assert_called_once_with(
            "Тип треугольника: равнобедренный"
        )