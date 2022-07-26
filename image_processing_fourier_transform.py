import os
import pathlib
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, exp

from to_snake_case import to_snake_case


# https://towardsdatascience.com/image-processing-with-python-application-of-fourier-transformation-5a8584dc175b
# https://hicraigchen.medium.com/digital-image-processing-using-fourier-transform-in-python-bcb49424fd82

# TODO
# https://robotclass.ru/tutorials/opencv-detect-rectangle-angle/
# https://robotclass.ru/tutorials/opencv-color-range-filter/
# https://robotclass.ru/tutorials/opencv-python-find-contours/
# https://medium.com/nuances-of-programming/%D0%BE%D0%B1%D0%BD%D0%B0%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-%D1%86%D0%B2%D0%B5%D1%82%D0%BE%D0%B2%D0%BE%D0%B9-%D1%81%D0%B5%D0%B3%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B8-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B2-python-9128814bc55c

def fourier_base_processing(
        main_tittle,
        base_output_path,
        folder_index,
        figure_size,
        gray_image
):
    return fourier_image_processing(
        main_tittle,
        base_output_path,
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
                "Spectrum2",
                lambda x: x,
                lambda x: np.log(np.abs(x))
            ],

            [
                "Phase Angle",
                lambda x: x,
                lambda x: np.angle(x)
            ],

            [
                "Centered Spectrum",
                lambda x: np.fft.fftshift(x),
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
            ],

        ]

    )


def fourier_filter_processing(
        main_tittle,
        base_output_path,
        folder_index,
        figure_size,
        gray_image,
        freqs
):
    index = folder_index

    for freq in freqs:
        index = fourier_image_processing(
            main_tittle,
            base_output_path,
            index,
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
                    "Centered Spectrum multiply Low Pass Filter" + "Freq" + str(freq).zfill(4),
                    lambda x: x * ideal_low_pass_filter(freq, gray_image.shape),
                    lambda x: np.log(1 + np.abs(x))
                ],

                [
                    "Decentralize" + "Freq" + str(freq).zfill(4),
                    lambda x: np.fft.ifftshift(x),
                    lambda x: np.log(1 + np.abs(x))
                ],

                [
                    "Processed Image" + "Freq" + str(freq).zfill(4),
                    lambda x: np.fft.ifft2(x),
                    lambda x: np.abs(x)
                ]

            ]

        )

    return index


# Главная процедура обработки данных
def fourier_image_processing(
        main_tittle,
        base_output_path,
        folder_index,
        figure_size,
        gray_image,
        process_options
):
    print("*****************************************************")
    print("Starting: ", main_tittle)
    print("*****************************************************")

    # Путь к сохраняемым файлам
    output_path = base_output_path + \
                  "/" + \
                  str(folder_index).zfill(4) + \
                  "_" + \
                  to_snake_case(main_tittle)

    # Создает папку, если ее не существует
    pathlib \
        .Path(output_path) \
        .mkdir(parents=True, exist_ok=True)

    # Конфигурирует плоскость построения графиков
    plt.figure(figsize=figure_size, constrained_layout=False)

    # Хранит данные между итерациями
    data = gray_image

    # В цикле обрабатывает данные и сохраняет графики
    for option in process_options:
        tittle, process_data, process_image = option
        data = process_data(data)

        # Имя файла с индексом
        filename = to_snake_case(tittle) + ".png"

        print("Processing: " + filename)

        # Если файл существует, то ничего не делаем
        if os.path.exists(output_path + "/" + filename):
            print("File exists! The old version remains!")
            continue

        # Построение
        plt.imshow(process_image(data).astype(np.uint8), "gray"), plt.title(tittle)

        # Сохранение
        plt.savefig(output_path + '/' + filename, bbox_inches='tight')

    plt.show()

    print()
    print()
    print("*****************************************************")
    print("*****************************************************")
    print()
    print()

    return folder_index + 1


def distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def ideal_low_pass_filter(d0, image_shape):
    base = np.zeros(image_shape[:2])
    rows, cols = image_shape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            if distance((y, x), center) < d0:
                base[y, x] = 1
    return base


def ideal_high_pass_filter(d0, image_shape):
    base = np.ones(image_shape[:2])
    rows, cols = image_shape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            if distance((y, x), center) < d0:
                base[y, x] = 0
    return base


def butterworth_low_pass_filter(d0, image_shape, n):
    base = np.zeros(image_shape[:2])
    rows, cols = image_shape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            base[y, x] = 1 / (1 + (distance((y, x), center) / d0) ** (2 * n))
    return base


def butterworth_high_pass_filter(self, d0, image_shape, n):
    base = np.zeros(image_shape[:2])
    rows, cols = image_shape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            base[y, x] = 1 - 1 / (1 + (self.__distance((y, x), center) / d0) ** (2 * n))
    return base


def gaussian_low_pass_filter(d0, image_shape):
    base = np.zeros(image_shape[:2])
    rows, cols = image_shape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            base[y, x] = exp(((-distance((y, x), center) ** 2) / (2 * (d0 ** 2))))
    return base


def gaussian_high_pass_filter(d0, image_shape):
    base = np.zeros(image_shape[:2])
    rows, cols = image_shape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            base[y, x] = 1 - exp(((-distance((y, x), center) ** 2) / (2 * (d0 ** 2))))
    return base
