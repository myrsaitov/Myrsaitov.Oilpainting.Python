import inspect
import os
import pathlib
import cv2
import numpy as np
import random

from matplotlib import pyplot as plt

from load_from_file_or_process_data import load_from_file_or_process_data
from to_snake_case import to_snake_case
from collections import namedtuple
from math import sqrt

try:
    import Image
except ImportError:
    from PIL import Image

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))


# https://habr.com/ru/post/156045/

# https://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/
# I've been using this method for a few years. A neat extension to it enables you to determine a "foreground" and "background color. The cluster with the most pixels near the center of the image is "foreground". The cluster with the most pixels near the edges is "background".

# Процедура, реализующая фильтр
def image_processing_get_dominate_colors(
        tittle,
        output_path_root,
        colors_count,
        image
):

    print("*****************************************************")
    print("Starting: ", inspect.currentframe().f_code.co_name, ": ", tittle)
    print("*****************************************************")

    ##############################################
    # Папка с результатами
    ##############################################

    # Путь к сохраняемым файлам
    output_path = output_path_root + "/" + to_snake_case(tittle)

    # Если папка существует, то действия не требуются
    if os.path.exists(output_path):
        print("The folder exists! The old version remains!")
        # return
    else:
        # Создает папку, если ее не существует
        pathlib \
            .Path(output_path) \
            .mkdir(parents=True, exist_ok=True)

    ##############################################
    # Сохраняет оригинал
    ##############################################

    original_image_path = output_path + "/__original_image.jpg"
    if not os.path.exists(original_image_path):
        # В массиве аргументов первым идет "image": argv[0]
        cv2.imwrite(original_image_path, image)

    ##############################################
    # Настройка координатной плоскости для построения гистограмм
    ##############################################

    # Размер координатной плоскости для построения результатов
    figure_size = (6.4 * 5, 4.8 * 5)  # (6.4 * 25, 4.8 * 25))

    ##############################################
    # Поиск доминирующих цветов
    ##############################################

    # Открывает изображение
    image = Image.open(original_image_path)

    # Получает точки
    points = load_from_file_or_process_data(
        output_path + '/__points_' + str(colors_count).zfill(2) + '.bin',
        get_points,
        image
    )

    # Поиск кластеров
    clusters = load_from_file_or_process_data(
        output_path + '/__clusters_' + str(colors_count).zfill(2) + '.bin',
        kmeans,
        points,
        colors_count,
        1
    )

    # Получает центры масс
    print("Starting: Get rgbs")
    rgbs = [map(int, c.center.coords) for c in clusters]

    # Получает список цветов
    colors = list(map(rtoh, rgbs))

    ##############################################
    # Построение гистограммы доминирущих цветов
    ##############################################
    print("Starting: Plot dominate colors")

    # Конфигурирует плоскость построения графиков
    plt.figure(figsize=figure_size, constrained_layout=False)

    fig, ax = plt.subplots()
    # Цвет фона координатных осей
    ax.set_facecolor('white')
    # Цвет фона
    fig.set_facecolor('white')

    # Построение гистограмм
    # https://www.delftstack.com/ru/howto/matplotlib/how-to-draw-rectangle-on-image-in-matplotlib/
    # https://pyprog.pro/mpl/mpl_bar.html
    x = colors
    y = np.empty(colors_count)
    y.fill(8)
    ax.bar(x, y, color=colors)

    # Наименование плоскости и координатных осей
    plt.title('Dominate colors')
    plt.xlabel("colors")
    # plt.ylabel('y')

    # Сохранение в файл
    plt.savefig(
        output_path + '/colors_' + str(colors_count).zfill(2) + '.png',
        dpi=300,
        format='png',
        bbox_inches='tight')

    # Очистка координатной плоскости
    plt.clf()

    ##############################################
    # Построение карты кластеров
    ##############################################
    print("Starting: Plot clusters")

    # Конфигурирует плоскость построения графиков
    plt.figure(figsize=figure_size, constrained_layout=False)

    fig, ax = plt.subplots()
    # Цвет фона координатных осей
    ax.set_facecolor('white')
    # Цвет фона
    fig.set_facecolor('white')

    # Наименование плоскости и координатных осей
    plt.title('Clusters')

    # Вывод точек покластерно
    cluster_index = 0
    for cluster in clusters:
        print("Cluster: ", cluster_index)
        count = 0

        # Plot Points
        for point in cluster.points:
            x = point.coords[0]
            y = point.coords[1]
            plt.scatter(
                x,
                y,
                marker='x',
                color=colors[cluster_index]
            )
            count += 1
            if count > 100:
                break

        # Plot Center
        x = cluster.center.coords[0]
        y = cluster.center.coords[1]
        plt.scatter(
            x,
            y,
            marker='o',
            color='black'
        )

        cluster_index += 1

    # Сохранение в файл
    plt.savefig(
        output_path + '/clusters_colors_count_' + str(colors_count).zfill(2) + '.png',
        dpi=300,
        format='png',
        bbox_inches='tight')

    # Очистка координатной плоскости
    plt.clf()


def get_points(image):

    # Если нужно уменьшить разрешение изображения
    image.thumbnail((200, 200))

    #  Point = namedtuple('Point', ('coords', 'n', 'ct'))
    points = []
    w, h = image.size
    for count, color in image.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points


def rtoh(rgb):
    return '#%s' % ''.join(('%02x' % p for p in rgb))


def euclidean(p1, p2):
    return sqrt(
        sum(
            [
                (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
            ]
        )
    )


def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)


def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters
