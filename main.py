import sys
import getopt
import cv2
from image_save import image_save
from image_dilate import image_dilate


# Определение функции main
def main(argv):
    input_file = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('main.py -i <input_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <input_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg

    # Если входной файл не задан, то выход
    if input_file == "":
        print("Enter filename!")
        sys.exit()

    # Открывает исходный файл
    image = cv2.imread(input_file, 1)

    # Выполняет "Dilate"
    image_save(
        input_file,
        "dilated",
        image_dilate(image))

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
