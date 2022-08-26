import inspect
import os
import pathlib

from to_snake_case import to_snake_case


def functional_primitive(
        title,  # Заголовок, описание
        output_path_root,  # Путь к корневому расположению результатов
        function_name,  # Название вызываемой функции
        return_if_file_exists=True,  # Если файл существует, то никаких действий не предпринимать
        return_if_folder_exists=True,  # Если папка существует, то никаких действий не предпринимать
        *argv,  # Позиционные аргументы функции
        **kwargs  # Именованные аргументы функции, например: iterations=5
):
    print("*****************************************************")
    print("Starting: ", title)
    print("*****************************************************")

    # Путь и папка для сохранения результата
    output_path = output_path_root + \
                  "/" + to_snake_case(title)

    # Если папка существует, то действия не требуются
    if os.path.exists(output_path) and return_if_folder_exists:
        print("The folder exists! The old version remains!")
        return None
    else:
        # Создает папку, если ее не существует
        pathlib \
            .Path(output_path) \
            .mkdir(parents=True, exist_ok=True)

    # Вызывает процедуру
    function_name(output_path, *argv, **kwargs)
