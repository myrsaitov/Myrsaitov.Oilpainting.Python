import pathlib

import cv2


# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
from image_save import image_save


def filtering_image_processing_gaussian_blur(
        main_output_path,
        image
):

    # Путь к сохраняемым файлам
    output_path = main_output_path + "/filtering_gaussian_blur"

    # Создает папку, если ее не существует
    pathlib\
        .Path(output_path)\
        .mkdir(parents=True, exist_ok=True)


    # Начальный индекс файла
    image_index = 1

    # Сохраняет оригинал
    image_save(
        output_path,
        image_index,
        "_original",
        image
    )
    image_index += 1

    # Применяет фильтр
    for size in [5]:

        image_save(
            output_path,
            image_index,
            "_size_" + str(size).zfill(4),
            cv2.GaussianBlur(
                image,
                (size, size),
                cv2.BORDER_DEFAULT
            )
        )

        image_index += 1

