import cv2
import mediapipe as mp
import math
import time
import keyboard
from voice import voice

import serial
import serial.tools.list_ports
import numpy as np

# Функция для автоматического поиска и подключения к Arduino
def find_arduino_port():
    # Получаем список всех доступных COM-портов
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(port, end=" ")
        try:
            # Пытаемся открыть каждый порт
            ser = serial.Serial(port.device, 9600, timeout=2)
            print("opened")
            return ser  # Возвращаем объект порта, если успешно
        except serial.SerialException:
            # Продолжаем поиск, если порт не подходит
            continue

    # Выводим сообщение, если Arduino не найдена
    print("Arduino не найдена.")
    return None



# Ищем Arduino и подключаемся
ser = find_arduino_port()
if ser is None:
    exit()  # Завершаем программу, если подключение не удалось
time.sleep(2) #Ждем открытия порта

words_codes = [
    ("выстрел", 1)
]

nap = 1

main_state = 127

main_flag = 0

state = 0
radius = 10
thickness = 4
all_x = []
x_face = []
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


def get_distanse_m(size, angle):
    # size - meters
    return (size) / (2 * math.tan(math.radians(angle / 2)))


# 75, 52

old_state = 0
res_state = 0
k_filt = 0.5
cap = cv2.VideoCapture(1)
otr = True

old_delta, delta = 0, 0

dop_state, dop_old_state = 0, 0

with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as holistic:
    while True:
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = holistic.process(image)

        # Draw landmark annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        if results.pose_landmarks:
            all_x = list(map(lambda x: x.x, results.pose_landmarks.landmark))
            face_x = list(map(lambda x: x.x, filter(lambda x: x.x > 0 and x.x < 1, results.pose_landmarks.landmark[:11])))
            # print(results.pose_landmarks.landmark[:11])
            # print(len(face_x), len(list(map(lambda x: x.x, filter(lambda x: x.x > 0 and x.x < 1, results.pose_landmarks.landmark[:11])))))

            height, width = image.shape[:2]
            if len(face_x) > 0:
                state = int(old_state + ((sum(face_x) / len(face_x)) % 1 * 255 - old_state) * k_filt)
                old_state = state
                dop_old_state = dop_state
                dop_state = int(dop_old_state + ((sum(face_x) / len(face_x)) % 1 * width - dop_old_state) * k_filt)
                image = cv2.circle(image, (dop_state, 80), radius, (255, 255, 0), thickness)
                image = cv2.circle(image, (int(sum(face_x) / len(face_x) * width), 50), radius, (0, 255, 0), thickness)
                image = cv2.circle(image, (width // 2, 20), radius, (0, 0, 0), thickness)
                delta = int((dop_state - 320) // 30)

                if abs(delta) < 3 and abs(delta) >= 1:
                    delta = int(dop_state - 320)
                    if delta > 0:
                        delta = 1
                    elif delta < 0:
                        delta = -1
                if abs(delta) < 1:
                    delta = 0
                    if main_flag:
                        # ser.write(bytearray([0]))
                        main_flag = 0

                if delta > 0:
                    nap = 1
                else:
                    nap = -1

                # if abs(delta) < 3 and abs(delta) > 1:
                #     delta = int((dop_state - 320) // 30)
                # elif abs(delta) <= 1:
                #     delta = 0



                main_state += delta

                main_state = max(45, min(main_state, 245))
        else:
            if main_state + nap > 245 or main_state + nap < 45:
                nap = -nap
            main_state += nap



        cv2.imshow('Dich', image)
        # print(max(45, min(main_state, 245)))
        print(main_flag, delta)
        if cv2.waitKey(1) == ord('q'):
            break
        ser.write(bytearray([max(45, min(main_state, 245))]))
cap.release()
cv2.destroyAllWindows()
