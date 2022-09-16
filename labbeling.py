from random import randint
from sys import argv

import numpy as np
from PIL import Image


class Label():
    def __init__(self, img: str):
        self.img = Image.open(img)
        self.width, self.height = self.img.size
        self.array = np.asarray(self.img)

    def operation(self):
        lines = self.height
        columns = self.width
        array = self.array

        labels = {}
        pixels = {}

        i = 0

        for l in range(0, lines):
            for c in range(0, columns):
                px = array[l][c]
                left = array[l][c - 1]
                up = array[l - 1][c]

                if not c - 1 in range(0, columns):
                    left = True

                if not l - 1 in range(0, lines):
                    up = True

                if px:
                    continue

                if left and up:
                    labels[i] = [(l, c)]
                    pixels[(l, c)] = i

                    i += 1

                else:
                    if not left and not up:
                        labels[pixels[(l - 1, c)]].append((l, c))
                        pixels[(l, c)] = pixels[(l - 1, c)]

                        if pixels[(l, c - 1)] != pixels[(l - 1, c)]:
                            labels[pixels[(l - 1, c)]
                                   ] += labels[pixels[(l, c - 1)]]

                            del labels[pixels[(l, c - 1)]]

                            for pixel in pixels.keys():
                                if pixels[pixel] == pixels[(l, c - 1)]:
                                    pixels[pixel] = pixels[(l - 1, c)]

                    elif left and not up:
                        labels[pixels[(l - 1, c)]].append((l, c))
                        pixels[(l, c)] = pixels[(l - 1, c)]

                    elif up and not left:
                        labels[pixels[(l, c - 1)]].append((l, c))
                        pixels[(l, c)] = pixels[(l, c - 1)]

        return labels

    def howManyObjects(self):
        print(f"\nNúmero de objetos encontrados: {len(self.operation())}.")

    def colorizeObjects(self):
        img = self.img.convert("RGB")
        array = np.asarray(img)
        labels = self.operation()

        for label in labels.keys():
            r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
            for pixel in labels[label]:
                l, c = pixel
                array[l][c] = r, g, b

        out = Image.fromarray(array)
        out.save("output.jpg", "JPEG")


if len(argv) < 2:
    print("É preciso informar os argumentos por linha de comando!\n")
    print("O primeiro argumento é, necessariamente, o nome da imagem binária (bitmap).")
    print("Ex : \"python3 " + argv[0] + " image.bmp [operation(s)]\"\n")

    print("As operações são: \n")
    print("'--colorize':  Colore os objetos encontrados com cores aleatórias.")
    print("'--how-many':  Retorna o número de objetos encontraddos.")

    exit(0)

image = argv[1]

if "--colorize" in argv:
    print("Colorindo...")
    Label(image).colorizeObjects()

if "--how-many" in argv:
    print("Contando objetos...")
    Label(image).howManyObjects()
