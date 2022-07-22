import cv2
import numpy as np


kamera = cv2.VideoCapture(0)


sayac = True
sayi = 0
while sayac is True:
    sayi = sayi+100
    ret, frame = kamera.read()
    frame = cv2.flip(frame, 1, )
    width = 640
    height = 480
    cx = width / 2
    cy = height / 2
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernal = np.ones((5, 5), "uint8")

    red_lower = np.array([161, 155, 84])
    red_higher = np.array([179, 255, 255])

    red_mask = cv2.inRange(hsv, red_lower, red_higher)
    redmask_dilate = cv2.dilate(red_mask, kernal)
    redmask_blur = cv2.GaussianBlur(redmask_dilate, (5, 5), 4 / 6)

    red_contours, hierarchy = cv2.findContours(redmask_blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0

    for pic, contour in enumerate(red_contours):
        area = cv2.contourArea(contour)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            i = i + 1
            if i == 2:
                break

            centerX = x + (w // 2)
            centerY = y + (h // 2)

            if centerX < cx and centerY < cy:
                print(centerX, centerY)
                #sayac = False
            elif centerX < cx and centerY > cy:
                print(centerX, centerY)
                #sayac = False
            elif centerX > cx and centerY < cy:
                print(centerX, centerY)
                #sayac = False
            elif centerX > cx and centerY > cy:
                print(centerX, centerY)
                #sayac = False

            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            frame = cv2.circle(frame, (centerX, centerY), 5, (0, 0, 255), -1)

            if y < 10 and x <= 360:
                frame = cv2.putText(frame, f"x={centerX} y={centerY}", (x, y + h + 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255), 3)
            elif y < 10 and x > 360:
                frame = cv2.putText(frame, f"x={centerX} y={centerY}", (350, y + h + 20),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    (0, 0, 255), 3)
            elif y > 10 and x <= 360:
                frame = cv2.putText(frame, f"x={centerX} y={centerY}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255),
                                    3)
            elif y > 10 and x > 360:
                frame = cv2.putText(frame, f"x={centerX} y={centerY}", (350, y), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255), 3)

    cv2.imshow("KAMERA", frame)
    cv2.imshow("FILTRE", red_mask)
    if cv2.waitKey(1) == ord("q"):
        break
    if sayi > 10000:
        sayi = 0

kamera.release()
cv2.destroyAllWindows()