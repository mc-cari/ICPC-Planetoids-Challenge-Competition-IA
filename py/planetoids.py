#!/usr/bin/env python3
# ^^^ Important - tells kattis this is python3 vs python2

import sys
import json
import math
from io import open
from random import random


def ang(x, y):

    a = math.atan2(y, x)
    b = math.atan2(y, x)
    if (a < 0):
        a += 2.0 * math.pi
    return a

def rad(d):
    return d*math.pi / 180.0

def cross(x1, y1, x2, y2):
    return x1 * y2 - y1 * x2

def dist(x1, y1, x2, y2):
  return math.sqrt((x1-x2)*(x1-x2)+ (y1-y2)*(y1-y2)) 

def angbs(a, b):
    return min(abs(a - b), 2*math.pi - abs(a - b))

class Dim:
    def __init__(self, xo, yo, data):
        self.xa = xo - data["shipPos"][0]
        self.ya = yo - data["shipPos"][1]
        self.xo = xo
        self.yo = yo
        self.ang = ang(self.xa, self.ya)
        self.dist = dist(xo, yo, data["shipPos"][0], data["shipPos"][1])

W = 7600
H = 4300
preart = (-1, -1)
prepos = (-1, -1)
preasts = dict()
preufos = dict()
vart = (0, 0)
cont = 0
for i in range(100):
    preufos[i] = (-1, -1)
for i in range(200):
    preasts[i] = (-1, -1)
fps = 0
while True:
    
    raw_data = sys.stdin.readline()
    # Exit if stdin is closed.
    if not raw_data:
        break
    
    data = json.loads(raw_data)

    # Exit if we hit Game Over.
    if "gameOver" in data and data["gameOver"]:
        break

    # @TODO: Process input frame
    raw_data
    fps += 1
    arts = []
    arts.append(Dim(data["artfPos"][0], data["artfPos"][1], data))
    arts.append(Dim(data["artfPos"][0] + W, data["artfPos"][1], data))
    arts.append(Dim(data["artfPos"][0], data["artfPos"][1] + H, data))
    arts.append(Dim(data["artfPos"][0], data["artfPos"][1] - H, data))
    arts.append(Dim(data["artfPos"][0] - W, data["artfPos"][1], data))

    mini = 100000000
    
    chosed = 0
    arti = Dim(data["artfPos"][0], data["artfPos"][1], data)
    for art in arts:
        if art.dist < mini and (angbs(rad(data["shipR"]), art.ang)) < 0.55 and art.dist < 4500:
            arti = art
            mini = art.dist
            chosed = 1

    for art in arts:
        if art.dist < mini and not chosed:
            arti = art
            mini = art.dist

    ufos = []
    for ind, ufo in enumerate(data["ufoPos"]):

        vufo = (0, 0)
        if(preufos[data["ufoIds"][ind]] != (-1, -1)):
            vufo = (ufo[0] - preufos[data["ufoIds"][ind]][0], ufo[1] - preufos[data["ufoIds"][ind]][1])

        ux = ufo[0] + vufo[0]*4
        uy = ufo[1] + vufo[1]*4
        ufos.append(Dim(ux, uy, data))
        rate = 1.05
        if ufos[-1].dist > 1700 or angbs(ufos[-1].ang, arti.ang) > rate:
            ufos.pop()
        ufos.append(Dim(ux - W, uy, data))
        if ufos[-1].dist > 1700 or angbs(ufos[-1].ang, arti.ang) > rate:
            ufos.pop()
        ufos.append(Dim(ux + W, uy, data))
        if ufos[-1].dist > 1700 or angbs(ufos[-1].ang, arti.ang) > rate:
            ufos.pop()
        ufos.append(Dim(ux - W, uy + H, data))
        if ufos[-1].dist > 1700 or angbs(ufos[-1].ang, arti.ang) > rate:
            ufos.pop()
        ufos.append(Dim(ux, uy + H, data))
        if ufos[-1].dist > 1700 or angbs(ufos[-1].ang, arti.ang) > rate:
            ufos.pop()
        preufos[data["ufoIds"][ind]] = (ufo[0], ufo[1])

    for art in ufos:
        if art.dist < mini:
            arti = art
            mini = art.dist
    asts = []
    mini_ast = 10000000

    for ind, ast in enumerate(data["astPos"]):
        ad = 0
        if data["astSizes"][ind] == 48:
            ad = 120
        elif data["astSizes"][ind] == 49:
            ad = 190
        else:
            ad = 240
        asts.append(Dim(data["astPos"][ind][0], data["astPos"][ind][1], data))
        mini_ast = min(mini_ast, max(0, asts[-1].dist -ad))
        asts.pop()
        

        vast = (0, 0)

        if(preasts[data["astIds"][ind]] != (-1, -1)):
            vast = (ast[0] - preasts[data["astIds"][ind]][0], ast[1] - preasts[data["astIds"][ind]][1])

        ux = ast[0] + vast[0]*2.2
        uy = ast[1] + vast[1]*2.2
        asts.append(Dim(ux, uy, data))
 
        rate = 0.19
        if asts[-1].dist > 1700 or (angbs(asts[-1].ang, arti.ang) > rate):
            asts.pop()
        asts.append(Dim(ux - W, uy, data))
        if asts[-1].dist > 1700 or (angbs(asts[-1].ang, arti.ang) > rate) :
            asts.pop()
        asts.append(Dim(ux + W, uy, data))
        if asts[-1].dist > 1700 or (angbs(asts[-1].ang, arti.ang) > rate) :
            asts.pop()
        asts.append(Dim(ux - W, uy + H, data))
        if asts[-1].dist > 1700 or (angbs(asts[-1].ang, arti.ang) > rate) :
            asts.pop()
        asts.append(Dim(ux, uy + H, data))
        if asts[-1].dist > 1700 or (angbs(asts[-1].ang, arti.ang) > rate) :
            asts.pop()
        preasts[data["astIds"][ind]] = (ast[0], ast[1])
    
    for art in asts:
        if art.dist < mini:
            arti = art
            mini = art.dist
    for i in range(len(data["bulPos"])):
        if data["bulSrc"][i] != 48:
            asts.append(Dim(data["bulPos"][i][0], data["bulPos"][i][1], data))
            mini_ast = min(mini_ast, asts[-1].dist)
    

    ang2 = rad(data["shipR"])
    

    xr = math.cos(ang2)
    yr = math.sin(ang2)

    if(prepos != (-1, -1)):
        vart = (data["shipPos"][0] - prepos[0], data["shipPos"][1] - prepos[1])

    prepos = (data["shipPos"][0], data["shipPos"][1])

    
    if angbs(ang(xr + vart[0], yr + vart[1]), ang2) > 0.3 and dist(data["artfPos"][0], data["artfPos"][1],data["shipPos"][0], data["shipPos"][1]) >450:
        ang2 = ang(xr + vart[0], yr + vart[1])
    

    if(preart == (-1, -1)):
        preart = (data["artfPos"][0], data["artfPos"][1])
    elif preart != (data["artfPos"][0], data["artfPos"][1]):
        preart = (data["artfPos"][0], data["artfPos"][1])
        cont = 30
    dist_art = dist(data["artfPos"][0], data["artfPos"][1],data["shipPos"][0], data["shipPos"][1])
    hyp = "0"
    if(((mini_ast < 50 and not mini < 1600) or mini > 3000)  and not chosed):
        hyp = "1"
    mov = "0"
    if(angbs(arti.ang, ang2) < 0.4) or (arti.dist > 3500 and fps%5 == 0):
        mov = "1"
    if(angbs(arti.ang, ang2) < 0.05):

        mov = "1"
        sys.stdout.write(f"{mov}001{hyp}1\n")

    
    elif cross(xr, yr, arti.xa, arti.ya) >= 0:
        
        sys.stdout.write(f"{mov}011{hyp}1\n")
    else:
        sys.stdout.write(f"{mov}101{hyp}1\n")
    # Emit command.
    cont -= 1
    cont = max(cont, 0)
    
    sys.stdout.flush()