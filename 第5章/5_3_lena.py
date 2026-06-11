import cv2
print(cv2.__version__)
import numpy as np
img = cv2.imread('lena.jpg')

cv2.imshow('lena',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
