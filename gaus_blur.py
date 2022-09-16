import cv2
import numpy

grey = cv2.imread("img/hb_2.jpg")
grey_copy = grey.copy()
n = 5
matr_gauss = [[0 for i in range(0,n)]  for i in range(0,n)]

def gauss(x, y):
    a = b = 2
    sig = 1
    return (1 / (2 * numpy.pi * sig ** 2)) * numpy.exp(-((x - a) ** 2 + (y - b) ** 2) / (2 * sig ** 2))

ln = [i for i in range(0, n)]

sum_matr = 0

for i in ln:
    for j in ln:
        matr_gauss[i][j] = gauss(i, j)
        sum_matr += matr_gauss[i][j]
        
for i in ln:
    for j in ln:
        matr_gauss[i][j] /= sum_matr

def gauss_blur(ker, foto_grey):
    for i in range(0, 883):
        for j in range(0, 697):
            sum_value = 0
            for k in range(0,4):
                for l in range(0,4):
                    sum_value += ker[k][l]*foto_grey[i+k][j+l][0]
            for k in range(0,3):
                foto_grey[i+2][j+2][k] = sum_value
    return foto_grey

new_grey = gauss_blur(matr_gauss, grey.copy())
cv2.namedWindow('Display window', cv2.WINDOW_NORMAL)
two_foto = numpy.concatenate((new_grey,grey),axis=1)
cv2.imshow("Blur", two_foto)
cv2.imwrite("img/blur_photo.jpg", two_foto)
cv2.waitKey(0)
cv2.destroyAllWindows()