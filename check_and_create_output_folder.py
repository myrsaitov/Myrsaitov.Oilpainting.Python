# Создает новую папку для результатов работы алгоритма.
# Если папка уже существует, то алгоритм не выполняется
import inspect
import os
import pathlib

from to_snake_case import to_snake_case


def check_and_create_output_folder(
        title,
        output_path_root
):

    print("*****************************************************")
    print("Starting function: ", inspect.currentframe().f_back.f_code.co_name, ": ", title)
    print("*****************************************************")


    # Путь к сохраняемым файлам
    output_path = output_path_root + \
                  "/" + to_snake_case(title)

    # Если папка существует, то действия не требуются
    if os.path.exists(output_path):
        print("The folder exists! The old version remains!")
        return None
    else:
        # Создает папку, если ее не существует
        pathlib \
            .Path(output_path) \
            .mkdir(parents=True, exist_ok=True)

    return output_path
