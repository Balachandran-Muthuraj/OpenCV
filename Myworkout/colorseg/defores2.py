import cv2
import matplotlib.pyplot as plt

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
image1 = cv2.imread('img/1985.png', cv2.IMREAD_COLOR)
image4 = cv2.imread('img/2011.png', cv2.IMREAD_COLOR)
draw_image_histogram_bgr(image1, '1985')
draw_image_histogram_bgr(image4, '2011')

draw_image_histogram_bgr(image1,'1985 - Log Plot', 'log')
draw_image_histogram_bgr(image4,'2011 - Log Plot', 'log')