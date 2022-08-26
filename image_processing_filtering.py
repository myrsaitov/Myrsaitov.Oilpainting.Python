import inspect
import os
import pathlib
import cv2

from to_snake_case import to_snake_case


# Filtering Image Processing: Blur
# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html

# Filtering Image Processing: Gaussian Blur
# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
# https://www.tutorialkart.com/opencv/python/opencv-python-gaussian-image-smoothing/

# Filtering Image Processing: Median Blur
# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html

# Filtering Image Processing: Bilateral
# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
# https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
# http://people.csail.mit.edu/sparis/bf_course/
# Можно использовать для проверки, получился ли передний план (все остальное блекнет)

def filter_processing_wrapper(
    output_path_root,
    image
):

    # Filtering Image Processing: Blur
    for size in range(1, 20):
        image_processing_filtering(
            "Filtering: Blur",
            output_path_root,
            cv2.blur,
            image,
            (size, size)
        )

    # Filtering Image Processing: Gaussian Blur
    # Только нечетные значения size!
    for size in range(1, 50, 4):
        image_processing_filtering(
            "Filtering: Gaussian Blur",
            output_path_root,
            cv2.GaussianBlur,
            image,
            (size, size),
            cv2.BORDER_DEFAULT
        )

    # Filtering Image Processing: Median Blur
    # Только нечетные значения size!
    for size in range(1, 50, 4):
        image_processing_filtering(
            "Filtering: Median Blur",
            output_path_root,
            cv2.medianBlur,
            image,
            size
        )

    # Filtering Image Processing: Bilateral
    # Можно использовать для проверки, получился ли передний план (все остальное блекнет)
    for size in [5, 25, 50, 100]:  # , 200, 300, 1000],:
        image_processing_filtering(
            "Filtering: Bilateral Blur",
            output_path_root,
            cv2.bilateralFilter,
            image,
            size,
            75,
            75
        )



# Процедура, реализующая фильтр
def image_processing_filtering(
        title,
        output_path_root,
        image_processing_func,  # Функция для преобразования изображения
        *argv,  # Позиционные аргументы функции
        **kwargs  # Именованные аргументы функции, например: iterations=5
):  # https://tproger.ru/translations/python-args-and-kwargs/
    # https://python.ivan-shamaev.ru/python-3-functions-value-arguments-call-variables-arrays/

    print("*****************************************************")
    print("Starting: ", inspect.currentframe().f_code.co_name, ": ", title)
    print("*****************************************************")

    ##############################################
    # Суффикс сохраняемого файла
    ##############################################

    # Второй аргумент по счету связан с size
    arg = argv[1]

    # Если это массив?
    if hasattr(arg, "__len__"):
        # Берем первый элемент списка, а если нет списка, то просто этот элемент
        suffix = "_size_" + str(arg[0]).zfill(4)
    else:
        suffix = "_size_" + str(arg).zfill(4)

    ##############################################
    # Папка с результатами
    ##############################################

    # Путь к сохраняемым файлам
    output_path = output_path_root + "/" + to_snake_case(title)

    # Создает папку, если ее не существует
    pathlib \
        .Path(output_path) \
        .mkdir(parents=True, exist_ok=True)

    ##############################################
    # Сохраняет оригинал
    ##############################################

    original_image_path = output_path + "/__original_image.jpg"
    if not os.path.exists(original_image_path):
        # В массиве аргументов первым идет "image": argv[0]
        cv2.imwrite(original_image_path, argv[0])

    ##############################################
    # Сохраняет результат
    ##############################################

    # Полное имя файла
    file_path = output_path + "/" + to_snake_case(title) + suffix + ".jpg"

    if os.path.exists(file_path):
        print("File exists! The old version remains!")
        return

    try:


        # Выполнение преобразования с переданной функцией и аргументами к ней
        processed_image = image_processing_func(*argv, **kwargs)

        # Запись файла
        cv2.imwrite(file_path, processed_image)

        print("Saved: ", file_path)

    except Exception:
        print("Error in image processing, ", suffix, " Exception:", Exception)

    # Возвращает результат преобразования
    return processed_image
