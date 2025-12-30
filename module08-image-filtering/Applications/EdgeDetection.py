import cv2
import plt

img = cv2.imread('visuals/')

# Convert to grayscale.
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(img_gray, threshold1 = 180, threshold2 = 200)

plt.figure(figsize = (20,10))
plt.subplot(131); plt.axis("off"); plt.imshow(img[:,:,::-1]); plt.title('Original')
plt.subplot(132); plt.axis("off"); plt.imshow(img_gray);      plt.title('Grayscale')
plt.subplot(133); plt.axis("off"); plt.imshow(edges);         plt.title('Canny Edge Map');