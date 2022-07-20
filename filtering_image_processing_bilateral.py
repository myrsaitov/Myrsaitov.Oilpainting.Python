import pathlib
import cv2


# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
from image_save import image_save


# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
# http://people.csail.mit.edu/sparis/bf_course/

def filtering_image_processing_bilateral(
        main_output_path,
        sizes,
        image
):

    print("*****************************************************")
    print("*****************************************************")
    print("Starting: filtering_image_processing_bilateral()")

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
    for size in sizes:

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

    print("*****************************************************")
    print("*****************************************************")
    print()
    print()
