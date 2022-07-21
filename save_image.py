import cv2
import os.path


# Записывает файл с изображением на диск
def image_save(
        path,
        index,
        suffix,
        image
):

    # Добавляет индекс в начале файла для удобства сортировки по имени
    file_path = path + "/" + str(index).zfill(4) + suffix + ".jpg"

    # Если файл существует, то он не перезаписывается
    if os.path.exists(file_path):
        print("File exists! The old version remains!")
        return

    # Запись файла
    cv2.imwrite(file_path, image)
