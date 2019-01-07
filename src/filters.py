import numpy as np
import gputools
import time


def gray_scale(image, **param):
    gray = 0.299 * image[:, :, 0] + 0.587 * \
        image[:, :, 1] + 0.114 * image[:, :, 2]
    return gray


def blur(image, **param):
    kernel = param.get('kernel', (3, 3))
    sigma = param.get('sigma', 3)
    g = gauss2D(shape=kernel, sigma=sigma)
    blur_img = _filter3d(image, g)
    return blur_img


def sharpen(image, **param):
    rate = param.get('rate', 1.5)
    kernel = param.get('kernel', (3, 3))
    sigma = param.get('sigma', 3)
    blurred = blur(image, kernel=kernel, sigma=sigma)
    sharp = np.clip((1+rate)*image - rate*blurred, 0, 255)
    return sharp


def invert(image, **param):
    return 255-image


def power(image, **param):
    rate = param.get('rate', 0.5)
    powered = image**(2-rate)
    powered = powered * (255/powered.max())
    return powered


def enhance(image, **param):
    contrast = param.get('contrast', 0.1)
    brightness = param.get('brightness', 0.1)
    image = image.astype('float')
    enhanced = contrast * (image - 128) + 128 + brightness
    enhanced = np.clip(enhanced, 0, 255)
    return enhanced


def sobel(image, **param):
    mode = param.get('mode', 0)
    if len(image.shape) == 3:
        image = gray_scale(image)
    if mode == 0:
        f = np.array([[-1, 0, 1],
                      [-1, 0, 1],
                      [-1, 0, 1]])
    else:
        f = np.array([[1, 2, 1],
                      [0, 0, 0],
                      [-1, -2, -1]])
    grad = _filter2d(image, f)
    return grad


def edge_detect(image, **param):
    blurred = blur(image, sigma=1.5)
    gx = sobel(blurred, mode=0)
    gy = sobel(blurred, mode=1)
    mag = np.sqrt((gx**2)+(gy**2))
    mag = np.clip(mag, 0, 255)
    return mag


def _filter2d(image, filter):
    return gputools.convolve(image, filter)


def _filter3d(image, filter):
    output = np.zeros_like(image)
    output[:, :, 0] = gputools.convolve(image[:, :, 0], filter)
    output[:, :, 1] = gputools.convolve(image[:, :, 1], filter)
    output[:, :, 2] = gputools.convolve(image[:, :, 2], filter)

    return output


def gauss2D(shape=(3, 3), sigma=3):
    m, n = [(ss-1)/2 for ss in shape]
    y, x = np.ogrid[-m:m+1, -n:n+1]
    h = np.exp(-(x*x + y*y) / (2.*sigma*sigma))
    if h.sum() != 0:
        h[h < np.finfo(h.dtype).eps*h.max()] = 0
        return h/h.sum()
    return h
