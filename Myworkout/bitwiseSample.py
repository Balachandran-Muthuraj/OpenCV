import cv2
import matplotlib.pyplot as plt

imgrect=cv2.imread('img/rectangle.jpg', cv2.IMREAD_GRAYSCALE)
imgrcircle=cv2.imread('img/circle.jpg', cv2.IMREAD_GRAYSCALE)


imgbwand=cv2.bitwise_xor(imgrcircle,imgrect,mask=None)

# Plot the images
plt.figure(figsize=(18, 5))
plt.subplot(131)
plt.imshow(imgrect, cmap='gray')
plt.title('Rectangle')

plt.subplot(132)
plt.imshow(imgrcircle, cmap='gray')
plt.title('Circle')

plt.subplot(133)
plt.imshow(imgbwand, cmap='gray')
plt.title('AND')
print(imgrect.shape)
print(imgrcircle.shape)

plt.show()