import pathlib

import cv2


# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
from image_save import image_save


# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html

def filtering_image_processing_bilateral(
        main_output_path,
        image
):

    # Путь к сохраняемым файлам
    output_path = main_output_path + "/filtering_bilateral"

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
    for size in [5,10,15,20,25,30,35,40,45,50]:

        image_save(
            output_path,
            image_index,
            "_bilateral_size_" + str(size).zfill(4),
            cv2.bilateralFilter(
                image,
                size,
                75,
                75)
        )

        image_index += 1

