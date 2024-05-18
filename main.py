import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from skimage.io import imread
from skimage.filters import threshold_multiotsu

from PIL import Image

PATH = "solda.png"

def otsu_histogram(im:object, thresholds: tuple):
    ...

def binary_threshold(im:object)->object:
    image = Image.fromarray(np.uint8(im)).convert('L')
    (l, h) = image.size

    out = Image.new(mode='L', size=(l, h))

    for j in range(0, h):
        for i in range(0, l):
            if image.getpixel((i, j)) > 1:
                out.putpixel(
                    (i, j),
                    1055
                )
            else:
                out.putpixel(
                    (i, j),
                    0
                )

    return out

def threshold(im:object)->object:
    thresholds = threshold_multiotsu(im)
    regions = np.digitize(image, bins=thresholds)

    return binary_threshold(regions)

def zero_frame(im:object)->object:
    (l, h) = im.size

    M = l + 2
    N = h + 2

    out = Image.new(mode='L', size=(M, N))

    for i in range(0, M):
        for j in range(0, N):
            if i == 0 and 0 <= j <= N:
                out.putpixel((i, j), 0)
            elif i == M - 1 and 0 <= j <= N - 1:
                out.putpixel((i, j), 0)
            elif 0 <= i <= M and j == 0:
                out.putpixel((i, j), 0)
            elif 0 <= i <= M - 1 and j == N - 1:
                out.putpixel((i, j), 0)
            else:
                out.putpixel((i, j), im.getpixel((i - 2, j - 2)))
    return out

def NO(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate

    if im.getpixel((i - 1, j - 1)) == size:
        return True
    return False

def N(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i - 1, j)) == size:
        return True
    return False

def NE(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i - 1, j + 1)) == size:
        return True
    return False

def O(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i, j - 1)) == size:
        return True
    return False

def L(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i, j + 1)) == size:
        return True
    return False

def SO(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i + 1, j - 1)) == size:
        return True
    return False

def S(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i + 1, j)) == size:
        return True
    return False

def SE(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i + 1, j + 1)) == size:
        return True
    return False

def calculate_coordinate(im, coordinate:tuple, size:int)->bool:
    list_cordinate_functions = [NO, N, NE, O, L, SO, S, SE]
    list_pixels = [] # [NO, N, NE, O, L, SO, S, SE]

    for fi in list_cordinate_functions:
        list_pixels.append(fi(im, coordinate, size))

    return True in list_pixels

def lettering_counting(im:object)->tuple:
    list_components = [1]

    (l, h) = im.size

    out = Image.new(mode='L', size=(l, h))

    components = 1

    for j in range(1, h - 1):
        for i in range(1, l - 1):
            if calculate_coordinate(im, (i, j), 255):
                out.putpixel((i, j), 106 + components)
            elif im.getpixel((i, j)) != 0:
                components += 1
                list_components.append(components)
                out.putpixel((i, j), 0)

    return (out, list_components)

def identifica_side(im:object)->list:
    list_component = []
    
def remove_side_component(im:object, list_componentes:list)->object:
    ...

def open_image(im:str, gray:bool = True)->object:
    return imread(im, as_gray=gray)

if __name__ == "__main__":
    image = open_image(PATH, True)

    image = threshold(image)

    image.save("results/threshold.jpg")

    zero_image = zero_frame(image)

    zero_image.save("results/zero_image.jpg")

    (components_image, list_components) = lettering_counting(zero_image)

    print(list_components)

    plt.imshow(components_image)
    plt.savefig("results/components_image.jpg")
    plt.show()