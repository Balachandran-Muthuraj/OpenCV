# Load image with gaussian noise.
import cv2
from matplotlib import pyplot as plt

image1 = cv2.imread('images/mri-skull-20-percent-gaussian-noise.jpg')
image2 = cv2.imread('images/mri-skull-40-percent-gaussian-noise.jpg')


# diameter of the pixel neighborhood used during filtering.
dia = 20

# Larger the value the distant colours will be mixed together
# to produce areas of semi equal colors.
sigmaColor = 200

# Larger the value more the influence of the farther placed pixels
# as long as their colors are close enough.
sigmaSpace = 100

# Apply bilateralFilter.
dst1 = cv2.bilateralFilter(image1, dia, sigmaColor, sigmaSpace)
dst2 = cv2.bilateralFilter(image2, dia, sigmaColor, sigmaSpace)

plt.figure(figsize = (20, 12))
plt.subplot(221); plt.axis('off'); plt.imshow(image1[:,:,::-1]); plt.title("Image with 20% gaussian noise")
plt.subplot(222); plt.axis('off'); plt.imshow(dst1[:,:,::-1]);   plt.title("Bilateral blur Result")
plt.subplot(223); plt.axis('off'); plt.imshow(image2[:,:,::-1]); plt.title("Image with 40% gaussian noise")
plt.subplot(224); plt.axis('off'); plt.imshow(dst2[:,:,::-1]);   plt.title("Bilateral blur Result")
plt.show()