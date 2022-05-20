import logging

from finger import Finger


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

class Manipulator:
    def get_angle(self, finger: Finger, length_side: int):
        pass

    def get_data(self, data: float):
        pass


class Claw(Manipulator):
    def get_data(self, distance_between_fingers: float):
        value = 0.11 * (180 - distance_between_fingers)
        new_value = 0 if value < 0 else round(value)
        return f'C{new_value}'


class VerticalLever(Manipulator):
    max_angle = 135

    def get_angle(self, finger: Finger, length_side: int):
        result = self.max_angle - finger.y * (self.max_angle / length_side)
        logging.info(result)

        return round(result)

    def get_data(self, data: float):
        return f'V{data}'


class HorizontalLever(Manipulator):
    def get_angle(self, finger: Finger, length_side: int):
        result = finger.x*(180 / length_side)
        logging.info(result)

        return round(result)

    def get_data(self, data: float):
        return f'H{data}'
