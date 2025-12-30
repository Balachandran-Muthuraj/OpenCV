import  numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
def detect_green_BGR(img):
    """Detect and return a mask for the green area of an image using BGR segmentation."""
    lower_BGR_values = np.array([0, 50, 0], dtype='uint8')
    upper_BGR_values = np.array([255, 100, 255], dtype='uint8')

    # Create a mask using the lower and upper range.
    mask_BGR = cv2.inRange(img, lower_BGR_values, upper_BGR_values)

    return mask_BGR
def percent_forest(gray_img):
    """Return the percentage of the image detected to be forested."""
    c = cv2.countNonZero(gray_img)

    # Finding number of pixels in image to find percentage.
    t = gray_img.shape[0] * gray_img.shape[1]

    # Rounding off to 2 decimal place.
    return round((c / t) * 100, 2)


image_files = glob.glob("img/*.png")
image_files.sort()
for image_file in image_files:
    image = cv2.imread(image_file)

    segmented_green = detect_green_BGR(image)
    green_ratio = percent_forest(segmented_green)

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(image[:, :, ::-1])
    ax.set_title('Original - ' + image_file)

    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(segmented_green, cmap='gray')
    ax.set_title('Color Segmented in Green Channel: ' + str(green_ratio) + '%')

    plt.show()