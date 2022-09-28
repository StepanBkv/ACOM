import cv2
import numpy as np
import math


def GF(img, size, sigma):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    newGray = img

    newGray = cv2.cvtColor(newGray, cv2.COLOR_BGR2GRAY)

    h, w = newGray.shape[:2]

    n = size

    pad = n // 2
    g_m = [[0] * n for i in range(n)]

    summ = 0
    for i in range(n):
        for j in range(n):
            g_m[i][j] = (1 / (2 * np.pi * sigma ** 2) * np.exp(
                -((i - pad) ** 2 + (j - pad) ** 2) / (2 * sigma ** 2)))
            summ += g_m[i][j]

    summ_2 = 0
    for i in range(n):
        for j in range(n):
            g_m[i][j] = g_m[i][j] / summ
            summ_2 += g_m[i][j]

    finishh = h - pad
    finishw = w - pad

    for i in range(pad, finishh):
        for j in range(pad, finishw):
            new_value = 0
            for k in range(n):
                for l in range(n):
                    new_value = new_value + g_m[k][l] * gray[i - pad + k][j - pad + l]
            newGray[i][j] = new_value

    return newGray


def tang(x, y):
    tg = y / x

    a = 0

    if (x > 0 and y < 0 and tg < -2.414) or (x < 0 and y < 0 and tg > 2.414): a = 0
    if x > 0 and y < 0 and tg < -0.414: a = 1
    if (x > 0 and y < 0 and tg < -0.414) or (x > 0 and y > 0 and tg < 0.414): a = 2
    if x > 0 and y > 0 and tg < 2.414: a = 3
    if (x > 0 and y > 0 and tg > 2.414) or (x < 0 and y > 0 and tg > -2.414): a = 4
    if x < 0 and y > 0 and tg < -0.414: a = 5
    if (x < 0 and y > 0 and tg < -0.414) or (x < 0 and y < 0 and tg > 0.414): a = 6
    if x < 0 and y < 0 and tg < 2.414: a = 7

    return a


def main():
    size = 3
    pad = size // 2
    sigma = 0.5
    high = 100
    low = 50

    img1 = cv2.imread(r"img/new_hb_2.jpg")
    image_GF = GF(img1, 7, sigma)

    h, w = image_GF.shape[:2]

    image_GF1 = image_GF.copy()
    image_GF2 = [[0] * w for i in range(h)]

    finishh = h - pad
    finishw = w - pad

    g_m_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    g_m_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    for i in range(pad, finishh):
        for j in range(pad, finishw):
            valueX = 0
            valueY = 0
            for k in range(size):
                for l in range(size):
                    valueX = valueX + g_m_x[k][l] * image_GF[i - pad + k][j - pad + l]
                    valueY = valueY + g_m_y[k][l] * image_GF[i - pad + k][j - pad + l]
            image_GF1[i][j] = int(math.sqrt(valueX ** 2 + valueY ** 2))
            image_GF2[i][j] = tang(valueX, valueY)

    for i in range(pad, finishh):
        for j in range(pad, finishw):
            if image_GF2[i][j] == 0 | image_GF2[i][j] == 4:
                if image_GF1[i][j + 1] < image_GF1[i][j] & image_GF1[i][j] > image_GF1[i][j - 1]:
                    image_GF1[i][j] = image_GF1[i][j]
                else:
                    image_GF1[i][j] = 0
            if image_GF2[i][j] == 1 | image_GF2[i][j] == 5:
                if image_GF1[i + 1][j + 1] < image_GF1[i][j] & image_GF1[i][j] > image_GF1[i - 1][j - 1]:
                    image_GF1[i][j] = image_GF1[i][j]
                else:
                    image_GF1[i][j] = 0
            if image_GF2[i][j] == 2 | image_GF2[i][j] == 6:
                if image_GF1[i + 1][j] < image_GF1[i][j] & image_GF1[i][j] > image_GF1[i - 1][j]:
                    image_GF1[i][j] = image_GF1[i][j]
                else:
                    image_GF1[i][j] = 0
            if image_GF2[i][j] == 3 | image_GF2[i][j] == 7:
                if image_GF1[i + 1][j - 1] < image_GF1[i][j] & image_GF1[i][j] > image_GF1[i - 1][j + 1]:
                    image_GF1[i][j] = image_GF1[i][j]
                else:
                    image_GF1[i][j] = 0

    cv2.namedWindow("Lab", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Lab", image_GF1)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()