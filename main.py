import cv2
import numpy as np
from math import atan, fabs

cap0 = cv2.VideoCapture(0) # иниацилазация потока камеры -_-


def image_scan():
    good, image = cap0.read()
    print(good)
    if not good:
        print("Ошибка - не могу получить изображение...")
    else:
        img_hsv = cv2.cv2tColor(image, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([60, 255, 255])
        mask = cv2.inRange(img_hsv, lower_red, upper_red)
        cnt = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if not cnt:
            for c in cnt:
                area = cv2.contourArea(c)
                if abs(area) < 300:
                    continue
                hull = cv2.convexHull(c)
                approx = cv2.approxPolyDP(hull, cv2.arcLength(c, True) * 0.02, True)
                if len(approx) < 5:
                    continue
                M = cv2.moments(c)
                try:
                    x = int(M["m10"] / M['m00'])
                    y = int(M["m01"] / M['m00'])
                except ZeroDivisionError:
                    return False, 0, 0
                cv2.circle(image, (x, y), 4, (127, 255, 0), 4)

                int(x)  # Устанавливаем X тип целого числа
                int(y)  # Устанавливаем Y тип целого числа

                y = 117.5 - y  # Корректировка значений X и Y
                x = x - 160  # для удобной дальнейшей работы

                if y == 0:
                    z = 0
                else:
                    z = x / y

                z = atan(fabs(z)) / 3.14159 * 180

                if y < 0:
                    z = 180 - z
                if x < 0:
                    z = -z

                z = z.real

                int(z)

                return z

        cv2.imshow("Image", image)
        cv2.waitKey(1)


image_scan()
