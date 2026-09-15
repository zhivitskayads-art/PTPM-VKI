import logging
import os
import sys
import math

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(LOG_DIR, "file_txt.log"), encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)

EPS = 1e-9


def scale_to_canvas(points, size=100, padding=10):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y

    if width <= EPS or height <= EPS:
        return None

    available_size = size - 2 * padding
    scale = min(available_size / width, available_size / height)

    scaled_w = width * scale
    scaled_h = height * scale

    offset_x = (size - scaled_w) / 2
    offset_y = (size - scaled_h) / 2

    result = []
    for x, y in points:
        sx = (x - min_x) * scale + offset_x
        sy = (max_y - y) * scale + offset_y
        result.append((int(round(sx)), int(round(sy))))

    result = [(max(0, min(size, x)), max(0, min(size, y))) for x, y in result]
    return result


def calculate_triangle(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        logger.warning("Ошибочные числовые данные: стороны должны быть > 0. a=%s, b=%s, c=%s", a, b, c)
        return "не треугольник", [(-1, -1)] * 3

    if a + b <= c + EPS or a + c <= b + EPS or b + c <= a + EPS:
        logger.warning("Не выполняется неравенство треугольника. a=%s, b=%s, c=%s", a, b, c)
        return "не треугольник", [(-1, -1)] * 3

    if abs(a - b) <= EPS and abs(b - c) <= EPS:
        triangle_type = "равносторонний"
    elif abs(a - b) <= EPS or abs(b - c) <= EPS or abs(a - c) <= EPS:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    x = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
    y = math.sqrt(max(0.0, b ** 2 - x ** 2))

    points = [(0.0, 0.0), (c, 0.0), (x, y)]

    coords = scale_to_canvas(points)
    if coords is None:
        return "не треугольник", [(-1, -1)] * 3

    return triangle_type, coords


def main():
    logger.info("Приложение запущено")

    try:
        raw_input = []
        for _ in range(3):
            line = sys.stdin.readline()
            if not line:
                line = ""
            raw_input.append(line.strip())

        logger.debug("Входные строки: %s", raw_input)

        try:
            a = float(raw_input[0])
            b = float(raw_input[1])
            c = float(raw_input[2])
        except ValueError:
            logger.error("Невалидные (нечисловые) данные во входе", exc_info=True)
            print("")
            print("[(-2, -2), (-2, -2), (-2, -2)]")
            return

        triangle_type, coords = calculate_triangle(a, b, c)

        print(triangle_type)
        print(coords)

        if triangle_type == "не треугольник":
            logger.warning("Успешный запрос (ошибочные данные): тип=%s, координаты=%s", triangle_type, coords)
        else:
            logger.info("Успешный запрос: тип=%s, координаты=%s", triangle_type, coords)

    except Exception: # noqa
        logger.exception("Непредвиденная ошибка")
        print("")
        print("[(-2, -2), (-2, -2), (-2, -2)]")


if __name__ == "__main__":
    main()