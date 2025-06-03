import numpy as np
from PIL import Image
import os
import filetype

def contrast_value():
    correct = False
    contrast = ""
    min_contrast = 10
    max_contrast = 0
    while(correct != True):
        # Я бы взял минимальную и максимальные значения контраста в переменную, и воспользовался бы f-строкой
        # input(f"Enter a contrast value (from min = {min_constrast} to max = {max_contrast}")
        # чтобы когда ты вздумаешь поменять эти значения, тебе бы не пришлось менять все значения, и ещё не дай бог ошибиться где-нибудь

        # А, я не знала про f-строки
        contrast = input(f"Enter a contrast value (from min = {min_contrast} to max = {max_contrast}):\t")
        try:
            if not contrast.isdigit():
                raise Exception("The contrast value must be set by a number!")
            contrast = int(contrast)
            if contrast < max_contrast or contrast > min_contrast:
                raise Exception("The entered contrast value is outside the range!")
            correct = True
        except Exception as err: # здесь (как и везде в коде нужен только один except для всех raise)
                                # Согласна, я дебилъ
            print("ERROR! ", err)
            exit(-1)
    return contrast

def path_to_original_image():
    correct = False
    path = ""
    while (correct != True):
        path = input("Enter the full path to the original image (for example: D:\\flower.png):\t")
        try:
            if not os.path.exists(path):
                raise Exception("The path is set incorrectly!")
            if not filetype.is_image(path):
                raise Exception("The file is not an image!")
            correct = True
        except Exception as err:
            print("ERROR! ", err)
            exit(-1)

    return path

def width_image():
    correct = False
    width = 0
    while (correct != True):
        width = input("Enter the width of the creating image:\t")
        try:
            if not width.isdigit():
                raise Exception("The width value must be set by a number!")
            correct = True
            width = int(width)
        except Exception as input_err:
            print("ERROR! ", input_err)
            exit(-1)

    return width

def ASCII_image_out(contrast, path, width, to_File, ratio_symbol):
    # маловато символов, и последние 5 сливаются вместе, также последний символ не входит в ASCII, из-за чего он может нормально не прочитаться

    # Мм, ну есть ещё такой набор, но мне результат меньше понравился
    #ASCII_SYMBOLS = "  .'`^,:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    ASCII_SYMBOLS = "  .,:;^!+*?]S%&8#@$№"
    ASCII_SYMBOLS = ASCII_SYMBOLS[:len(ASCII_SYMBOLS) - contrast]
    max_contrast = len(ASCII_SYMBOLS) - 1

    image = Image.open(path)
    image = image.convert('L')

    original_width = image.size[0]
    original_height = image.size[1]

    if to_File:
        # почему для файла минимум 180?
        # Потому что в строке окна может уместиться 180 символов. Если указать размер больше, то символы начнут переноситься на другую строку и изображение не получится
        if width > 180:
            width_for_file = 180
        else:
            width_for_file = width

    ratio = original_height / original_width
    height = int(width * ratio * ratio_symbol) # почему 0.35 и 0.45?
                                                # Потому что соотношение сторон символа не 1:1, а очень-очень приблизительно 1:2.
                                                # Чтобы изображение не искажалось, надо умножать на 0.35 для консоли или на 0.45 для файла
                                                # (почему разное значение для файла и консоли, я не особо понимаю, но если устанавливать одинаковое,
                                                # то в одном из источников вывода изображение будет сжиматься заметно сильнее)
    image = image.resize((width, height))
    arr_pixels = np.array(image)

    ASCII_image = ""
    for i in range(height):
        for j in range(width):
            brightness = arr_pixels[i, j]
            k = int(np.ceil(brightness / 256 * max_contrast))
            ASCII_image += ASCII_SYMBOLS[max_contrast - k]
        ASCII_image += '\n'
    return ASCII_image


def save_to_file(contrast, path, width):
    correct = False
    need_to_save = ""
    while (correct != True):
        need_to_save = input("Do you want to save the image to a file? (write yes/no):\t")
        try:
            if need_to_save.lower() != "yes" and need_to_save.lower() != "no":
                raise Exception("The answer is incorrect!")
            correct = True
        except Exception as input_err:
            print("ERROR! ", input_err)
            exit(-1)


    if need_to_save.lower() == "no":
        return

    correct = False
    path_to_save = ""
    while (correct != True):
        path_to_save = input("Enter the directory to save the image (for example: D:\\new_folder):\t") # directory или folder :)
        try:
            if not os.path.exists(path_to_save):
                raise Exception("The path is set incorrectly!")
            correct = True
        except Exception as err:
            print("ERROR! ", err)
            exit(-1)

    file_name = input("Enter the file name (for example: new_picture):\t")  # directory или folder :)
    file_result = open(path_to_save + "/" + file_name + ".txt", "w")
    ASCII_image_for_file = ASCII_image_out(contrast, path, width, True, 0.45)
    file_result.write(ASCII_image_for_file)
    return

def main():
    contrast = contrast_value()
    path = path_to_original_image()
    width = width_image()

    ASCII_image = ASCII_image_out(contrast, path, width, False, 0.35)
    print(ASCII_image)

    save_to_file(contrast, path, width)

if __name__ == "__main__":
    main()


