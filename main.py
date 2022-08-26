import sys
import getopt
import cv2
import pathlib

from image_processing_filtering import filter_processing_wrapper
from image_processing_fourier_transform import fourier_processing_wrapper
from image_processing_get_dominate_colors import dominate_colors_processing_wrapper
from image_processing_brightness import brightness_processing_wrapper
from image_processing_morphological import morphological_processing_wrapper


# Определение функции main
def main(argv):
    input_path = ''
    output_path_root = ''

    #################################################
    # Считывает параметры командной строки
    #################################################
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ipath=", "opath="])
    except getopt.GetoptError:
        print('main.py -i <input_path> -o <output_path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <input_path> -o <output_path>')
            sys.exit()
        elif opt in ("-i", "--ipath"):
            input_path = arg
        elif opt in ("-o", "--opath"):
            output_path_root = arg

    # Если входной путь не задан, то выход
    if input_path == "":
        print("Enter input path!")
        sys.exit()
    # Если выходной путь не задан, то выход
    if output_path_root == "":
        print("Enter output path!")
        sys.exit()

    #################################################
    # Считывает исходный файл изображения
    # и подготавливает папку для результатов
    #################################################

    # TODO find files in SRC dir
    filename = "image1.jpg"
    output_path_root += "/" + filename[:-4]

    # Создает папку, если ее не существует
    pathlib \
        .Path(output_path_root) \
        .mkdir(parents=True, exist_ok=True)

    # Открывает исходный файл
    image = cv2.imread(
        input_path + "/" + filename,
        1)

    #################################################
    # Обработка изображений
    #################################################
    morphological_processing_wrapper(output_path_root, image)
    filter_processing_wrapper(output_path_root, image)
    fourier_processing_wrapper(output_path_root, image)
    dominate_colors_processing_wrapper(output_path_root, image)
    brightness_processing_wrapper(output_path_root, image)

    #################################################
    # Выход из программы
    #################################################
    sys.exit()


# Переменная __name__ - это специальная переменная,
# которая будет равна "__main__", только если файл
# запускается как основная программа, и выставляется
# равной имени модуля при импорте модуля.
# То есть, условие if __name__ == '__main__' проверяет,
# был ли файл запущен напрямую.
if __name__ == "__main__":
    main(sys.argv[1:])
