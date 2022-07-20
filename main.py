import sys
import getopt
import cv2
import pathlib

from filtering_image_processing_bilateral import filtering_image_processing_bilateral
from filtering_image_processing_blur import filtering_image_processing_blur
from filtering_image_processing_gaussian_blur import filtering_image_processing_gaussian_blur
from filtering_image_processing_median_blur import filtering_image_processing_median_blur
from morphological_image_processing import morphological_image_processing


# Определение функции main
def main(argv):
    input_path = ''
    output_path = ''

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
            output_path = arg

    # Если входной путь не задан, то выход
    if input_path == "":
        print("Enter input path!")
        sys.exit()
    # Если выходной путь не задан, то выход
    if output_path == "":
        print("Enter output path!")
        sys.exit()

    #################################################
    # Считывает исходный файл изображения
    # и подготавливает папку для результатов
    #################################################

    # TODO find files in SRC dir
    filename = "image1.jpg"
    output_path += "/" + filename[:-4]

    # Создает папку, если ее не существует
    pathlib \
        .Path(output_path) \
        .mkdir(parents=True, exist_ok=True)

    # Открывает исходный файл
    image = cv2.imread(
        input_path + "/" + filename,
        1)

    #################################################
    # Обработка изображений
    #################################################

    # Индекс папки
    folder_index = 1

    # Morphological Image Processing
    morphological_image_processing(
        output_path,
        folder_index,
        5,  # Здесь нет диапазона, указывается только число
        image
    )
    folder_index += 1

    # Filtering Image Processing: Blur
    filtering_image_processing_blur(
        output_path,
        folder_index,
        range(1, 20),
        image
    )
    folder_index += 1

    # Filtering Image Processing: Gaussian Blur
    filtering_image_processing_gaussian_blur(
        output_path,
        folder_index,
        [5],
        image
    )
    folder_index += 1

    # Filtering Image Processing: Median Blur
    filtering_image_processing_median_blur(
        output_path,
        folder_index,
        [5],
        image
    )
    folder_index += 1

    # Filtering Image Processing: Bilateral
    # Можно использовать для проверки, получился ли передний план (все остальное блекнет)
    filtering_image_processing_bilateral(
        output_path,
        folder_index,
        [5, 25, 50, 100, 200, 300, 1000],
        image
    )
    folder_index += 1

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
