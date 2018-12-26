import matplotlib.pyplot as plt
from skimage.io import imread
from filters import *

if __name__ == "__main__":
    filename = '../data/image.jpg'
    image = imread(filename)

    plt.figure()
    plt.imshow(image)

    gray = gray_scale(image)
    plt.figure()
    plt.imshow(gray)

    freq = 3

    blurred = blur(image, kernel=(freq*4+1, freq*4+1), sigma=0.5)
    plt.figure()
    plt.imshow(blurred)

    sharp = sharpen(image, rate=0.5, kernel=(freq*4+1, freq*4+1), sigma=0.5)
    plt.figure()
    plt.imshow(sharp)

    inverted = invert(image)
    plt.figure()
    plt.imshow(inverted)

    plt.show()
