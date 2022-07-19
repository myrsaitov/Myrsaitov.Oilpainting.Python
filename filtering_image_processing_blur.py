import pathlib

import cv2


# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
from image_save import image_save


def filtering_image_processing_blur(
        main_output_path,
        image
):

    # Путь к сохраняемым файлам
    output_path = main_output_path + "/filtering_blur"

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
    for size in range(1, 20):

        image_save(
            output_path,
            image_index,
            "_size_" + str(size).zfill(4),
            cv2.blur(
                image,
                (size, size)
            )
        )

        image_index += 1

