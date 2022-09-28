import cv2
import numpy as np
import math
from numba import njit

@njit
def gaussmatr(n,q):
    return np.array([[(1/(2*math.pi*q*q)*math.exp(-((j-n//2)*(j-n//2)+(i-n//2)*(i-n//2))/2*q*q)) for j in range(n)] for i in range(n)])

@njit
def conv(img,matr,n):
    img2 = img.copy()
    h, w = img2.shape[:2]
    start = n // 2
    finishh = h - start
    finishw = w - start
    for i in range(start, finishh):
        for j in range(start, finishw):

            newpixel = 0
            for k in range(n):
                for l in range(n):
                    newpixel += img[i - start + k][j - start + l] * matr[k][l]

            img2[i][j] = newpixel

    return img2


def anglsobel(x,y,tg):
    if ((x>0 and y<0 and tg<-2.414) or (x<0 and y<0 and tg> 2.414)):
       return 0
    if (x>0 and y<0 and tg<-0.414):
        return 1
    if ((x>0 and y<0 and tg>-0.414) or (x>0 and y>0 and tg< 0.414)):
        return 2
    if (x > 0 and y > 0 and tg < 2.414):
        return 3
    if ((x>0 and y>0 and tg > 2.414) or (x<0 and y>0 and tg< -2.414)):
        return 4
    if (x < 0 and y > 0 and tg < -0.414):
        return 5
    if ((x<0 and y>0 and tg>0.414) or (x<0 and y<0 and tg< 0.414)):
        return 6
    if (x < 0 and y < 0 and tg < 2.414):
        return 7
def anglsobel2(x,y,tg):
    if ((x>0 and y<0 and tg<-2.414) or (x<0 and y<0 and tg> 2.414)):
       return 0
    if (x>0 and y<0 and tg<-0.414):
        return 1
    if ((x>0 and y<0 and tg>-0.414) or (x>0 and y>0 and tg< 0.414)):
        return 2
    if (tg == -0.785):
        return 3
    if ((x>0 and y>0 and tg > 2.414) or (x<0 and y>0 and tg< -2.414)):
        return 4
    if (x < 0 and y > 0 and tg < -0.414):
        return 5
    if ((x<0 and y>0 and tg>0.414) or (x<0 and y<0 and tg< 0.414)):
        return 6
    if (x < 0 and y < 0 and tg < 2.414):
        return 7

def isCorrectindex(matr,x,y,h,w):
    if (x < 0) or (x > (w-1)) or (y < 0) or (y > (h-1)):
        return 0
    else:
        return 1

def check(matr,x,y,v,h,w):
    if isCorrectindex(matr,x,y,h,w) == 0:
        return 0
    if matr[y][x] <= v:
        return 1
    return 0
@njit
def sign(a):
    if a < 0:
        return -1
    if a > 0:
        return 1
    return 0

def nonMaximumSupression(img):
    h, w = img2.shape[:2]
    result = np.zeros((h,w))
    gM, anglM = SobelOperator2(img)
    printmaxd(gM)
    for i in range(h):
        for j in range(w):
            if gM[i][j]== 0:
                continue
            dx = sign(math.cos(anglM[i][j]))
            dy = sign(math.sin(anglM[i][j]))
            if check(gM, j + dx, i + dy, gM[i][j],h,w) == 1:
                result[i+dy][j+dx] = 0
            if check(gM, j - dx, i - dy, gM[i][j],h,w) == 1:
                result[i-dy][j-dx] = 0
            result[i][j]=gM[i][j]
    return result
@njit
def doubleFiltr(matr,lowPr,highPr):
    down = 14
    up = 15
    h = len(matr)
    w = len(matr[0])
    result = np.zeros((h,w))
    for y in range(h):
        for x in range(w):
            if matr[y][x] >= up:
                result[y][x]=255
            elif matr[y][x]<=down:
                result[y][x]=0
            else:
                result[y][x]=127
    return result



def SobelOperator2(img):
    MGx = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
    MGy = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    imgx = conv(img,MGx,3)
    imgy = conv(img,MGy,3)

    G = np.sqrt(imgx*imgx+imgy*imgy)
    G = G.astype('int8')
    f = np.round(np.arctan2(imgx,imgy)/(math.pi/4))*(math.pi/4)-(math.pi/2)

    return G,f

def printmaxd(matr):
    for i in matr:
        print(i.max())



img = cv2.imread(r'img/new_hb_2.jpg',cv2.IMREAD_GRAYSCALE)
n = 3
h, w = img.shape[:2]
#cv2.imshow('window', img2)

gaussm = gaussmatr(n, 1)

sumgaussmatr = gaussm.sum()
gaussm = gaussm/sumgaussmatr

img2 = conv(img,gaussm,n)
cv2.imshow('window1', img2 )
img2 = nonMaximumSupression(img2)
img2 = doubleFiltr(img2,0.3,0.3)

# img2 = cv2.Canny(img,100,255)



cv2.imshow('window', img2 )
#cv2.imshow('window1', img3 )
cv2.waitKey(0)
cv2.destroyAllWindows()


print()
