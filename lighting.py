from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Lighting:

    def __init__(self, position, ambient, diffuse):
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse

    def setlighting(self, light):
        glLightfv(light, GL_POSITION, self.position)
        glLightfv(light, GL_AMBIENT, self.ambient)
        glLightfv(light, GL_DIFFUSE, self.diffuse)


class Material:

    def __init__(self, color, specular, shininess, emission):
        self.color = color
        self.specular = specular
        self.shininess = shininess
        self.emission = emission

    def setmaterial(self):
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.color)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.shininess)
        glMaterialfv(GL_FRONT, GL_EMISSION, self.emission)


LIGHT_DEFAULT = Lighting(
    [0, 10, 0, 0],
    [0.4, 0.4, 0.4, 1],
    [0.5, 0.5, 0.5, 1]
)

MATERIAL_GROUND = Material(
    [0.8, 0.8, 0.8, 1],
    [0, 0, 0, 0],
    [0],
    [0, 0, 0, 0]
)

MATERIAL_OBJECT = Material(
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [40],
    [0, 0, 0, 0],
)
