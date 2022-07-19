import pathlib

import numpy as np
import cv2
from image_save import image_save


# https://neptune.ai/blog/image-processing-python
# https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/
# https://appdividend.com/2022/03/15/python-cv2-dilate/


def main(
        main_output_path,
        size,
        image):

    # Путь к сохраняемым файлам
    output_path = main_output_path + "/morphological_size_" + str(size).zfill(4)

    # Создает папку, если ее не существует
    pathlib\
        .Path(output_path)\
        .mkdir(parents=True, exist_ok=True)

    # Начальный индекс файла
    image_index = 1

    # Настройки преобразования
    kernel = np.ones(
        (size, size),
        'uint8')

    # Выполняет "Dilate"
    for iterations in reversed(range(1, 10)):

        image_save(
            output_path,
            image_index,
            "_dilated__iterations_" + str(iterations).zfill(4),
            cv2.dilate(
                image,
                kernel,
                iterations=iterations))

        image_index += 1

    # Сохраняет оригинал
    image_save(
        output_path,
        image_index,
        "_original",
        image)

    image_index += 1

    # Выполняет "Erode"
    for iterations in range(1, 10):
        image_save(
            output_path,
            image_index,
            "_eroded__iterations_" + str(iterations).zfill(4),
            cv2.erode(
                image,
                kernel,
                iterations=iterations))

        image_index += 1
