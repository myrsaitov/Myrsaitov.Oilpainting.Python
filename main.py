import sys
import getopt
import cv2
import pathlib

import numpy as np

from image_processing_filtering_bilateral import image_processing_filtering_bilateral
from image_processing_filtering_blur import image_processing_filtering_blur
from image_processing_filtering_gaussian_blur import image_processing_filtering_gaussian_blur
from image_processing_filtering_median_blur import image_processing_filtering_median_blur
from image_processing_fourier_transform import fourier_image_processing, ideal_low_pass_filter, ideal_high_pass_filter, \
    fourier_base_processing, fourier_filter_processing
from image_processing_morphological import image_processing_morphological


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


    ######################################################################
    # Morphological Image Processing
    ######################################################################
    image_processing_morphological(
        output_path,
        folder_index,
        5,  # Здесь нет диапазона, указывается только число
        image
    )
    folder_index += 1


    ######################################################################
    # Filtering
    ######################################################################

    # Filtering Image Processing: Blur
    image_processing_filtering_blur(
        output_path,
        folder_index,
        range(1, 20),
        image
    )
    folder_index += 1

    # Filtering Image Processing: Gaussian Blur
    image_processing_filtering_gaussian_blur(
        output_path,
        folder_index,
        [5],
        image
    )
    folder_index += 1

    # Filtering Image Processing: Median Blur
    image_processing_filtering_median_blur(
        output_path,
        folder_index,
        [5],
        image
    )
    folder_index += 1

    # Filtering Image Processing: Bilateral
    # Можно использовать для проверки, получился ли передний план (все остальное блекнет)
    image_processing_filtering_bilateral(
        output_path,
        folder_index,
        [5, 25, 50, 100],  # , 200, 300, 1000],
        image
    )
    folder_index += 1


    ######################################################################
    # Fourier Transforms
    ######################################################################

    # Преобразует исходное цветное изображение в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Размер координатной плоскости для построения результатов
    figure_size = (6.4 * 5, 4.8 * 5)  # (6.4 * 25, 4.8 * 25))

    folder_index = fourier_base_processing(
        "Base Fourier Processing",
        output_path,
        folder_index,
        figure_size,
        gray_image
    )

    folder_index = fourier_filter_processing(
        "Ideal LowPass Filter Processing",
        output_path,
        folder_index,
        figure_size,
        gray_image,
        [10, 50, 100, 150]
    )

    folder_index = fourier_image_processing(
        "Ideal HighPass Filter Processing",
        output_path,
        folder_index,
        figure_size,
        gray_image,

        # (1) Действие над данными
        # (2) Действие для вывода данных на плоскость
        # (3) Заголовок
        [

            [
                "Original gray image",
                lambda x: x,
                lambda x: x
            ],

            [
                "Spectrum",
                lambda x: np.fft.fft2(x),
                lambda x: np.log(1 + np.abs(x))
            ],

            [
                "Centered Spectrum",
                lambda x: np.fft.fftshift(x),
                lambda x: np.log(1 + np.abs(x))
            ],

            [
                "Centered Spectrum multiply High Pass Filter",
                lambda x: x * ideal_high_pass_filter(200, gray_image.shape),
                lambda x: np.log(1 + np.abs(x))
            ],

            [
                "Decentralize",
                lambda x: np.fft.ifftshift(x),
                lambda x: np.log(1 + np.abs(x))
            ],

            [
                "Processed Image",
                lambda x: np.fft.ifft2(x),
                lambda x: np.abs(x)
            ]

        ]

    )

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
