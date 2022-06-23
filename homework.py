from dataclasses import asdict, dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message_output = ('Тип тренировки: {training_type}; '
                      'Длительность: {duration:.3f} ч.; '
                      'Дистанция: {distance:.3f} км; '
                      'Ср. скорость: {speed:.3f} км/ч; '
                      'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        """Возвращает информацию о выполненных упражнениях."""
        return self.message_output.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MINUTES_IN_HOURS: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_km = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration_km)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(self.__class__.__name__,
                            self.duration_km,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""

    RUN_CALORIE_1: float = 18
    RUN_CALORIE_2: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.duration_km = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        return ((self.RUN_CALORIE_1 * self.get_mean_speed()
                - self.RUN_CALORIE_2)
                * self.weight / self.M_IN_KM
                * (self.duration_km * self.MINUTES_IN_HOURS))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALK_CALORIE_1: float = 0.035
    WALK_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.WALK_CALORIE_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.WALK_CALORIE_2 * self.weight)
                * (self.duration_km * self.MINUTES_IN_HOURS))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    SWIM_CALORIE_1: float = 1.1
    SWIM_CALORIE_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration_km)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.SWIM_CALORIE_1) * self.SWIM_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: List) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_data: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }

    if workout_type in class_data:
        return class_data[workout_type](*data)
    else:
        raise ValueError('Нет такого типа тренировки!')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
