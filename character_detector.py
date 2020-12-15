import cv2
import numpy as np
import sys

"""Argument komandne linije je naziv slike u kojoj se detektiraju znamenke"""

img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

#dimenzije slike
height, width = img.shape 

#slika prebacena u negativ (zbog funkcije findContours)
for i in range(0, height - 1): 
    for j in range(0, width - 1): 
        img[i,j] = 255 - img[i,j]

#iz grayscale u format crno-bijelo
(T,tresh_image) = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU,img)

#detekcija znakova na slici
contours, hierarchy = cv2.findContours(tresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
d=0
ch_list = []

for ctr in contours:
    # Dobivanje bounding boxa
    x, y, w, h = cv2.boundingRect(ctr)
    # Dobivanje ROI-a (region of interest)
    roi = tresh_image[y:y+h, x:x+w]

    m,n = roi.shape
    roi = cv2.resize(roi,(32,32))

    cv2.imwrite('character_%d.png'%d, roi)

    ch_list.append(roi)
    d+=1

ch_list = np.asarray(ch_list)
ch_list = (ch_list.flatten())
ch_list  = ch_list.reshape(-1, 1).T

with open('output.csv', 'ab') as f:
    np.savetxt(f, ch_list, delimiter=",")
