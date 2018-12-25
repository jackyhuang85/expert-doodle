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

    blurred = blur(image, kernel=(7, 7), sigma=1)
    plt.figure()
    plt.imshow(blurred)

    plt.show()
