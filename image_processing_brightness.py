import numpy as np

from functional_privitive import functional_primitive


# https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color
# https://stackoverflow.com/questions/14259912/calculate-dynamic-range-of-an-image#:~:text=The%20dynamic%20range%20is%2020,divided%20by%20the%20noise%20floor.

def brightness_processing_wrapper(
    output_path_root,
    image
):

    image_processing_brightness(
        "Brightness: Fast Algorithm",
        output_path_root,
        image
    )


def image_processing_brightness(
        title,
        output_path_root,
        image
):
    functional_primitive(
        title,
        output_path_root,
        get_brightness,
        return_if_folder_exists=False,
        *image,
        *lambda r, g, b: sum([r, g, b]) / 3
    )


def get_brightness(
        output_path_root,
        image,
        lambda_func
):

    y_max, x_max, z = image.shape

    brightness = []

    for x in range(1, x_max):
        for y in range(1, y_max):
            try:
                pixel = image[x, y]
                r, g, b = pixel
                brightness.append(lambda_func(r, g, b))

            except IndexError:
                pass

    dynamic_range = round(np.log2(max(brightness)) - np.log2(min(brightness)), 2)

    f = open(output_path_root + '/dynamic_range.txt', 'w')
    f.write('Dynamic range: ', dynamic_range, 'EV (fast)\n')
    f.close()

    return dynamic_range
