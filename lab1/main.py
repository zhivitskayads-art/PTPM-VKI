
# ============ ИНТЕРФЕЙС ============

class Parkable:
    """Интерфейс для объектов, которые могут быть припаркованы"""

    def park(self):
        raise NotImplementedError("Метод park должен быть реализован")

    def unpark(self):
        raise NotImplementedError("Метод unpark должен быть реализован")

    def get_parking_status(self):
        raise NotImplementedError("Метод get_parking_status должен быть реализован")


# ============ БАЗОВЫЙ КЛАСС ============

class Vehicle(Parkable):
    """
    Базовый класс для всех транспортных средств
    """

    def __init__(self, license_plate, brand, color):
        self.license_plate = license_plate  # госномер
        self.brand = brand  # марка
        self.color = color  # цвет
        self.is_parked = False  # состояние машины на парковке
        self.vehicle_type = "Транспортное средство"

    def get_vehicle_type(self):
        return self.vehicle_type

    def park(self):
        """Метод для парковки"""
        if not self.is_parked:
            self.is_parked = True
            print(f"{self.get_vehicle_type()} {self.license_plate} припаркована")
        else:
            print(f"{self.license_plate} уже на парковке!")

    def unpark(self):
        """Метод для выезда с парковки"""
        if self.is_parked:
            self.is_parked = False
            print(f"{self.get_vehicle_type()} {self.license_plate} уехала")
        else:
            print(f"{self.license_plate} не на парковке!")

    def get_parking_status(self):
        """Метод получения состояния машины на парковке"""
        status = "Припаркована" if self.is_parked else "Свободна"
        return f"{self.license_plate} ({self.brand}, {self.color}) - {status}"


# ============ ДОЧЕРНИЙ КЛАСС 1 ============

class Car(Vehicle):
    """Класс для легковых автомобилей"""

    def __init__(self, license_plate, brand, color, num_doors=4):
        Vehicle.__init__(self, license_plate, brand, color)
        self.num_doors = num_doors  # поле
        self.vehicle_type = "Легковой автомобиль"

    def get_vehicle_type(self):
        return self.vehicle_type

    def park(self):
        """Переопределенный метод park"""
        Vehicle.park(self)
        print(f"  {self.brand} запаркована на месте для легковых авто")

    def unpark(self):
        """Переопределенный метод unpark"""
        Vehicle.unpark(self)
        print(f"  {self.brand} покинула парковку")


# ============ ДОЧЕРНИЙ КЛАСС 2 ============

class Truck(Vehicle):
    """Класс для грузовых автомобилей"""

    def __init__(self, license_plate, brand, color, cargo_capacity=1000):
        Vehicle.__init__(self, license_plate, brand, color)
        self.cargo_capacity = cargo_capacity  # поле
        self.vehicle_type = "Грузовик"

    def get_vehicle_type(self):
        return self.vehicle_type

    def park(self):
        """Переопределенный метод park"""
        Vehicle.park(self)
        print(f"  {self.brand} запаркована на месте для грузовых авто")

    def unpark(self):
        """Переопределенный метод unpark"""
        Vehicle.unpark(self)
        print(f"  {self.brand} покинула парковку")


# ============ КЛАСС ПАРКОВКИ ============

class ParkingLot:
    """Класс для управления парковкой"""

    def __init__(self, max_capacity=10):
        self.max_capacity = max_capacity
        self.parked_vehicles = []  # список припаркованных ТС

    def add_vehicle(self, vehicle):
        """Добавить машину на парковку"""
        if len(self.parked_vehicles) >= self.max_capacity:
            print(f"Парковка заполнена! Максимум {self.max_capacity} мест")
            return False

        if vehicle.is_parked:
            print(f"{vehicle.license_plate} уже на парковке!")
            return False

        vehicle.park()
        self.parked_vehicles.append(vehicle)
        return True

    def remove_vehicle(self, license_plate):
        """Убрать машину с парковки"""
        for vehicle in self.parked_vehicles:
            if vehicle.license_plate == license_plate:
                vehicle.unpark()
                self.parked_vehicles.remove(vehicle)
                return True

        print(f"ТС с номером {license_plate} не найдено на парковке")
        return False

    def show_status(self):
        """Показать состояние парковки"""
        print("\n" + "=" * 50)
        print(f"ПАРКОВКА: {len(self.parked_vehicles)}/{self.max_capacity} мест занято")
        print("=" * 50)

        if not self.parked_vehicles:
            print("Парковка пуста")
        else:
            for i, vehicle in enumerate(self.parked_vehicles, 1):
                print(f"{i}. {vehicle.get_parking_status()}")
        print("=" * 50 + "\n")


# ============ ТЕСТИРОВАНИЕ ============

def main():
    """Демонстрация работы"""

    # Создаем парковку
    parking = ParkingLot(max_capacity=5)

    # Создаем транспортные средства
    car1 = Car("A123BC", "Toyota", "Красный", 4)
    car2 = Car("B456DE", "BMW", "Черный", 2)
    truck1 = Truck("C789FG", "Volvo", "Белый", 5000)

    print("СОЗДАННЫЕ ТРАНСПОРТНЫЕ СРЕДСТВА:")
    print(f"  - {car1.get_vehicle_type()}: {car1.brand} {car1.license_plate}")
    print(f"  - {car2.get_vehicle_type()}: {car2.brand} {car2.license_plate}")
    print(f"  - {truck1.get_vehicle_type()}: {truck1.brand} {truck1.license_plate}")
    print()

    # Показываем пустую парковку
    parking.show_status()

    # Паркуем машины
    print("--- ПАРКУЕМ ТРАНСПОРТ ---")
    parking.add_vehicle(car1)
    parking.add_vehicle(truck1)
    parking.add_vehicle(car2)

    parking.show_status()

    # Убираем машину
    print("--- УБИРАЕМ МАШИНУ ---")
    parking.remove_vehicle("A123BC")

    parking.show_status()

    # Пытаемся убрать несуществующую
    print("--- ПОПЫТКА УБРАТЬ НЕСУЩЕСТВУЮЩУЮ МАШИНУ ---")
    parking.remove_vehicle("ZZZ999")


if __name__ == "__main__":
    main()