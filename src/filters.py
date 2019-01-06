import numpy as np
import gputools
import time


def gray_scale(image):
    gray = 0.299 * image[:, :, 0] + 0.587 * \
        image[:, :, 1] + 0.114 * image[:, :, 2]
    return gray.astype('uint8')


def blur(image, kernel=(3, 3), sigma=1.):
    g = gauss2D(shape=kernel, sigma=sigma)
    blur_img = _filter3d(image, g)
    return blur_img.astype('uint8')


def sharpen(image, rate=0.5, kernel=(3, 3), sigma=1.):
    blurred = blur(image, kernel=kernel, sigma=sigma)
    sharp = np.clip((1+rate)*image - rate*blurred, 0, 255).astype('int')
    return sharp.astype('uint8')


def invert(image):
    return 255-image


def power(image, rate=0.5):
    powered = image**rate
    powered = powered * (255/powered.max())
    return powered.astype('uint8')


def enhance(image, contrast=0.1, brightness=0):
    # image = gray_scale(image).astype('float')
    image = image.astype('float')
    enhanced = contrast * (image - 128) + 128 + brightness
    # enhanced = np.zeros_like(image)
    # enhanced[:, :, 0] = contrast*(image[:, :, 0]-128) + 128 + brightness
    # enhanced[:, :, 1] = contrast*(image[:, :, 1]-128) + 128 + brightness
    # enhanced[:, :, 2] = contrast*(image[:, :, 2]-128) + 128 + brightness
    enhanced = np.clip(enhanced, 0, 255)
    return enhanced.astype('uint8')


def sobel(image, mode=0):
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
    return grad.astype('uint8')


def edge_detect(image, thin=True):
    blurred = blur(image, sigma=1.5)
    gx = sobel(blurred, mode=0).astype('float')
    gy = sobel(blurred, mode=1).astype('float')
    mag = np.sqrt((gx)+(gy**2))
    if thin is True:
        gxx = sobel(gx, mode=0)
        gyy = sobel(gy, mode=1)
        gxy = sobel(gx, mode=1)
        gyx = sobel(gy, mode=0)
        mag[gxx < 0] = 0
        mag[gyy < 0] = 0
        mag[gxy < 0] = 0
        mag[gyx < 0] = 0
    return mag.astype('uint8')

def _filter2d(image, filter):
    return gputools.convolve(image, filter)


def _filter3d(image, filter):
    output = np.zeros_like(image)
    output[:, :, 0] = gputools.convolve(image[:, :, 0], filter)
    output[:, :, 1] = gputools.convolve(image[:, :, 1], filter)
    output[:, :, 2] = gputools.convolve(image[:, :, 2], filter)

    return output


def gauss2D(shape=(3, 3), sigma=0.5):
    m, n = [(ss-1)/2 for ss in shape]
    y, x = np.ogrid[-m:m+1, -n:n+1]
    h = np.exp(-(x*x + y*y) / (2.*sigma*sigma))
    h[h < np.finfo(h.dtype).eps*h.max()] = 0
    return h / h.sum() if h.sum() != 0 else h
