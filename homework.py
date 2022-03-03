from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    cf_run_1 = 18
    cf_run_2 = 20

    def get_spent_calories(self) -> float:
        cal = self.cf_run_1 * self.get_mean_speed() - self.cf_run_2
        return cal * self.weight / self.M_IN_KM * (self.duration * 60)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cf_walk_1 = 0.035
    cf_walk_2 = 2
    cf_walk_3 = 0.029

    action: int
    duration: float
    weight: float
    height: int

    def get_spent_calories(self) -> float:
        cal1 = (self.get_mean_speed() ** self.cf_walk_2 // self.height)
        cal2 = self.cf_walk_1 * self.weight
        cal3 = cal2 + cal1 * self.cf_walk_3 * self.weight
        return cal3 * (self.duration * 60)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    swim_cf_1 = 1.1
    swim_cf_2 = 2
    LEN_STEP = 1.38

    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        speed1 = self.length_pool * self.count_pool
        return speed1 / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        cal1 = self.get_mean_speed() + self.swim_cf_1
        return cal1 * self.swim_cf_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trn_type_dict = {'RUN': Running, 'WLK': SportsWalking, 'SWM': Swimming}
    return trn_type_dict[workout_type](*data)


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
