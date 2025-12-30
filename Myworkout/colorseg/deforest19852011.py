
import cv2
import matplotlib.pyplot as plt
import numpy as np

# Read the image in color
img1985 = cv2.imread('img/1985.png', cv2.IMREAD_COLOR)
img1993 = cv2.imread('img/1993.png', cv2.IMREAD_COLOR)
img2001 = cv2.imread('img/2001.png', cv2.IMREAD_COLOR)
img2011 = cv2.imread('img/2011.png', cv2.IMREAD_COLOR)
b1, g1, r1 = cv2.split(img1985)
b4, g4, r4 = cv2.split(img2011)

# Show the channels.
plt.figure(figsize = [20, 15])
plt.subplot(331); plt.imshow(img1985[:, :, ::-1]); plt.title('Original 1985')
plt.subplot(332); plt.imshow(img2011[:, :, ::-1]); plt.title('Original 2011')

plt.subplot(334); plt.imshow(r1); plt.title('Red Channel - 1985')
plt.subplot(335); plt.imshow(g1); plt.title('Green Channel - 1985')
plt.subplot(336); plt.imshow(b1); plt.title('Blue Channel - 1985')

plt.subplot(337); plt.imshow(r4); plt.title('Red Channel - 2011')
plt.subplot(338); plt.imshow(g4); plt.title('Green Channel - 2011')
plt.subplot(339); plt.imshow(b4); plt.title('Blue Channel - 2011')
plt.show()