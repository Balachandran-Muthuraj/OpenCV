import cv2
import matplotlib.pyplot as plt

# Load image in grayscale
img_gray = cv2.imread('image/kangaroo.jpg', cv2.IMREAD_GRAYSCALE)

img = cv2.imread('image/kangaroo.jpg', cv2.IMREAD_UNCHANGED)

print(img_gray.shape)

b, g, r = cv2.split(img)

# Apply thresholding
ret1, thresh1 = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
ret2, thresh2 = cv2.threshold(img_gray, 230, 255, cv2.THRESH_BINARY)
ret3, thresh3 = cv2.threshold(img_gray, 230, 200, cv2.THRESH_BINARY)

# Bitwise OR (Combining binary images)
ImgFullTransparent = cv2.bitwise_not(thresh2)
ImgSemiTransparent = cv2.bitwise_not(thresh3)

Full=[b,g,r,ImgFullTransparent]
imgFull=cv2.merge(Full)
imgFull=cv2.cvtColor(imgFull,cv2.COLOR_BGRA2RGBA)
Semi=[b,g,r,ImgSemiTransparent]
imgSemi=cv2.merge(Semi)
imgSemi=cv2.cvtColor(imgSemi,cv2.COLOR_BGRA2RGBA)
print(imgSemi.shape)
print(imgFull.shape)
# Plot images
plt.figure(figsize=(15, 3))

plt.subplot(141)
plt.imshow(img_gray, cmap='gray')
plt.title('Gray')

plt.subplot(142)
plt.imshow(thresh1, cmap='gray')
plt.title('T1 (Threshold 150)')

plt.subplot(143)
plt.imshow(thresh2, cmap='gray')
plt.title('T2 (Threshold 230, Max 255)')

plt.subplot(144)
plt.imshow(thresh3, cmap='gray')
plt.title('T3 (Threshold 230, Max 200)')

plt.figure(figsize=(15, 7))

plt.subplot(245)
plt.imshow(ImgFullTransparent, cmap='gray')
plt.title('Full OR Combination')

plt.subplot(246)
plt.imshow(ImgSemiTransparent, cmap='gray')
plt.title('Semi OR Combination')

plt.subplot(247)
plt.imshow(imgSemi)
plt.title('Semi ')

plt.subplot(248)
plt.imshow(imgFull)
plt.title('Full')

plt.show()
