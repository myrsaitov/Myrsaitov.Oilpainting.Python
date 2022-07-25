import inspect
import os
import pathlib
import re
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

    # Базовый путь
    base_output_path = None

    # Текущий путь к сохраняемому файлу
    output_path = None

    # Текущий размер плоскости
    figsize = None

    # Конструктор класса
    def __init__(self, output_path, figsize):
        self.base_output_path = output_path
        self.figsize = figsize

    def base_fourier_processing(
            self,
            folder_index,
            gray_image
    ):

        # Получает название функции в строковой форме
        tittle = inspect.currentframe().f_code.co_name

        print("*****************************************************")
        print("Starting: ", tittle)
        print("*****************************************************")

        # Путь к сохраняемым файлам
        self.output_path = self.base_output_path + \
                           "/" + \
                           str(folder_index).zfill(4) + \
                           "_" + \
                           tittle

        # Создает папку, если ее не существует
        pathlib \
            .Path(self.output_path) \
            .mkdir(parents=True, exist_ok=True)

        # Начальный индекс файла
        self.image_index = 1

        # Конфигурирует плоскость построения графиков
        plt.figure(
            figsize=self.figsize,
            constrained_layout=False)

        # Original gray image
        self.__process_data_and_save(
            gray_image,
            lambda x: x
        )

        # Implement Fast Fourier Transformation to transform gray scaled image into frequency
        gray_image_fft2 = np.fft.fft2(gray_image)
        self.__process_data_and_save(
            gray_image_fft2,
            lambda x: np.log(1 + np.abs(x))
        )

        # Spectrum
        self.__process_data_and_save(
            gray_image_fft2,
            lambda x: np.log(np.abs(x))
        )

        # Phase Angel
        self.__process_data_and_save(
            gray_image_fft2,
            lambda x: np.angle(x)
        )

        # Visualize and Centralize zero-frequency component
        gray_image_fft2_fftshift = np.fft.fftshift(gray_image_fft2)
        self.__process_data_and_save(
            gray_image_fft2_fftshift,
            lambda x: np.log(1 + np.abs(x))
        )

        # Decentralize
        gray_image_fft2_fftshift_ifftshift = np.fft.ifftshift(gray_image_fft2_fftshift)
        self.__process_data_and_save(
            gray_image_fft2_fftshift_ifftshift,
            lambda x: np.log(1 + np.abs(x))
        )

        # Implement inverse Fast Fourier Transformation to generate image data
        gray_image_fft2_fftshift_ifftshift_ifft2 = np.fft.ifft2(gray_image_fft2_fftshift_ifftshift)
        self.__process_data_and_save(
            gray_image_fft2_fftshift_ifftshift_ifft2,
            lambda x: np.abs(x)
        )

        plt.show()

        print()
        print()
        print("*****************************************************")
        print("*****************************************************")
        print()
        print()

        return folder_index + 1

    def lowpass_filter_processing(
            self,
            folder_index,
            gray_image
    ):

        # Получает название функции в строковой форме
        tittle = inspect.currentframe().f_code.co_name

        print("*****************************************************")
        print("Starting: ", tittle)
        print("*****************************************************")

        # Путь к сохраняемым файлам
        self.output_path = self.base_output_path + \
                           "/" + \
                           str(folder_index).zfill(4) + \
                           "_" + \
                           tittle

        # Создает папку, если ее не существует
        pathlib \
            .Path(self.output_path) \
            .mkdir(parents=True, exist_ok=True)

        # Начальный индекс файла
        self.image_index = 1

        # Конфигурирует плоскость построения графиков
        plt.figure(figsize=self.figsize, constrained_layout=False)

        # Original gray image
        self.__process_data_and_save(
            gray_image,
            lambda x: x
        )

        # Implement Fast Fourier Transformation to transform gray scaled image into frequency
        gray_image_fft2 = np.fft.fft2(gray_image)
        self.__process_data_and_save(
            gray_image_fft2,
            lambda x: np.log(1 + np.abs(x))
        )

        # Visualize and Centralize zero-frequency component
        gray_image_fft2_fftshift = np.fft.fftshift(gray_image_fft2)
        self.__process_data_and_save(
            gray_image_fft2_fftshift,
            lambda x: np.log(1 + np.abs(x))
        )

        ################################
        # LowPass
        ################################

        gray_image_fft2_fftshift_lowpass = gray_image_fft2_fftshift * self.idealFilterLP(50, gray_image.shape)
        self.__process_data_and_save(
            gray_image_fft2_fftshift_lowpass,
            lambda x: np.log(1 + np.abs(x))
        )

        gray_image_fft2_fftshift_lowpass_ifftshift = np.fft.ifftshift(gray_image_fft2_fftshift_lowpass)
        self.__process_data_and_save(
            gray_image_fft2_fftshift_lowpass_ifftshift,
            lambda x: np.log(1 + np.abs(x))
        )

        gray_image_fft2_fftshift_lowpass_ifftshift_ifft2 = np.fft.ifft2(gray_image_fft2_fftshift_lowpass_ifftshift)
        self.__process_data_and_save(
            gray_image_fft2_fftshift_lowpass_ifftshift_ifft2,
            lambda x: np.abs(x)
        )

        plt.show()

        print()
        print()
        print("*****************************************************")
        print("*****************************************************")
        print()
        print()

        return folder_index + 1

    def lowpass_filter_processing_new_style(
            self,
            tittle,
            folder_index,
            gray_image,
            process_options
    ):

        # Получает название функции в строковой форме
        # tittle = inspect.currentframe().f_code.co_name

        print("*****************************************************")
        print("Starting: ", tittle)
        print("*****************************************************")

        # Путь к сохраняемым файлам
        self.output_path = self.base_output_path + \
                           "/" + \
                           str(folder_index).zfill(4) + \
                           "_" + \
                           tittle

        # Создает папку, если ее не существует
        pathlib \
            .Path(self.output_path) \
            .mkdir(parents=True, exist_ok=True)

        # Начальный индекс файла
        self.image_index = 1

        # Конфигурирует плоскость построения графиков
        plt.figure(figsize=self.figsize, constrained_layout=False)

        #
        data = gray_image
        for option in process_options:
            tittle, process_data, process_image = option
            data = process_data(data)

            self.__process_data_and_save_with_tittle(
                data,
                process_image,
                tittle
            )

        plt.show()

        print()
        print()
        print("*****************************************************")
        print("*****************************************************")
        print()
        print()

        return folder_index + 1

################################################################
# PRIVATE
################################################################

    def __distance(self, point1, point2):
        return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def idealFilterLP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if self.__distance((y, x), center) < D0:
                    base[y, x] = 1
        return base

    def __idealFilterHP(self, D0, imgShape):
        base = np.ones(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if self.__distance((y, x), center) < D0:
                    base[y, x] = 0
        return base

    def __butterworthLP(self, D0, imgShape, n):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 / (1 + (self.__distance((y, x), center) / D0) ** (2 * n))
        return base

    def __butterworthHP(self, D0, imgShape, n):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 - 1 / (1 + (self.__distance((y, x), center) / D0) ** (2 * n))
        return base

    def __gaussianLP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = exp(((-self.__distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
        return base

    def __gaussianHP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 - exp(((-self.__distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
        return base

    def __retrieve_name(self, var):
        callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
        name_list = [var_name for var_name, var_val in callers_local_vars if var_val is var]
        return name_list[0] if name_list else None

    # Строит график по функции и массиву данных и сохраняет в файл
    def __process_data_and_save(
            self,
            data,
            lambda_expression
    ):

        # Имя переменной
        var_name = self.__retrieve_name(data)

        # Функция
        func_str = (self.__to_snake_case(
                inspect.getsourcelines(
                    lambda_expression
                )[0][0]
            )
        )[+7:]  # Отрезает первые 9 байт

        # Заголовок - имя переменной + lambda
        tittle = var_name + \
            "__FUNC(X)__" + \
            func_str

        # Имя файла с индексом
        indexed_filename = str(self.image_index).zfill(4) + \
                           "_" + \
                           tittle \
                           + ".png"

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

    # Строит график по функции и массиву данных и сохраняет в файл
    def __process_data_and_save_with_tittle(
            self,
            data,
            lambda_expression,
            tittle
    ):

        # Имя файла с индексом
        indexed_filename = str(self.image_index).zfill(4) + \
                           "_" + \
                           tittle \
                           + ".png"

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

    # Преобразует обычную строку в snake_case
    def __to_snake_case(self, string):

        # https://docs.microsoft.com/ru-ru/dotnet/standard/base-types/regular-expression-language-quick-reference

        # Разделяем на слова
        #
        # Исходное выражение
        # [A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+
        # |: Соответствует любому элементу, разделенному вертикальной чертой.
        #
        # Таким образом, получаем равнозначные выражения, соединенные по принципу "ИЛИ":
        #
        #    => Слова, состоящие только из букв, могут иметь большую букву в начале, но необязательно:
        #    [A-Z]?[a-z]+
        #        [A-Z]: Диапазон A-Z
        #        ?: Квантификатор: соответствует предыдущему элементу 0 или 1 раз
        #        [a-z]: Диапазон a-z
        #        +: Квантификатор: соответствует предыдущему элементу 1 или более раз
        #
        #    => Минимум две заглавных буквы, после которых или заглавная + строковая
        #        или число или символ или конец строки:
        #    [A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)
        #        [A-Z]: Диапазон A-Z
        #        {2,}: Предыдущий элемент повторяется как минимум 2 раза
        #        x(?=y): Сопоставляется с x, только если за x следует y:
        #                [A-Z]: Диапазон A-Z
        #                [a-z]: Диапазон a-z
        #            ИЛИ
        #                \d: Соответствие любой десятичной цифре
        #            ИЛИ
        #                \W: Соответствует любому символу, отличному от слова
        #            ИЛИ
        #                $: По умолчанию соответствие должно обнаруживаться
        #                    в конце строки или перед символом \n в конце строки.
        #
        #    => Число, состоящее из любого количества десятичных цифр, без разделяющих знаков
        #    \d+
        #        \d: Соответствие любой десятичной цифре
        #        +: Квантификатор: соответствует предыдущему элементу 1 или более раз
        #
        #    \(|\): открывающая или закрывающая скобка
        #    |\+|\-|\*|\/: или + или - или * или /
        #    |np\. : "np."

        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+|\(|\)|\+|\-|\*|\/|np\.', string)

        result_str = ""

        for x in words:
            if x == "+":
                result_str += "_plus_"
                continue
            if x == "-":
                result_str += "_minus_"
                continue
            if x == "*":
                result_str += "_._"
                continue
            if x == "/":
                result_str += "_div_"
                continue

            if x == " ":
                result_str += "_"
                continue

            if x == "np":
                continue

            result_str += x

        return result_str
        #return '_'.join(map(str.lower, words))
