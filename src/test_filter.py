import matplotlib.pyplot as plt
from skimage.io import imread, imsave
from filters import *

if __name__ == "__main__":
    filename = '../example/none.jpg'
    image = imread(filename)

    plt.figure()
    plt.imshow(image)

    gray = gray_scale(image)
    plt.figure()
    plt.imshow(gray, cmap='gray')
    imsave('../example/gray.jpg', gray)

    freq = 11
    blurred = blur(image, kernel=(freq*4+1, freq*4+1), sigma=freq)
    plt.figure()
    plt.imshow(blurred)
    imsave('../example/blur.jpg', blurred)

    sharp = sharpen(image, rate=0.5, kernel=(freq*4+1, freq*4+1), sigma=freq)
    plt.figure()
    plt.imshow(sharp)
    imsave('../example/sharpen.jpg', sharp)

    inverted = invert(image)
    plt.figure()
    plt.imshow(inverted)
    imsave('../example/invert.jpg', inverted)

    powered = power(image)
    plt.figure()
    plt.imshow(powered)
    imsave('../example/power.jpg', powered)

    enhanced = enhance(image, contrast=1.5, brightness=50)
    plt.figure()
    plt.imshow(enhanced)
    imsave('../example/enhanced.jpg', enhanced)

    grad = sobel(image)
    plt.figure()
    plt.imshow(grad, cmap='gray')
    imsave('../example/sobel.jpg', grad)

    edge = edge_detect(image)
    plt.figure()
    plt.imshow(edge, cmap='gray')
    imsave('../example/edge.jpg', edge)

    plt.show()
