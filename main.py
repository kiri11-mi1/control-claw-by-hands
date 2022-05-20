import logging

import cv2
import mediapipe as mp

from arduino import Arduino
from manipulator import Claw, HorizontalLever, VerticalLever
import config as cfg
import service
from finger import Finger


claw = Claw()
horizontal_lever = HorizontalLever()
vertical_lever = VerticalLever()
arduino = Arduino(cfg.COM_PORT_6, cfg.BOD_SPEED)
camera = cv2.VideoCapture(cfg.BUILTIN_CAMERA)

fingers = [Finger() for _ in range(cfg.FINGER_POINTS_COUNT)]

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

old_finger = Finger()
flag = True

while cv2.waitKey(cfg.TIME_DELAY) != ord('q'):
    good, img = camera.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            for id, finger_point in enumerate(hand_lms.landmark):
                height, width, _ = img.shape
                fingers[id].x = int(finger_point.x * width)
                fingers[id].y = int(finger_point.y * height)

                if id == cfg.FOREFINGER_ID or id == cfg.THUMB_ID:

                    cv2.circle(img, (fingers[id].x, fingers[id].y), cfg.CIRCLE_RADIUS, cfg.PINK_COLOR, cv2.FILLED)
                    distance = service.get_distance(fingers[cfg.FOREFINGER_ID], fingers[cfg.THUMB_ID])
                    logging.info(distance)

                    if distance < cfg.MAX_DISTANCE_BETWEEN_FINGERS:
                        # получение данных по оси Y
                        vertical_data = vertical_lever.get_angle(fingers[cfg.THUMB_ID], cfg.HEIGHT)
                        arduino.send(vertical_lever.get_data(vertical_data))

                        # получение данных по оси X
                        horizontal_data = horizontal_lever.get_angle(fingers[cfg.THUMB_ID], cfg.WIDTH)
                        arduino.send(horizontal_lever.get_data(horizontal_data))

                        # отводим клешню в нулевое положение
                        arduino.send(claw.get_data(0))

                    else:
                        logging.info('КЛЕШНЯ АКТИВИРОВАНА')
                        arduino.send(claw.get_data(distance))

    cv2.imshow("Hand recognizer", img)
