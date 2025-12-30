import cv2
import matplotlib.pyplot as plt
import numpy as np

# Read the image in color
img1985 = cv2.imread('img/1985.png', cv2.IMREAD_COLOR)
img1993 = cv2.imread('img/1993.png', cv2.IMREAD_COLOR)
img2001 = cv2.imread('img/2001.png', cv2.IMREAD_COLOR)
img2011 = cv2.imread('img/2011.png', cv2.IMREAD_COLOR)

fig = plt.figure(figsize=[20, 10])

ax = fig.add_subplot(2, 2, 1)
ax.set_title('1985')
plt.imshow(img1985[:, :, ::-1])

ax = fig.add_subplot(2, 2, 2)
ax.set_title('1993')
plt.imshow(img1993[:, :, ::-1])

ax = fig.add_subplot(2, 2, 3)
ax.set_title('2001')
plt.imshow(img2001[:, :, ::-1])

ax = fig.add_subplot(2, 2, 4)
ax.set_title('2011')
plt.imshow(img2011[:, :, ::-1])
plt.show()