import sys
import pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *
from filter_hsv import Webcam

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

webcam = Webcam()
model_3D = "sonic-series-amy-rose.obj"

pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)

# Загрузка объекта
obj = OBJ(model_3D, swapyz=True)

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(90.0, width / float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry = (180, 90)
tx, ty = (0, 0)
zpos = 5
rotate = move = False
run = True
while run:
    for e in pygame.event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            run = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                zpos = max(1, zpos - 1)
            elif e.button == 5:
                zpos += 1
            elif e.button == 1:
                rotate = True
            elif e.button == 3:
                move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                rotate = False
            elif e.button == 3:
                move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j

    # управление волшебной палочкой
    cord = webcam.update_frame()
    if cord:
        rx, ry = cord

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslate(tx / 20., ty / 20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glCallList(obj.gl_list)

    pygame.display.flip()
    clock.tick(30)

sys.exit(0)
