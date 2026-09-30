"""
Юнит-тесты для src/delivery_service.py (модуль доставки).
Запуск: python -m unittest tests.test_delivery -v

ВАЖНО: часть тестов СПЕЦИАЛЬНО падает — в модуле есть баги,
которые нужно локализовать в отчёте (пункты Б и В).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.delivery_service import calculate_delivery_cost


class TestDeliveryValidation(unittest.TestCase):
    """Группа 1. Валидация входных данных."""

    def test_weight_below_minimum_returns_error(self):
        """Вес < 0.1 -> -1, '0000-00-00'."""
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_maximum_returns_error(self):
        """Вес > 50 -> -1, '0000-00-00'."""
        cost, date = calculate_delivery_cost(51.0, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_below_minimum_returns_error(self):
        """Дистанция < 1 -> -1, '0000-00-00'."""
        cost, date = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_above_maximum_returns_error(self):
        """Дистанция > 5000 -> -1, '0000-00-00'."""
        cost, date = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_package_type_returns_error(self):
        """Неизвестный тип посылки -> -1, '0000-00-00'."""
        cost, date = calculate_delivery_cost(1.0, 100, "магический")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_at_minimum_boundary(self):
        """Вес ровно 0.1 -> валиден."""
        cost, _ = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertGreater(cost, 0)

    def test_weight_at_maximum_boundary(self):
        """Вес ровно 50.0 -> валиден."""
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertGreater(cost, 0)

    def test_distance_at_minimum_boundary(self):
        """Дистанция ровно 1 -> валидна."""
        cost, _ = calculate_delivery_cost(1.0, 1, "обычный")
        self.assertGreater(cost, 0)

    def test_distance_at_maximum_boundary(self):
        """Дистанция ровно 5000 -> валидна."""
        cost, _ = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertGreater(cost, 0)


class TestDeliveryCost(unittest.TestCase):
    """Группа 2. Расчёт стоимости."""

    def test_base_cost_formula(self):
        """Базовая: 200 + 5 * distance (при весе <= 5)."""
        # weight=1, distance=100: 200 + 500 = 700
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_medium_coefficient(self):
        """Вес 6..19 -> множитель 1.2."""
        # weight=10, distance=100: (200 + 500) * 1.2 = 840
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_heavy_coefficient(self):
        """Вес >= 20 -> множитель 1.5."""
        # weight=25, distance=100: (200 + 500) * 1.5 = 1050
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_weight_boundary_at_5(self):
        """Вес ровно 5.0 — не попадает ни в 1.2, ни в 1.5."""
        # weight=5, distance=100: 700 (без множителя)
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_boundary_at_20(self):
        """Вес ровно 20.0 — должен быть множитель 1.5."""
        # weight=20, distance=100: (200+500)*1.5 = 1050
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_fragile_surcharge(self):
        """Хрупкий +300."""
        # weight=1, distance=100: 700 + 300 = 1000
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_surcharge(self):
        """Опасный +1000."""
        # weight=1, distance=100: 700 + 1000 = 1700
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_normal_package_no_surcharge(self):
        """Обычный без наценки."""
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_express_makes_delivery_more_expensive(self):
        """🚨 ЭКСПРЕСС ДОЛЖЕН УДОРОЖАТЬ доставку, а не удешевлять.

        Ожидаем: экспресс = обычная стоимость * 1.5 (или хотя бы > обычной).
        В модуле сейчас стоит '*= 0.5' -> ТЕСТ ПАДАЕТ (обнаружен БАГ).
        """
        cost_normal, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=False)
        cost_express, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertGreater(
            cost_express, cost_normal,
            f"Экспресс ({cost_express}) должен быть дороже обычной доставки ({cost_normal})"
        )


class TestDeliveryDate(unittest.TestCase):
    """Группа 3. Дата доставки."""

    def test_delivery_date_format(self):
        """Формат даты — YYYY-MM-DD."""
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")

    def test_delivery_date_short_distance(self):
        """Дистанция 100 км -> 1 день (max(1, 100//500))."""
        # 100 // 500 = 0 -> max(1, 0) = 1
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_delivery_date_long_distance(self):
        """Дистанция 5000 км -> 10 дней."""
        # 5000 // 500 = 10
        _, date = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertEqual(date, "2026-09-13")

    def test_express_delivery_not_slower_than_normal(self):
        """🚨 Экспресс не должен быть медленнее обычной доставки.

        В модуле days_needed //= 2 может дать 0 при days=1.
        Тест проверяет: дата экспресса не позже даты обычной.
        """
        _, date_normal = calculate_delivery_cost(1.0, 500, "обычный", is_express=False)
        _, date_express = calculate_delivery_cost(1.0, 500, "обычный", is_express=True)
        self.assertLessEqual(date_express, date_normal)

    def test_express_delivery_5000km(self):
        """5000 км, экспресс -> должно быть 5 дней (10 // 2)."""
        _, date = calculate_delivery_cost(1.0, 5000, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-08")


if __name__ == "__main__":
    unittest.main(verbosity=2)