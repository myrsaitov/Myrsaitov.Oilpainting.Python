import numpy as np
import cv2


def image_dilate(image):
    kernel = np.ones((5, 5), 'uint8')

    return cv2.dilate(image, kernel, iterations=1)
