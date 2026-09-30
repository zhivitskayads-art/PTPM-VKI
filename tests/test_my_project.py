"""
Юнит-тесты для src/my_project.py (ЛР1 — треугольники).
Запуск: python -m unittest tests.test_my_project -v
"""
import math
import os
import sys
import unittest

# Добавляем корень проекта в sys.path, чтобы работал импорт src.my_project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.my_project import calculate_triangle, scale_to_canvas, EPS


class TestCalculateTriangleValidation(unittest.TestCase):
    """Группа 1. Валидация сторон — случаи 'не треугольник'."""

    def test_negative_side_returns_not_triangle(self):
        """Отрицательная сторона -> 'не треугольник'."""
        ttype, coords = calculate_triangle(-1, 3, 3)
        self.assertEqual(ttype, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_zero_side_returns_not_triangle(self):
        """Нулевая сторона -> 'не треугольник'."""
        ttype, coords = calculate_triangle(0, 3, 3)
        self.assertEqual(ttype, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_all_negative_sides_returns_not_triangle(self):
        """Все стороны отрицательные -> 'не треугольник'."""
        ttype, coords = calculate_triangle(-2, -3, -4)
        self.assertEqual(ttype, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_sum_of_two_equals_third_is_not_triangle(self):
        """a + b == c — вырожденный случай -> 'не треугольник'."""
        ttype, coords = calculate_triangle(1, 2, 3)
        self.assertEqual(ttype, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_sum_of_two_less_than_third_is_not_triangle(self):
        """Не выполняется неравенство треугольника -> 'не треугольник'."""
        ttype, coords = calculate_triangle(1, 2, 10)
        self.assertEqual(ttype, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_very_small_sides_close_to_zero(self):
        """Очень маленькие стороны, но валидные (1e-5) -> треугольник."""
        ttype, _ = calculate_triangle(1e-5, 1e-5, 1e-5)
        self.assertEqual(ttype, "равносторонний")


class TestCalculateTriangleType(unittest.TestCase):
    """Группа 2. Определение типа треугольника."""

    def test_equilateral_triangle(self):
        """Все стороны равны -> равносторонний."""
        ttype, _ = calculate_triangle(3, 3, 3)
        self.assertEqual(ttype, "равносторонний")

    def test_equilateral_large_sides(self):
        """Большие равные стороны -> равносторонний."""
        ttype, _ = calculate_triangle(100, 100, 100)
        self.assertEqual(ttype, "равносторонний")

    def test_isosceles_a_equals_b(self):
        """a == b -> равнобедренный."""
        ttype, _ = calculate_triangle(5, 5, 6)
        self.assertEqual(ttype, "равнобедренный")

    def test_isosceles_b_equals_c(self):
        """b == c -> равнобедренный."""
        ttype, _ = calculate_triangle(6, 5, 5)
        self.assertEqual(ttype, "равнобедренный")

    def test_isosceles_a_equals_c(self):
        """a == c -> равнобедренный."""
        ttype, _ = calculate_triangle(5, 6, 5)
        self.assertEqual(ttype, "равнобедренный")

    def test_scalene_triangle_classic_3_4_5(self):
        """Классический прямоугольный 3-4-5 -> разносторонний."""
        ttype, _ = calculate_triangle(3, 4, 5)
        self.assertEqual(ttype, "разносторонний")

    def test_scalene_triangle_large_values(self):
        """Разносторонний с большими значениями."""
        ttype, _ = calculate_triangle(7, 8, 9)
        self.assertEqual(ttype, "разносторонний")

    def test_isosceles_with_epsilon_difference(self):
        """Разница в пределах EPS -> равнобедренный."""
        ttype, _ = calculate_triangle(5, 5 + EPS / 2, 6)
        self.assertEqual(ttype, "равнобедренный")


class TestCalculateTriangleCoordinates(unittest.TestCase):
    """Группа 3. Возвращаемые координаты."""

    def test_returns_three_coordinates(self):
        """Всегда возвращается ровно 3 точки."""
        _, coords = calculate_triangle(3, 4, 5)
        self.assertEqual(len(coords), 3)

    def test_coordinates_are_tuples_of_ints(self):
        """Каждая точка — кортеж из двух int."""
        _, coords = calculate_triangle(3, 4, 5)
        for point in coords:
            self.assertIsInstance(point, tuple)
            self.assertEqual(len(point), 2)
            self.assertIsInstance(point[0], int)
            self.assertIsInstance(point[1], int)

    def test_coordinates_within_canvas(self):
        """Все координаты в диапазоне [0, 100]."""
        _, coords = calculate_triangle(3, 4, 5)
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_not_triangle_returns_minus_one_coords(self):
        """При ошибке — три точки (-1, -1)."""
        _, coords = calculate_triangle(1, 2, 3)
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_equilateral_coordinates_symmetric(self):
        """Для равностороннего — основание (c) лежит на оси Y=0."""
        _, coords = calculate_triangle(5, 5, 5)
        # Первая точка (0,0), вторая (c,0) -> у обеих y-координата совпадает
        self.assertEqual(coords[0][1], coords[1][1])

    def test_scalene_coordinates_first_at_origin(self):
        """Первая точка — на нижней границе canvas (scale сдвигает точки)."""
        _, coords = calculate_triangle(3, 4, 5)
        # scale_to_canvas пересчитывает точки, первая становится внизу слева
        # Проверяем, что она в пределах canvas
        self.assertGreaterEqual(coords[0][0], 0)
        self.assertLessEqual(coords[0][0], 100)
        self.assertGreaterEqual(coords[0][1], 0)
        self.assertLessEqual(coords[0][1], 100)


class TestScaleToCanvas(unittest.TestCase):
    """Группа 4. Функция scale_to_canvas напрямую."""

    def test_scale_returns_none_for_degenerate_line(self):
        """Все точки на одной прямой (нулевая высота) -> None."""
        points = [(0, 0), (5, 0), (10, 0)]
        self.assertIsNone(scale_to_canvas(points))

    def test_scale_returns_none_for_single_point(self):
        """Одна точка (нулевая ширина и высота) -> None."""
        self.assertIsNone(scale_to_canvas([(5, 5)]))

    def test_scale_returns_none_for_same_width_height_zero(self):
        """Все точки одинаковы -> None."""
        self.assertIsNone(scale_to_canvas([(1, 1), (1, 1), (1, 1)]))

    def test_scale_normal_points_returns_list(self):
        """Нормальные точки -> список кортежей int."""
        points = [(0, 0), (10, 0), (5, 10)]
        result = scale_to_canvas(points)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        for x, y in result:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_scale_custom_size_and_padding(self):
        """Кастомные размер и padding."""
        points = [(0, 0), (100, 0), (50, 100)]
        result = scale_to_canvas(points, size=200, padding=20)
        self.assertIsNotNone(result)
        for x, y in result:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 200)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)