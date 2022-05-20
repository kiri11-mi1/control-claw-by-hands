import math
import logging

from finger import Finger


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


def get_distance(finger_1: Finger, finger_2: Finger) -> float:
    return math.sqrt(
        (finger_1.x - finger_2.x) ** 2 + (finger_1.y - finger_2.y) ** 2
    )
