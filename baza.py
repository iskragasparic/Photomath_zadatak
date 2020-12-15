import numpy as np
import cv2
import os

"""Program je spremio 30 fontova u training set, a 8 fontova u testing set"""


IMG_DIR = '/home/iskra/Desktop/photomath/glavni/baza2/baza'

c_label = 0
c_38 = 1

for img in sorted(os.listdir(IMG_DIR)):
        print(img)
        img_array = cv2.imread(os.path.join(IMG_DIR,img), cv2.IMREAD_GRAYSCALE)

        img_array = cv2.resize(img_array,(28,28))
        img_array = (img_array.flatten())
        img_array = np.concatenate((np.asarray([c_label]), img_array))
        img_array  = img_array.reshape(-1, 1).T

        if c_38 <= 30:
            with open('train.csv', 'ab') as f:
                np.savetxt(f, img_array, delimiter=",")
        else:
            with open('test.csv', 'ab') as g:
                np.savetxt(g, img_array, delimiter=",")

        if c_38 == 38:
            c_38 = 0
            c_label = c_label + 1
        c_38 = c_38 + 1
