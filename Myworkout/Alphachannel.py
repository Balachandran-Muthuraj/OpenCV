import cv2
import matplotlib.pyplot as plt

img=cv2.imread('img/opencv_logo.png',cv2.IMREAD_UNCHANGED)

print(img.shape)
b,g,r,a=cv2.split(img)
# Plot the images
plt.figure(figsize=(18, 5))
plt.subplot(141)
plt.imshow(b, cmap='gray')
plt.title('Blue')

plt.subplot(142)
plt.imshow(g, cmap='gray')
plt.title('Green')

plt.subplot(143)
plt.imshow(r, cmap='gray')
plt.title('Red')

plt.subplot(144)
plt.imshow(a, cmap='gray')
plt.title('Alpha ')

plt.show()