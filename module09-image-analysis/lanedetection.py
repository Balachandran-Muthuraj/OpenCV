import cv2
import numpy as np

# 1. Read image
img = cv2.imread("test_img1.jpg")

if img is None:
    print("Error: Image not found")
    exit()

# 2. Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. Gaussian blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 4. Canny edge detection
edges = cv2.Canny(blur, 50, 150)

# 5. Region of Interest (ROI)
height, width = edges.shape
mask = np.zeros_like(edges)

polygon = np.array([
    [(0, height),
     (width, height),
     (width // 2, height // 2)]
], np.int32)

cv2.fillPoly(mask, polygon, 255)
roi = cv2.bitwise_and(edges, mask)

# 6. Hough Line Transform
lines = cv2.HoughLinesP(
    roi,
    rho=1,
    theta=np.pi / 180,
    threshold=100,
    minLineLength=40,
    maxLineGap=5
)

# 7. Draw lines
line_img = img.copy()

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 3)

# 8. Show result
cv2.imshow("Original Image", img)
cv2.imshow("Edges", edges)
cv2.imshow("Lane Detection", line_img)

# 9. Wait and destroy
cv2.waitKey(0)
cv2.destroyAllWindows()
