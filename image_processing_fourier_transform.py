import os
import pathlib

import cv2
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

def fourier_processing_wrapper(
    output_path_root,
    image
):

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





def fourier_processing(
    main_title,
    output_path_root,
    gray_image,
    filter_lambda_function,
    freqs
):

    print("*****************************************************")
    print("Starting: ", main_title)
    print("*****************************************************")

    # ???????? ?? ?????????????????????? ????????????
    output_path = output_path_root + \
                  "/" + to_snake_case(main_title)

    # ???????? ?????????? ????????????????????, ???? ???????????????? ???? ??????????????????
    if os.path.exists(output_path):
        print("The folder exists! The old version remains!")
        return
    else:
        # ?????????????? ??????????, ???????? ???? ???? ????????????????????
        pathlib \
            .Path(output_path) \
            .mkdir(parents=True, exist_ok=True)

    # ???????????? ???????????????????????? ?????????????????? ?????? ???????????????????? ??????????????????????
    figure_size = (6.4 * 5, 4.8 * 5)  # (6.4 * 25, 4.8 * 25))

    # ?????????????????????????? ?????????????????? ???????????????????? ????????????????
    plt.figure(figsize=figure_size, constrained_layout=False)

    for freq in freqs:
        fourier_image_processing(
            output_path,
            gray_image,

            # (1) ???????????????? ?????? ??????????????
            # (2) ???????????????? ?????? ???????????? ???????????? ???? ??????????????????
            # (3) ??????????????????
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
                    "Spectrum-2",
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
                    "Centered Spectrum multiply Filter" + "Freq" + str(freq).zfill(4),
                    lambda x: x * filter_lambda_function(freq, gray_image.shape),
                    lambda x: np.log(1 + np.abs(x))
                ],

                [
                    "Decentralize" + "Freq" + str(freq).zfill(4),
                    lambda x: np.fft.ifftshift(x),
                    lambda x: np.log(1 + np.abs(x))
                ],

                [
                    "Processed Image" + "Freq" + str(freq).zfill(4) ,
                    lambda x: np.fft.ifft2(x),
                    lambda x: np.abs(x)
                ]

            ]

        )


# ?????????????? ?????????????????? ?????????????????? ????????????
def fourier_image_processing(
    output_path,
    gray_image,
    process_options
):

    # ???????????? ???????????? ?????????? ????????????????????
    data = gray_image

    # ?? ?????????? ???????????????????????? ???????????? ?? ?????????????????? ??????????????
    for option in process_options:
        title, process_data, process_image = option
        data = process_data(data)

        # ?????? ?????????? ?? ????????????????
        filename = to_snake_case(title) + ".png"

        print("Processing: " + filename)

        # ???????? ???????? ????????????????????, ???? ???????????? ???? ????????????
        if os.path.exists(output_path + "/" + filename):
            print("The file exists! The old version remains!")
            continue

        # ????????????????????
        plt.imshow(process_image(data).astype(np.uint8), "gray"), plt.title(title)

        # ????????????????????
        plt.savefig(
            output_path + '/' + filename,
            dpi=300,
            format='png',
            bbox_inches='tight')

    plt.show()

    print()
    print()
    print("*****************************************************")
    print("*****************************************************")
    print()
    print()


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
