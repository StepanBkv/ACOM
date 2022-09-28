import cv2
import numpy as np
import math
from numba import njit 

@njit
def img_size(img):
    return img.shape[:2]

@njit
def doubleFiltr(img, size,lowPr,highPr):
    begin = size // 2
    h, w = img_size(img)
    end_h = h - begin
    end_w = w - begin
    for x in range(begin, end_h):
        for y in range(begin, end_w):
            if img[x][y][0] >= lowPr:
                img[x][y]= 255
            elif img[x][y][0]<=lowPr:
                img[x][y]= 0
            else:
                img[x][y]= 127
    return img

@njit
def tang(x, y):
    if x != 0:
        tg = y / x

    if ((x>0 and y<0 and tg<-2.414) or (x<0 and y<0 and tg> 2.414)):
       return 0
    elif (x>0 and y<0 and tg<-0.414):
        return 1
    elif ((x>0 and y<0 and tg>-0.414) or (x>0 and y>0 and tg< 0.414)):
        return 2
    elif (tg == -0.785):
        return 3
    elif ((x>0 and y>0 and tg > 2.414) or (x<0 and y>0 and tg< -2.414)):
        return 4
    elif (x < 0 and y > 0 and tg < -0.414):
        return 5
    elif ((x<0 and y>0 and tg>0.414) or (x<0 and y<0 and tg< 0.414)):
        return 6
    elif (x < 0 and y < 0 and tg < 2.414):
        return 7
    else: 
        return 0
@njit
def sobel_operation(img, size):
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    begin = size // 2
    h, w = img_size(img)

    end_h = h - begin
    end_w = w - begin

    Gv = img.copy()
    Gfi = [[0] * w for i in range(h)]
    
    for i in range(begin, end_h):
        for j in range(begin, end_w):
            x = 0
            y = 0
            for k in range(size):
                for l in range(size):
                    x += sobel_x[k][l] * img[i - begin + k][j - begin + l][0]
                    y += sobel_y[k][l] * img[i - begin + k][j - begin + l][0]
            Gv[i][j] = int(math.sqrt(x ** 2 + y ** 2))
            Gfi[i][j] = tang(x, y)
    return Gv, Gfi
@njit
def canny_alg(img, size, low, high):
    Gv, Gfi = sobel_operation(img, size)

    h,w = img_size(img)
    begin = size // 2 

    end_h = h - begin
    end_w = w - begin

    for i in range(begin, end_h):
        for j in range(begin, end_w):
            if Gfi[i][j] == 0 or Gfi[i][j] == 4:
                if Gv[i][j + 1][0] < Gv[i][j][0] and Gv[i][j][0] > Gv[i][j - 1][0]:
                    Gv[i][j] = Gv[i][j]
                else:
                    Gv[i][j] = [0,0,0]
            if Gfi[i][j] == 1 or Gfi[i][j] == 5:
                if Gv[i + 1][j + 1][0] < Gv[i][j][0] and Gv[i][j][0] > Gv[i - 1][j - 1][0]:
                    Gv[i][j] = Gv[i][j]
                else:
                    Gv[i][j] = [0,0,0]
            if Gfi[i][j] == 2 or Gfi[i][j] == 6:
                if Gv[i + 1][j][0] < Gv[i][j][0] and Gv[i][j][0] > Gv[i - 1][j][0]:
                    Gv[i][j] = Gv[i][j]
                else:
                    Gv[i][j] = [0,0,0]
            if Gfi[i][j] == 3 or Gfi[i][j] == 7:
                if Gv[i + 1][j - 1][0] < Gv[i][j][0] and Gv[i][j][0] > Gv[i - 1][j + 1][0]:
                    Gv[i][j] = Gv[i][j]
                else:
                    Gv[i][j] = [0,0,0]
    return Gv, size, low, high

@njit
def canny(img, size, low, high):
    img_1, size, low, high = canny_alg(img, size, low, high)
    img_1 = doubleFiltr(img, size, low, high)
    return img_1

def main():
    size = 3
    img = cv2.imread("img/oxxy_3.png", cv2.COLOR_BGR2GRAY)
    img_blur = cv2.blur(img,(1,1))
    img_canny = canny(img_blur, size, 145, 151)
    cv2.imwrite("img/photo_canny_5.jpg", img_canny)
    cv2.namedWindow("Lab", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Lab", img_canny)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()