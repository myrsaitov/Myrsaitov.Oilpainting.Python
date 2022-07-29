import sys
import getopt
import cv2
import pathlib

from image_processing_filtering import image_processing_filtering
from image_processing_fourier_transform import ideal_high_pass_filter, \
    fourier_processing, ideal_low_pass_filter
from image_processing_get_dominate_colors import image_processing_get_dominate_colors
from image_processing_morphological import image_processing_morphological


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


    ######################################################################
    # Morphological Image Processing
    ######################################################################
    image_processing_morphological(
        output_path_root,
        5,  # Здесь нет диапазона, указывается только число
        image
    )


    ######################################################################
    # Filtering
    ######################################################################

    # Filtering Image Processing: Blur
    for size in range(1, 20):
        image_processing_filtering(
            "Filtering: Blur",
            output_path_root,
            cv2.blur,
            image,
            (size, size)
        )

    # Filtering Image Processing: Gaussian Blur
    # Только нечетные значения size!
    for size in range(1, 50, 4):
        image_processing_filtering(
            "Filtering: Gaussian Blur",
            output_path_root,
            cv2.GaussianBlur,
            image,
            (size, size),
            cv2.BORDER_DEFAULT
        )

    # Filtering Image Processing: Median Blur
    # Только нечетные значения size!
    for size in range(1, 50, 4):
        image_processing_filtering(
            "Filtering: Median Blur",
            output_path_root,
            cv2.medianBlur,
            image,
            size
        )

    # Filtering Image Processing: Bilateral
    # Можно использовать для проверки, получился ли передний план (все остальное блекнет)
    for size in [5, 25, 50, 100]:  # , 200, 300, 1000],:
        image_processing_filtering(
            "Filtering: Bilateral Blur",
            output_path_root,
            cv2.bilateralFilter,
            image,
            size,
            75,
            75
        )

    ######################################################################
    # Fourier Transforms
    ######################################################################

    # Преобразует исходное цветное изображение в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    fourier_processing(
        "Fourier Processing: Ideal LowPass Filter",
        output_path_root,
        gray_image,
        lambda f, shape: ideal_low_pass_filter(f, shape),
        range(0, 400, 10)
    )

    fourier_processing(
        "Fourier Processing: Ideal HighPass Filter",
        output_path_root,
        gray_image,
        lambda f, shape: ideal_high_pass_filter(f, shape),
        range(0, 400, 10)
    )

    fourier_processing(
        "Fourier Processing: Ideal BandPass Filter (10 Hz)",
        output_path_root,
        gray_image,
        lambda f, shape: ideal_low_pass_filter(f + 10, shape)*ideal_high_pass_filter(f, shape),
        range(0, 400, 10)
    )

    fourier_processing(
        "Fourier Processing: Ideal BandPass Filter (50 Hz)",
        output_path_root,
        gray_image,
        lambda f, shape: ideal_low_pass_filter(f + 50, shape)*ideal_high_pass_filter(f, shape),
        range(0, 400, 10)
    )

    fourier_processing(
        "Fourier Processing: Ideal Rejector Filter (10 Hz)",
        output_path_root,
        gray_image,
        lambda f, shape: 1 - ideal_low_pass_filter(f + 10, shape)*ideal_high_pass_filter(f, shape),
        range(0, 400, 10)
    )

    fourier_processing(
        "Fourier Processing: Ideal Rejector Filter (50 Hz)",
        output_path_root,
        gray_image,
        lambda f, shape: 1 - ideal_low_pass_filter(f + 50, shape)*ideal_high_pass_filter(f, shape),
        range(0, 400, 10)
    )


    ######################################################################
    # Dominate Colors
    ######################################################################

    image_processing_get_dominate_colors(
        "Get Dominate Colors",
        output_path_root,
        3,
        image
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
