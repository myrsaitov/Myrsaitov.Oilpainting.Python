import pathlib
import cv2

from image_process_and_save import image_process_and_save
from image_save import image_save


# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html


def filtering_image_processing_median_blur(
        main_output_path,
        folder_index,
        sizes,
        image
):

    print("*****************************************************")
    print("*****************************************************")
    print("Starting: filtering_image_processing_median_blur()")

    # Путь к сохраняемым файлам
    output_path = main_output_path + "/" + str(folder_index).zfill(4) + "_filtering_median_blur"

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
    for size in sizes:

        image_process_and_save(
            output_path,
            image_index,
            "_median_blur_size_" + str(size).zfill(4),
            cv2.medianBlur,
            image,
            size
        )

        image_index += 1

    print()
    print()
    print("*****************************************************")
    print("*****************************************************")
    print()
    print()
