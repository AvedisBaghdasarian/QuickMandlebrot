##in this scipt all complex numbers are represented by 2-tuples (yes I know numpy natively handles complex numbers but I though that this would make it faster but it doesnt bc tuple overhead)

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from PIL import Image

# center = (-1.75291, 0.01255)
# deltax = 6.2*10**-4
center = (0,0)
deltax = 4
ratio = 1
deltay = deltax/ratio
pix_length = int(1000)
pix_height = int(pix_length/ratio)

iter = 10



##necessary math
def sigmoid(x):
  return 2 / (1 + math.exp(-x)) - 1

def cadd(x, y):
    a , b = x[:]
    c , d = y[:]
    result = (a+c, b+d)
    return result

def cmult(x, y):
    a , b = x[:]
    c , d = y[:]
    result = (a*c-b*d,a*d+b*c)
    return result

def cnormsquare(x):
    a,b = x[:]
    result = a**2 + b**2
    return result



##takes pixels to the complex plane
def pix_to_comp(pix, center, deltax, deltay, pix_length, pix_height):
    px = pix[0]
    py = pix[1]
    deltay = ratio*deltax
    x = (px-pix_length/2)/pix_length*deltax + center[0]
    y = (pix_height/2-py)/pix_height*deltay + center[1]
    return (x,y)

##takes values on the complex plane back to pixels
def comp_to_pix(coor, center, deltax, deltay, pix_length, pix_height):
    cx = coor[0]
    cy = coor[1]
    deltay = ratio*deltax
    px = int(np.round((cx - (center[0] - deltax / 2)) * pix_length / deltax))
    py = int(np.round(-(cy - (center[1] + deltay / 2)) * pix_height / deltay ))
    return (px,py)



##canonical mandlebrot test, takes arg on complex plane
def mandle(c):
    z = (0,0)
    for i in range(iter):
        zquare = cmult(z, z)
        z = cadd(zquare, c)
        if cnormsquare(z) >= 4:
            return i
    return -1

##snakey mandlebrot test, takes arg pixel number




def mandlesnake(c, origin):
    z = pix_to_comp(c, center, deltax, deltay,  pix_length, pix_height)
    zquare = cmult(z, z)
    z = cadd(zquare, z)
    if cnormsquare(z) >= 4:
        return "escape"
    # if z == origin:
    #     return -1
    # print(pix_to_comp(c, center, deltax, deltay,  pix_length, pix_height), z)
    g = comp_to_pix(z, center, deltax, deltay,  pix_length, pix_height)
    return g



##maps escape values to a color
def colormap(escape):
    if escape == -1:
        color = np.zeros(3)
    else:
        color = np.array([255, 50, 0]) * sigmoid(escape*2/iter)
    return color

def count(arg, px):
    if px[1] == 0:
        os.system('cls')
        print(px[0])
    return arg



##moves through points given an origin, when it encounters a loop or an esacpe, enumerates the dictionary
def enumerate(esacpe_dict, origin, pos, n):
    n += 1
    newpos = escape_dict.get(pos, "none")
    if newpos == "none":
        newpos = mandlesnake(pos, origin)
        if newpos == "escape":
            escape_dict[pos] = 1
            indexer = origin
            while n >= 2:
                indexer_temp = escape_dict[indexer]
                escape_dict[indexer] = n
                indexer = indexer_temp
                n -= 1
        else:
            escape_dict[pos] = newpos
            pos = newpos
            enumerate(escape_dict, origin, pos, n)
    else:
        if newpos == -1:
            indexer = origin
            while n >= 1:
                indexer_temp = escape_dict[indexer]
                escape_dict[indexer] = -1
                indexer = indexer_temp
                n -= 1
        elif isinstance(newpos, int):
            indexer = origin
            n += newpos
            while n > newpos:
                indexer_temp = escape_dict[indexer]
                escape_dict[indexer] = n
                indexer = indexer_temp
                n -= 1
        else:
            indexer = origin
            while n >= 1:
                indexer_temp = escape_dict[indexer]
                escape_dict[indexer] = -1
                indexer = indexer_temp
                n -= 1

    return 0








##populates dictionary for normal mandlebrot set

# escape_dict = {(i,j): count(mandle(pix_to_comp((i,j), center, deltax, deltay,  pix_length, pix_height)), (i, j))  for i in range(int(pix_length)) for j in range(int(pix_height))
#     }
#


##generates escape dictionary snakely
escape_dict_snake = {}
for i in range(int(pix_length-1)):
    for j in range(int(pix_height-1)):

        if escape_dict.get((i,j), "none") == "none":
            enumerate(escape_dict_snake, (i,j), (i, j), 0)

#generates image from dictionarry
bitmap = np.zeros((pix_length, pix_height, 3), dtype = np.uint8)
for i in escape_dict.keys():
    if i[0] < pix_length and i[1] < pix_height:
        bitmap[i[0], i[1], :] = colormap(escape_dict_snake[i])

img = Image.fromarray(bitmap, 'RGB')
img.save('bro.png')
img.show()
