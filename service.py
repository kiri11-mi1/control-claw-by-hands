import math
import logging

from serial import Serial

from finger import Finger


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


def get_distance(finger_1: Finger, finger_2: Finger) -> float:
    return math.sqrt(
        (finger_1.x - finger_2.x) ** 2 + (finger_1.y - finger_2.y) ** 2
    )


def get_claw_angle(distance_between_fingers) -> int:
    """получение угла клешни"""
    value = 0.11*(180 - distance_between_fingers)
    # print(f'{distance_between_fingers=}')
    # print(f'{value=}')
    return 0 if value < 0 else value


def get_rotate_angle_for_axis(finger: Finger, width: int) -> float:
    """поворот оси"""
    result = finger.x*(180 / width)
    logging.info(result)

    return round(result)


def send_to_arduino(protocol: Serial, data: float):
    if isinstance(data, float):
        return
    message = f'#{data};'
    protocol.write(bytes(message, 'utf-8'))
    logging.info(message)
