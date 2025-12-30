import cv2
import numpy as np

# Open video file
cap = cv2.VideoCapture("lane1-straight.mp4")

if not cap.isOpened():
    print("Error: Cannot open video file")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Canny edge detection
    edges = cv2.Canny(blur, 50, 150)

    # 4. Region of Interest (ROI)
    height, width = edges.shape
    mask = np.zeros_like(edges)

    polygon = np.array([[
        (0, height),
        (width, height),
        (width // 2, height // 2)
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    roi = cv2.bitwise_and(edges, mask)

    # 5. Hough Line Transform
    lines = cv2.HoughLinesP(
        roi,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=40,
        maxLineGap=5
    )

    # 6. Draw lines
    line_img = frame.copy()
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # 7. Display
    cv2.imshow("Edges", edges)
    cv2.imshow("Lane Detection", line_img)

    # Press 'q' to exit
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
