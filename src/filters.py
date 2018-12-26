import numpy as np
from scipy.ndimage import filters


def gray_scale(image):
    gray = 0.299 * image[:, :, 0] + 0.587 * \
        image[:, :, 1] + 0.114 * image[:, :, 2]
    return np.repeat(gray[:, :, np.newaxis], 3, axis=2).astype('int')


def blur(image, kernel=(3, 3), sigma=1.):
    g = _gaussian(kernel=kernel, sigma=sigma)
    # g = gauss2D(shape=kernel, sigma=sigma)
    blur = _filter(image, g)
    return blur


def sharpen(image, rate=0.5, kernel=(3, 3), sigma=1.):
    blurred = blur(image, kernel=kernel, sigma=sigma)
    sharp = np.clip((1+rate)*image - rate*blurred, 0, 255).astype('int')
    return sharp


def invert(image):
    return 255-image


def _filter(image, filter):
    output = np.zeros_like(image)
    h, w, c = image.shape
    for k in range(c):
        output[:, :, k] = filters.convolve(image[:, :, k], filter)

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
