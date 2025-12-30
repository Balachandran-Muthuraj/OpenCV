# Load images.
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('images/515.jpg')
img2 = cv2.imread('images/girl-skin.jpg')

# Apply Gaussian filter for comparison.
img1_gaussian = cv2.GaussianBlur(img1, (5,5), cv2.BORDER_DEFAULT)
img2_gaussian = cv2.GaussianBlur(img2, (5,5), cv2.BORDER_DEFAULT)

# Apply bilateralFilter.
img1_bilateral = cv2.bilateralFilter(img1, d = 25, sigmaColor = 90, sigmaSpace = 40)
img2_bilateral = cv2.bilateralFilter(img2, d = 30, sigmaColor = 65, sigmaSpace = 15)

# Display.
plt.figure(figsize = (18, 15))
plt.subplot(321); plt.axis('off'); plt.imshow(img1[:,:,::-1]);           plt.title('Image1')
plt.subplot(322); plt.axis('off'); plt.imshow(img2[:,:,::-1]);           plt.title('Image2')
plt.subplot(323); plt.axis('off'); plt.imshow(img1_gaussian[:,:,::-1]);  plt.title('Gaussian Filter')
plt.subplot(324); plt.axis('off'); plt.imshow(img2_gaussian[:,:,::-1]);  plt.title('Gaussian Filter')
plt.subplot(325); plt.axis('off'); plt.imshow(img1_bilateral[:,:,::-1]); plt.title('Bilateral Filter')
plt.subplot(326); plt.axis('off'); plt.imshow(img2_bilateral[:,:,::-1]); plt.title('Bilateral Filter')
plt.show()