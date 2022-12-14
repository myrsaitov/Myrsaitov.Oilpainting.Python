import re


# Преобразует обычную строку в snake_case
def to_snake_case(string):

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

    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', string)

    return '_'.join(map(str.lower, words))
