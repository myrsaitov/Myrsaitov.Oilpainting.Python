import sys
import getopt
import cv2
import pathlib
import morphological_image_processing


# Определение функции main
def main(argv):
    input_path = ''
    output_path = ''

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

    # TODO find files in SRC dir
    filename = "image1.jpg"
    output_path += "/" + filename[:-4]

    # Создает папку, если ее не существует
    pathlib\
        .Path(output_path)\
        .mkdir(parents=True, exist_ok=True)

    # Открывает исходный файл
    image = cv2.imread(
        input_path + "/" + filename,
        1)

    #################################################
    # Morphological Image Processing
    #################################################
    for size in range(1, 10):
        morphological_image_processing.main(
            output_path,
            size,
            image)

    # Выход из программы
    sys.exit()


# Переменная __name__ - это специальная переменная,
# которая будет равна "__main__", только если файл
# запускается как основная программа, и выставляется
# равной имени модуля при импорте модуля.
# То есть, условие if __name__ == '__main__' проверяет,
# был ли файл запущен напрямую.
if __name__ == "__main__":
    main(sys.argv[1:])
