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

class image_processing_fourier_transform(object):

    # Поля класса

    # Начальный индекс файла
    image_index = 1

    # Базовый путь к сохраняемому файлу
    output_path = None

    # Конструктор класса
    def __init__(self):
        s = 3

    def all_processes(
            self,
            main_output_path,
            folder_index,
            image
    ):
        print("*****************************************************")
        print("Starting: image_processing_fourier_transform()")
        print("*****************************************************")

        # Путь к сохраняемым файлам
        self.output_path = main_output_path + "/" + str(folder_index).zfill(4) + "_fourier_transform"

        # Создает папку, если ее не существует
        pathlib \
            .Path(self.output_path) \
            .mkdir(parents=True, exist_ok=True)

        # Преобразует исходное цветное изображение в оттенуи серого
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # FFT без фильтров
        original = np.fft.fft2(gray_image)
        center = np.fft.fftshift(original)
        inv_center = np.fft.ifftshift(center)
        processed_img = np.fft.ifft2(inv_center)

        # Lowpass Filter
        LowPassCenter = center * self.idealFilterLP(50, gray_image.shape)
        LowPass = np.fft.ifftshift(LowPassCenter)
        inverse_LowPass = np.fft.ifft2(LowPass)

        # plt.figure(figsize=(6.4 * 25, 4.8 * 25), constrained_layout=False)
        plt.figure(figsize=(6.4 * 5, 4.8 * 5), constrained_layout=False)

        # Original gray image
        self.plt_and_save_data(
            "Original Image",
            gray_image
        )

        # Implement Fast Fourier Transformation to transform gray scaled image into frequency
        self.plt_and_save_lambda(
            "Processed Image",
            lambda x: np.log(1 + np.abs(x)),
            original
        )

        # Visualize and Centralize zero-frequency component
        self.plt_and_save_lambda(
            "Centered Spectrum",
            lambda x: np.log(1 + np.abs(x)),
            center
        )

        # Decentralize
        self.plt_and_save_lambda(
            "Decentralized",
            lambda x: np.log(1 + np.abs(x)),
            inv_center
        )

        # Implement inverse Fast Fourier Transformation to generate image data
        self.plt_and_save_lambda(
            "Processed Image",
            lambda x: np.abs(x),
            processed_img
        )

        # Spectrum
        self.plt_and_save_lambda(
            "Spectrum",
            lambda x: np.log(np.abs(x)),
            original
        )

        # Phase Angel
        self.plt_and_save_lambda(
            "Phase Angle",
            lambda x: np.angle(x),
            original
        )

        ################################
        # LowPass
        ################################
        self.plt_and_save_lambda(
            "Centered Spectrum multiply Low Pass Filter",
            lambda x: np.log(1 + np.abs(x)),
            LowPassCenter
        )

        self.plt_and_save_lambda(
            "Decentralize",
            lambda x: np.log(1 + np.abs(LowPass)),
            LowPass
        )

        self.plt_and_save_lambda(
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

        return folder_index + 1


    def distance(self, point1, point2):
        return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


    def idealFilterLP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) < D0:
                    base[y, x] = 1
        return base

    def idealFilterHP(self, D0, imgShape):
        base = np.ones(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) < D0:
                    base[y, x] = 0
        return base

    def butterworthLP(self, D0, imgShape, n):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 / (1 + (self.distance((y, x), center) / D0) ** (2 * n))
        return base

    def butterworthHP(self, D0, imgShape, n):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 - 1 / (1 + (self.distance((y, x), center) / D0) ** (2 * n))
        return base

    def gaussianLP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = exp(((-self.distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
        return base

    def gaussianHP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 - exp(((-self.distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
        return base

    # Строит график по функции и массиву данных и сохраняет в файл
    def plt_and_save_lambda(
            self,
            tittle,
            lambda_expression,
            data
    ):
        # Имя файла и индексом
        indexed_filename = str(self.image_index).zfill(4) +\
                           "_" +\
                           self.to_snake_case(tittle) + ".png"

        print("Processing: " + indexed_filename)

        # Если файл существует, то ничего не делаем
        if os.path.exists(self.output_path + "/" + indexed_filename):
            print("File exists! The old version remains!")
            self.image_index += 1
            return

        # Построение
        plt.imshow(lambda_expression(data).astype(np.uint8), "gray"), plt.title(tittle)

        # Сохранение
        plt.savefig(self.output_path + '/' + indexed_filename, bbox_inches='tight')

        self.image_index += 1
        return

    # Строит график по массиву данных и сохраняет в файл
    def plt_and_save_data(
            self,
            tittle,
            data
    ):
        # Имя файла и индексом
        indexed_filename = str(self.image_index).zfill(4) + \
                           "_" + \
                           self.to_snake_case(tittle) + ".png"

        print("Processing: " + indexed_filename)

        # Если файл существует, то ничего не делаем
        if os.path.exists(self.output_path + "/" + indexed_filename):
            print("File exists! The old version remains!")
            self.image_index += 1
            return

        # Построение
        plt.imshow(data, "gray"), plt.title(tittle)

        # Сохранение
        plt.savefig(self.output_path + '/' + indexed_filename, bbox_inches='tight')

        self.image_index += 1
        return

    # Преобразует обычную строку в snake_case
    def to_snake_case(self, string):
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', string)
        return '_'.join(map(str.lower, words))
