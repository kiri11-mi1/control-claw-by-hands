import logging

from serial import Serial


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


class Arduino:
    def __init__(self, port: int, bod_speed: int):
        self.uart = Serial(port, bod_speed)

    def send(self, data):
        message = f'#{data};'
        self.uart.write(bytes(message, 'utf-8'))
        logging.info(message)
