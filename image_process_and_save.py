import cv2
import os.path


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
):                                  # https://tproger.ru/translations/python-args-and-kwargs/
                                    # https://python.ivan-shamaev.ru/python-3-functions-value-arguments-call-variables-arrays/

    # Добавляет индекс в начале файла для удобства сортировки по имени
    file_path = path + "/" + str(index).zfill(4) + suffix + ".jpg"

    # Если файл существует, то он не перезаписывается
    if os.path.exists(file_path):
        return

    # Выполнение преобразования с переданной функцией и аргументами к ней
    image = image_processing_func(*function_arguments, **named_function_arguments)

    # Запись файла
    cv2.imwrite(file_path, image)

    print("Saved: ", file_path)
