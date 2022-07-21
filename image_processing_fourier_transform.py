import os
import pathlib
import re

import cv2
import numpy as np
import matplotlib.pyplot as plt

from math import sqrt, exp


# https://towardsdatascience.com/image-processing-with-python-application-of-fourier-transformation-5a8584dc175b
# https://hicraigchen.medium.com/digital-image-processing-using-fourier-transform-in-python-bcb49424fd82

# TODO
# https://robotclass.ru/tutorials/opencv-detect-rectangle-angle/
# https://robotclass.ru/tutorials/opencv-color-range-filter/
# https://robotclass.ru/tutorials/opencv-python-find-contours/
# https://medium.com/nuances-of-programming/%D0%BE%D0%B1%D0%BD%D0%B0%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-%D1%86%D0%B2%D0%B5%D1%82%D0%BE%D0%B2%D0%BE%D0%B9-%D1%81%D0%B5%D0%B3%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B8-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B2-python-9128814bc55c

def image_processing_fourier_transform(
        main_output_path,
        folder_index,
        image
):
    print("*****************************************************")
    print("Starting: image_processing_fourier_transform()")
    print("*****************************************************")

    # Путь к сохраняемым файлам
    output_path = main_output_path + "/" + str(folder_index).zfill(4) + "_fourier_transform"

    # Создает папку, если ее не существует
    pathlib \
        .Path(output_path) \
        .mkdir(parents=True, exist_ok=True)

    # Начальный индекс файла
    image_index = 1

    # Преобразует исходное цветное изображение в оттенуи серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # FFT без фильтров
    original = np.fft.fft2(gray_image)
    center = np.fft.fftshift(original)
    inv_center = np.fft.ifftshift(center)
    processed_img = np.fft.ifft2(inv_center)

    # Lowpass Filter
    LowPassCenter = center * idealFilterLP(50, gray_image.shape)
    LowPass = np.fft.ifftshift(LowPassCenter)
    inverse_LowPass = np.fft.ifft2(LowPass)

    # plt.figure(figsize=(6.4 * 25, 4.8 * 25), constrained_layout=False)
    plt.figure(figsize=(6.4 * 5, 4.8 * 5), constrained_layout=False)

    # Original gray image
    image_index = plt_and_save_data(
        output_path,
        image_index,
        "Original Image",
        gray_image
    )

    # Implement Fast Fourier Transformation to transform gray scaled image into frequency
    image_index = plt_and_save_lambda(
        output_path,
        image_index,
        "Processed Image",
        lambda x: np.log(1 + np.abs(x)),
        original
    )


    # Visualize and Centralize zero-frequency component
    image_index = plt_and_save_lambda(
        output_path,
        image_index,
        "Centered Spectrum",
        lambda x: np.log(1 + np.abs(x)),
        center
    )

    # Decentralize
    image_index = plt_and_save_lambda(
        output_path,
        image_index,
        "Decentralized",
        lambda x: np.log(1 + np.abs(x)),
        inv_center
    )

    # Implement inverse Fast Fourier Transformation to generate image data
    image_index = plt_and_save_lambda(
        output_path,
        image_index,
        "Processed Image",
        lambda x: np.abs(x),
        processed_img
    )

    # Spectrum
    image_index = plt_and_save_lambda(
        output_path,
        image_index,
        "Spectrum",
        lambda x: np.log(np.abs(x)),
        original
    )

    # Phase Angel
    image_index = plt_and_save_lambda(
        output_path,
        image_index,
        "Phase Angle",
        lambda x: np.angle(x),
        original
    )

    ################################
    # LowPass
    ################################
    image_index = plt_and_save_lambda(
        output_path,
        image_index,
        "Centered Spectrum multiply Low Pass Filter",
        lambda x: np.log(1 + np.abs(x)),
        LowPassCenter
    )

    image_index = plt_and_save_lambda(
        output_path,
        image_index,
        "Decentralize",
        lambda x: np.log(1 + np.abs(LowPass)),
        LowPass
    )

    image_index = plt_and_save_lambda(
        output_path,
        image_index,
        "Processed Image",
        lambda x: np.abs(x),
        inverse_LowPass
    )

    plt.show()

    print()
    print()
    print("*****************************************************")
    print("*****************************************************")
    print()
    print()


def distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def idealFilterLP(D0, imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            if distance((y, x), center) < D0:
                base[y, x] = 1
    return base


def idealFilterHP(D0, imgShape):
    base = np.ones(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            if distance((y, x), center) < D0:
                base[y, x] = 0
    return base


def butterworthLP(D0, imgShape, n):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            base[y, x] = 1 / (1 + (distance((y, x), center) / D0) ** (2 * n))
    return base


def butterworthHP(D0, imgShape, n):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            base[y, x] = 1 - 1 / (1 + (distance((y, x), center) / D0) ** (2 * n))
    return base


def gaussianLP(D0, imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            base[y, x] = exp(((-distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
    return base


def gaussianHP(D0, imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows / 2, cols / 2)
    for x in range(cols):
        for y in range(rows):
            base[y, x] = 1 - exp(((-distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
    return base


# Строит график по функции и массиву данных и сохраняет в файл
def plt_and_save_lambda(
        output_path,
        image_index,
        tittle,
        lambda_expression,
        data
):
    # Имя файла и индексом
    indexed_filename = str(image_index).zfill(4) + "_" + to_snake_case(tittle) + ".png"

    print("Processing: " + indexed_filename)

    # Если файл существует, то ничего не делаем
    if os.path.exists(output_path + "/" + indexed_filename):
        print("File exists! The old version remains!")
        return image_index + 1

    # Построение
    plt.imshow(lambda_expression(data).astype(np.uint8), "gray"), plt.title(tittle)

    # Сохранение
    plt.savefig(output_path + '/' + indexed_filename, bbox_inches='tight')

    return image_index + 1


# Строит график по массиву данных и сохраняет в файл
def plt_and_save_data(
        output_path,
        image_index,
        tittle,
        data
):
    # Имя файла и индексом
    indexed_filename = str(image_index).zfill(4) + "_" + to_snake_case(tittle) + ".png"

    print("Processing: " + indexed_filename)

    # Если файл существует, то ничего не делаем
    if os.path.exists(output_path + "/" + indexed_filename):
        print("File exists! The old version remains!")
        return image_index + 1

    # Построение
    plt.imshow(data, "gray"), plt.title(tittle)

    # Сохранение
    plt.savefig(output_path + '/' + indexed_filename, bbox_inches='tight')

    return image_index + 1


# Преобразует обычную строку в snake_case
def to_snake_case(string):
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', string)
    return '_'.join(map(str.lower, words))
