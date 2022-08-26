import inspect
import os
import pathlib
import numpy as np
import cv2


# https://neptune.ai/blog/image-processing-python
# https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/
# https://appdividend.com/2022/03/15/python-cv2-dilate/

def morphological_processing_wrapper(
    output_path_root,
    image
):
    image_processing_morphological(
        output_path_root,
        5,  # Здесь нет диапазона, указывается только число
        image
    )

def image_processing_morphological(
    output_path_root,
    size,
    image
):

    print("*****************************************************")
    print("Starting: ", inspect.currentframe().f_code.co_name)
    print("*****************************************************")

    # Путь к сохраняемым файлам
    output_path = output_path_root + "/morphological"

    # Если папка существует, то действия не требуются
    if os.path.exists(output_path):
        print("The folder exists! The old version remains!")
        return
    else:
        # Создает папку, если ее не существует
        pathlib \
            .Path(output_path) \
            .mkdir(parents=True, exist_ok=True)

    # Начальный индекс файла
    image_index = 1

    # Настройки преобразования
    kernel = np.ones(
        (size, size),
        'uint8')


    ##############################################
    # Выполняет "Dilate"
    ##############################################

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


    ##############################################
    # Сохраняет оригинальный файл
    ##############################################

    # Добавляет индекс в начале файла для удобства сортировки по имени
    original_file_path = output_path + "/" + str(image_index).zfill(4) + "_original.jpg"

    # Если файл существует, то он не перезаписывается
    if os.path.exists(original_file_path):
        print("File exists! The old version remains!")
    else:
        cv2.imwrite(original_file_path, image)

    image_index += 1


    ##############################################
    # Выполняет "Erode"
    ##############################################

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


# Если файл с таким именем существует,
# то ничего не происходит, иначе проводится
# обработка изображения и записывается в файл.
# Это нужно, чтобы пропускать обработку,
# если файл уже имеется.
def image_process_and_save(
    path,
    index,
    suffix,
    image_processing_func,      # Функция для преобразования изображения
    *function_arguments,        # Позиционные аргументы функции
    **named_function_arguments  # Именованные аргументы функции, например: iterations=5
):                              # https://tproger.ru/translations/python-args-and-kwargs/
                                # https://python.ivan-shamaev.ru/python-3-functions-value-arguments-call-variables-arrays/

    # Добавляет индекс в начале файла для удобства сортировки по имени
    file_path = path + "/" + str(index).zfill(4) + suffix + ".jpg"

    # Если файл существует, то он не перезаписывается
    if os.path.exists(file_path):
        print("File exists! The old version remains!")
        return

    # Выполнение преобразования с переданной функцией и аргументами к ней
    image = image_processing_func(*function_arguments, **named_function_arguments)

    # Запись файла
    cv2.imwrite(file_path, image)

    print("Saved: ", file_path)