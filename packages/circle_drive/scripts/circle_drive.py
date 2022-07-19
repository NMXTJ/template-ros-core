# Импорт базового класса для всех gym_duckietown решений:
from gym_duckietown.tasks.task_solution import TaskSolution
# Импорт библиотеки компьютерной математики:
import numpy as np
# Импорт библиотеки для компьютерного зрения:
import cv2

yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([30, 255, 255])
# Каждое решение -- класс-наследник TaskSolution
class DontCrushDuckieTaskSolution(TaskSolution):
    # Стандартный конструктор
    def __init__(self, generated_task):
        super().__init__(generated_task)

    # Именно данный метод содержит код, который будет выполнен на роботе
    def solve(self):
        # Через объект env решение сможет взаимодействовать с внешним миром
        env = self.generated_task['env']
        # Метод step принимает линейную и угловую скорость робота и возвращает obs (observation), содержащий картинку с камеры робота.
        # Так как мы никуда не движемся, следующей строчкой мы получает картинку в начальном положении робота
        obs, _, _, _ = env.step([0, 0])

        # Конвертация изображения в формат RGB для более удобной работы:
        img = cv2.cvtColor(np.ascontiguousarray(obs), cv2.COLOR_BGR2RGB)

        # Теперь мы можем обработать изображение. Например, поискать на нем уточек

        # Условие, истинность которого обозначает продолжение движения прямо:
        condition = True
        while condition:
            # Даем команду роботу ехать прямо.
            # Действие выполняется квант времени и метод возвращает новое изображение с камеры робота
            obs, _, _, _ = env.step([1, 0])
            img = cv2.cvtColor(np.ascontiguousarray(obs), cv2.COLOR_RGB2HSV)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
            yellow_ratio = (cv2.countNonZero(mask_yellow)) / (img.size / 3)
            res = np.round(yellow_ratio * 100, 2)

            if res > 6.5:
                #env.step([0, 0])
                condition = False
            # Снова конвертируем изображе
            # ние и как-то его обрабатываем. Например, ищем уточку.
            # Определяем пора ли остановиться
            # condition = True
            # Метод симулятора, который решение вызывает после каждой итерации обработки очередного кадра
            env.render()
