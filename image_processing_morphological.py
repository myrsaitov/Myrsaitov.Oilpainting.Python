import pathlib
import numpy as np
import cv2

from process_and_save_result import image_process_and_save
from save_image import image_save


# https://neptune.ai/blog/image-processing-python
# https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/
# https://appdividend.com/2022/03/15/python-cv2-dilate/


def image_processing_morphological(
        main_output_path,
        folder_index,
        size,
        image
):

    print("*****************************************************")
    print("Starting: image_processing_morphological()")
    print("*****************************************************")

    # Путь к сохраняемым файлам
    output_path = main_output_path + "/" + str(folder_index).zfill(4) + "_morphological"

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

        image_process_and_save(
            output_path,
            image_index,
            "_dilated__size" + str(size).zfill(4) + "_iterations_" + str(iterations).zfill(4),
            cv2.dilate,
            image,
            kernel,
            iterations=iterations
        )

        image_index += 1

    # Сохраняет оригинал
    image_save(
        output_path,
        image_index,
        "_original",
        image
    )

    image_index += 1

    # Выполняет "Erode"
    for iterations in range(1, 10):
        image_process_and_save(
            output_path,
            image_index,
            "_eroded__size" + str(size).zfill(4) + "_iterations_" + str(iterations).zfill(4),
            cv2.erode,
            image,
            kernel,
            iterations=iterations
        )

        image_index += 1

    print()
    print()
    print("*****************************************************")
    print("*****************************************************")
    print()
    print()
