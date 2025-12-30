import cv2
import matplotlib.pyplot as plt
import numpy as np

# Read the image in color
image1 = cv2.imread('img/1985.png', cv2.IMREAD_COLOR)
image4 = cv2.imread('img/2011.png', cv2.IMREAD_COLOR)

b1, g1, r1 = cv2.split(image1)
b4, g4, r4 = cv2.split(image4)

# Show the channels.
plt.figure(figsize = [20, 15])
plt.subplot(331); plt.imshow(image1[:, :, ::-1]); plt.title('Original 1985')
plt.subplot(332); plt.imshow(image4[:, :, ::-1]); plt.title('Original 2011')

plt.subplot(334); plt.imshow(r1); plt.title('Red Channel - 1985')
plt.subplot(335); plt.imshow(g1); plt.title('Green Channel - 1985')
plt.subplot(336); plt.imshow(b1); plt.title('Blue Channel - 1985')

plt.subplot(337); plt.imshow(r4); plt.title('Red Channel - 2011')
plt.subplot(338); plt.imshow(g4); plt.title('Green Channel - 2011')
plt.subplot(339); plt.imshow(b4); plt.title('Blue Channel - 2011')

plt.show()


def draw_image_histogram_bgr(image, title='', yscale='linear'):
    """Utility to plot bgr histograms for all color channels independently."""
    histB = cv2.calcHist([image], [0], None, [256], [0, 255])
    histG = cv2.calcHist([image], [1], None, [256], [0, 255])
    histR = cv2.calcHist([image], [2], None, [256], [0, 255])

    # Plot the histograms for each channel.
    fig = plt.figure(figsize=[20, 5])
    fig.suptitle(title)

    ax = fig.add_subplot(1, 3, 1)
    ax.set_yscale(yscale)
    plt.plot(histB, color='b', label='Blue')
    ax.grid()
    ax.legend()

    ax = fig.add_subplot(1, 3, 2)
    ax.set_yscale(yscale)
    plt.plot(histG, color='g', label='Green')
    ax.grid()
    ax.legend()

    ax = fig.add_subplot(1, 3, 3)
    ax.set_yscale(yscale)
    plt.plot(histR, color='r', label='Red')
    ax.grid()
    ax.legend()

    plt.show()