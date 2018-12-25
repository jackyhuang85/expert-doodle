import numpy as np
from scipy.ndimage import filters


def gray_scale(image):
    gray = 0.299 * image[:, :, 0] + 0.587 * \
        image[:, :, 1] + 0.114 * image[:, :, 2]
    return np.repeat(gray[:, :, np.newaxis], 3, axis=2).astype('int')


def blur(image, kernel=(3, 3), sigma=1.):
    g = _gaussian(kernel=kernel, sigma=sigma)
    blur = _filter(image, g)
    return blur


# def sharpen(image, a=1, b=1, sigma=1.):
#     sharp = np.clip(a * image - b * blur, 0, 255)
#     return sharp


def _filter(image, filter):
    output = np.zeros_like(image)
    h, w, c = image.shape
    k1, k2 = filter.shape
    padded = np.pad(image,
                    ((k1//2, k1//2),
                     (k2//2, k2//2),
                     (0, 0)),
                    mode='symmetric')
    for k in range(c):
        output[:, :, k] = filters.convolve(image[:, :, k], filter)

    return output


def _gaussian(kernel=(3, 3), sigma=1.):
    x, y = np.meshgrid(np.linspace(-(kernel[0]//2), (kernel[0]//2)),
                       np.linspace(-(kernel[1]//2), (kernel[1]//2)))
    filter = np.exp(-(x**2+y**2)/(2*sigma**2))
    return filter / filter.sum()
