import numpy as np
import gputools
from scipy.ndimage import filters
import time

def gray_scale(image):
    gray = 0.299 * image[:, :, 0] + 0.587 * \
        image[:, :, 1] + 0.114 * image[:, :, 2]
    return np.repeat(gray[:, :, np.newaxis], 3, axis=2).astype('int')


def blur(image, kernel=(3, 3), sigma=1.):
    g = _gaussian(kernel=(3, 3), sigma=1.)
    # g = gauss2D(shape=kernel, sigma=sigma)
    tic = time.clock()
    blur_img = _filter(image, g)
    toc = time.clock()
    print('applying gaussian filter used: %f sec' % (toc-tic))
    return blur_img


def sharpen(image, rate=0.5, kernel=(3, 3), sigma=1.):
    blurred = blur(image, kernel=kernel, sigma=sigma)
    sharp = np.clip((1+rate)*image - rate*blurred, 0, 255).astype('int')
    return sharp


def invert(image):
    return 255-image


def power(image, rate=0.5):
    powered = image**rate
    powered = powered * (255/powered.max())
    return powered.astype('int')


def enhance(image, contrast=0.1, brightness=0):
    enhanced = np.zeros_like(image)
    enhanced[:, :, 0] = contrast*(image[:, :, 0]-128) + 128 + brightness
    enhanced[:, :, 1] = contrast*(image[:, :, 1]-128) + 128 + brightness
    enhanced[:, :, 2] = contrast*(image[:, :, 2]-128) + 128 + brightness
    enhanced = np.clip(enhanced, 0, 255).astype('int')
    return enhanced


def _filter(image, filter):
    output = np.zeros_like(image)
    output[:, :, 0] = gputools.convolve(image[:, :, 0], filter)
    output[:, :, 1] = gputools.convolve(image[:, :, 1], filter)
    output[:, :, 2] = gputools.convolve(image[:, :, 2], filter)

    return output


def _gaussian(kernel=(3, 3), sigma=1.):
    x, y = np.meshgrid(np.linspace(-(kernel[0]//2), (kernel[0]//2)),
                       np.linspace(-(kernel[1]//2), (kernel[1]//2)))
    filter = np.exp(-(x**2+y**2)/(2*sigma**2))
    return filter / filter.sum()


def gauss2D(shape=(3, 3), sigma=0.5):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m, n = [(ss-1.)/2. for ss in shape]
    y, x = np.ogrid[-m:m+1, -n:n+1]
    h = np.exp(-(x*x + y*y) / (2.*sigma*sigma))
    h[h < np.finfo(h.dtype).eps*h.max()] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h
