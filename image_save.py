import cv2


# Выводит изображение на экран
def image_save(
        base_tittle,
        suffix,
        image):

    cv2.imwrite(base_tittle[:-4] + "_" + suffix + ".jpg", image)


    # Масштабирует изображение в пределах экрана
    #image_resized = cv2.resize(image, (1024, 768))

    # Выводит отмасштабированное изображение на экран
    #cv2.imshow(tittle, image_resized)

    # Ожидает нажатия клавиши для закрытия
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
