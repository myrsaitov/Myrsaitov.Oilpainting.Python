import cv2
import os.path


# Записывает файл с изображением на диск
def image_save(
        path,
        index,
        suffix,
        image):

    # Добавляет индекс в начале файла для удобства сортировки по имени
    file_path = path + "/" + str(index).zfill(4) + suffix + ".jpg"

    # Если файл существует, то он не перезаписывается
    if os.path.exists(file_path):
        return

    # Запись файла
    cv2.imwrite(file_path, image)

    # Масштабирует изображение в пределах экрана
    #image_resized = cv2.resize(image, (1024, 768))

    # Выводит отмасштабированное изображение на экран
    #cv2.imshow(tittle, image_resized)

    # Ожидает нажатия клавиши для закрытия
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
