import pathlib
import cv2

from process_and_save_result import image_process_and_save
from save_image import image_save


# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html


def image_processing_filtering_blur(
        main_output_path,
        folder_index,
        sizes,
        image
):

    print("*****************************************************")
    print("Starting: image_processing_filtering_blur()")
    print("*****************************************************")

    # Путь к сохраняемым файлам
    output_path = main_output_path + "/" + str(folder_index).zfill(4) + "_filtering_blur"

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
            "_blur_size_" + str(size).zfill(4),
            cv2.blur,
            image,
            (size, size)
        )

        image_index += 1

    print()
    print()
    print("*****************************************************")
    print("*****************************************************")
    print()
    print()
