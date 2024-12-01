import cv2
import matplotlib.pyplot as plt

img = cv2.imread('image/kangaroo.jpg', cv2.IMREAD_UNCHANGED)
print(img.shape)
b, g, r = cv2.split(img)

# Create a green dot
imggreen = img.copy()
imggreen[80:120, 80:120, 0] = 0  # Blue channel
imggreen[80:120, 80:120, 1] = 255  # Green channel
imggreen[80:120, 80:120, 2] = 0  # Red channel

imggreen = cv2.cvtColor(imggreen, cv2.COLOR_BGR2RGBA)  # Ensure RGBA format for proper display
cv2.imwrite('image/kangaroo_green.jpg',imggreen)

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
plt.imshow(imggreen)
plt.title('Image with Green Dot')

plt.show()
