import numpy as np
from math import ceil

import matplotlib
import matplotlib.pyplot as plt

from skimage.io import imread
from skimage.filters import threshold_multiotsu

from PIL import Image

from collections import deque

PATH = "solda.png"

def otsu_histogram(im:object, thresholds: tuple):
    ...

def binary_threshold(im:object)->object:
    image = Image.fromarray(np.uint8(im)).convert('L')

    (l, h) = image.size

    out = Image.new(mode='L', size=(l, h))

    for j in range(0, h):
        for i in range(0, l):
            if image.getpixel((i, j)) == 0:
                out.putpixel(
                    (i, j),
                    0
                )
            else:
                out.putpixel(
                    (i, j),
                    255
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
        return (i - 1, j - 1)
    return None

def N(im:object, coordinate:tuple, size:int)->tuple:
    (i, j) = coordinate
    
    if im.getpixel((i - 1, j)) == size:
        return (i - 1, j)
    return None

def NE(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i - 1, j + 1)) == size:
        return (i - 1, j + 1)
    return None

def O(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i, j - 1)) == size:
        return (i, j - 1)
    return None

def L(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i, j + 1)) == size:
        return (i, j + 1)
    return None

def SO(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i + 1, j - 1)) == size:
        return (i + 1, j - 1)
    return None

def S(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i + 1, j)) == size:
        return (i + 1, j)
    return None

def SE(im:object, coordinate:tuple, size:int)->bool:
    (i, j) = coordinate
    
    if im.getpixel((i + 1, j + 1)) == size:
        return (i + 1, j + 1)
    return None

def calculate_coordinate(im, coordinate:tuple, size:int)->list:
    list_cordinate_functions = [NO, N, NE, O, L, SO, S, SE]
    list_pixels = [] # [NO, N, NE, O, L, SO, S, SE]

    for fi in list_cordinate_functions:
        list_pixels.append(fi(im, coordinate, size))

    return [i for i in list_pixels if i != None]

def dfs(im:object, out:object, coordinate:tuple, components:int)->set:
    set_coordinates:set = set()
    queue:deque = deque()

    set_coordinates.add(coordinate)
    queue.append(coordinate)

    while queue:
        for i in range(len(queue)):
            (i, j) = queue.popleft()

            coordinates = calculate_coordinate(im, (i, j), 255)

            if len(coordinates) != 0:
                out.putpixel((i, j), components)
                for k in coordinates:
                    if k not in set_coordinates:
                        queue.append(k)
                    set_coordinates.add(k)

    return set_coordinates

def lettering_counting(im:object)->tuple:
    (l, h) = im.size

    components = 10

    list_components:list = [components]
    set_coordinates:set = set()

    out = Image.new(mode='L', size=(l, h))

    for j in range(1, h - 1):
        for i in range(1, l - 1):
            if im.getpixel((i, j)) != 0 and (i, j) not in set_coordinates:
               set_coordinates = set_coordinates.union(dfs(im, out, (i, j), components)) 
               components += 1
               list_components.append(components)
            elif im.getpixel((i, j)) == 0:
                out.putpixel((i, j), 0)

    return (out, list_components)

def identifica_side(im:object)->set:
    list_component = []

    (l, h) = im.size
    
    for i in range(1, l - 1):
        if calculate_coordinate(im, (i, 1), 0) and im.getpixel((i, 1)) != 0:
            list_component.append(im.getpixel((i, 1)))
        
        if calculate_coordinate(im, (i, h - 2), 0) and im.getpixel((i, h - 2)) != 0:
            list_component.append(im.getpixel((i, h - 2)))

    
    for j in range(1, h - 1):
        if calculate_coordinate(im, (1, j), 0) and im.getpixel((1, j)) != 0:
            list_component.append(im.getpixel((1, j)))
        
        if calculate_coordinate(im, (l - 2, j), 0) and im.getpixel((l - 2, j)) != 0:
            list_component.append(im.getpixel((l - 2, j)))

    return set(list_component)
    
def remove_side_component(im:object, list_componentes:list)->object:
    (l, h) = im.size

    out = Image.new(mode='L', size=(l, h))
                    
    for j in range(0, h):
        for i in range(0, l):
            if im.getpixel((i, j)) in list_componentes:
                out.putpixel((i, j), 0)
            else:
                out.putpixel((i, j), im.getpixel((i, j)))
    
    return out

def max_component(im:object, list_components:list)->int:
    (l, h) = im.size 
    dict_components = {}

    for i in list_components:
        dict_components[i] = 0

    for j in range(0, h):
        for i in range(0, l):
            if im.getpixel((i, j)) != 0:
                dict_components[im.getpixel((i, j))] += 1

    return list(dict_components.keys())[list(dict_components.values()).index(max(dict_components.values()))]

def center_of_mass_image(im:object, list_components:list)->tuple:
    (l, h) = im.size

    max_value = max_component(im, list_components)

    sum_x = 0
    cont_x = 0

    sum_y = 0
    cont_y = 0

    for j in range(0, h):
        for i in range(0, l):
            if im.getpixel((i, j)) == max_value:
                sum_y += j
                cont_y += 1

    for i in range(0, l):
        for j in range(0, h):
            if im.getpixel((i, j)) == max_value:
                sum_x += i
                cont_x += 1
        
    return (ceil(sum_x/cont_x), ceil(sum_y/cont_y))

def psudo_color(im: object):
    ...
    
def main(file: str):
    ...

def open_image(im:str, gray:bool = True)->object:
    return imread(im, as_gray=gray)



if __name__ == "__main__":
    image = open_image(PATH, True)

    threshold_image = threshold(image)

    threshold_image.save("results/binary_threshold.jpg")

    zero_image = zero_frame(threshold_image)

    zero_image.save("results/zero_image.jpg")

    (components_image, list_components) = lettering_counting(zero_image)

    components_image.save("results/components_threshold.jpg")
    
    list_components_side = list(identifica_side(components_image))
    # print(list_components_side)

    remove_side_component_image = remove_side_component(components_image, list_components_side)
    remove_side_component_image.save("results/remove_side_component_image.jpg")

    # print(max_component(remove_side_component_image, list_components))

    (i, j) = center_of_mass_image(remove_side_component_image, list_components)
    print(i, j)

    remove_side_component_image.putpixel((i, j), 255)

    for k in range(1, 5):
        remove_side_component_image.putpixel((i, j + k), 255)
        remove_side_component_image.putpixel((i, j - k), 255)
        remove_side_component_image.putpixel((i + k, j), 255)
        remove_side_component_image.putpixel((i - k, j), 255)

    plt.imshow(remove_side_component_image)

    plt.savefig("results/center_of_mass_image.jpg")
    remove_side_component_image.save("results/center_of_mass_image.jpg")

    plt.show()