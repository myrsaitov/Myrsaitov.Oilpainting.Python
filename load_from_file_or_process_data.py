import os
import pickle
import inspect


# Проверяет, есть ли сохраненные данные, тогда загружает из файла,
# иначе рассчитывает по заданной функции.
# Используется, где процесс рассчета длительный.


def load_from_file_or_process_data(
        filename,
        data_processing_func,  # Функция для преобразования изображения
        *argv,                 # Позиционные аргументы функции
        **kwargs               # Именованные аргументы функции, например: iterations=5
):                             # https://tproger.ru/translations/python-args-and-kwargs/
                               # https://python.ivan-shamaev.ru/python-3-functions-value-arguments-call-variables-arrays/

    print("*****************************************************")
    print("Starting: ", inspect.currentframe().f_code.co_name)
    print("Checking File: ", filename)
    print("*****************************************************")

    # Если файл с данными существует
    if os.path.exists(filename):

        print("The saved file exists! Opening!")

        # Загружает данные из файла
        with open(filename, "rb") as f:
            data = pickle.load(f)

    else:

        # Обрабатывает данные
        data = data_processing_func(*argv, **kwargs)

        # Сохраняет в файл
        with open(filename, "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    return data
