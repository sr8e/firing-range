from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

from lighting import LIGHT_DEFAULT, MATERIAL_GROUND, MATERIAL_OBJECT
from control import Player
from ui import drawUI
from sound import Sound


# class to manage windowsize
class Window:
    def __init__(self, w, h):
        self._w = w
        self._h = h

    @property
    def size(self):
        return(self._w, self._h)

    @property
    def center(self):
        return tuple([int(v / 2) for v in self.size])

    @property
    def aspect(self):
        return self._w / self._h


window = Window(1600, 900)

# perspective parameters
FAR_DIST = 100
FOV = 100

# initialize sounds
sound = Sound()
sound.set_gain(0.1)

player = Player(window, 0, 0, math.pi / 2, 0, sound)


def main():
    init()
    glutMainLoop()


# initialize opengl
def init():
    """ initialize """
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(*window.size)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("射撃訓練場".encode('sjis'))
    glClearColor(0.59, 0.9, 0.95, 1.0)

    # setting callback functions
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(player.mouse)
    glutPassiveMotionFunc(None)
    glutMotionFunc(None)
    glutKeyboardFunc(player.keyboard)
    glutKeyboardUpFunc(player.keyboardup)
    glutIdleFunc(redisplay)

    # setting timers
    glutTimerFunc(10, player.move, 0)
    glutTimerFunc(10, player.strafe, 4)

    # lightings
    LIGHT_DEFAULT.setlighting(GL_LIGHT0)

    # settings
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glutSetKeyRepeat(GLUT_KEY_REPEAT_ON)


def display():
    # clear buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # ready to render 3d objects
    glMatrixMode(GL_MODELVIEW)

    # render ground grid
    glDisable(GL_LIGHTING)
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_LINES)
    edge_dist = FAR_DIST // 4
    for x in range(-edge_dist, edge_dist, 2):
        glVertex3d(x, 0, -edge_dist)
        glVertex3d(x, 0, edge_dist)
    for z in range(-edge_dist, edge_dist, 2):
        glVertex3d(-edge_dist, 0, z)
        glVertex3d(edge_dist, 0, z)
    glEnd()
    glEnable(GL_LIGHTING)

    # render ground surface
    MATERIAL_GROUND.setmaterial()
    glNormal3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3d(-edge_dist, 0, edge_dist)
    glVertex3d(edge_dist, 0, edge_dist)
    glVertex3d(edge_dist, 0, -edge_dist)
    glVertex3d(-edge_dist, 0, -edge_dist)
    glEnd()

    # render teapot
    MATERIAL_OBJECT.setmaterial()
    glPushMatrix()
    glTranslate(0, 1, 5)
    glutSolidTeapot(1)
    glPopMatrix()

    # render other objects
    player.draw()

    # prepare for 2d rendering
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    w, h = window.size
    glOrtho(0, w, 0, h, 0, 1)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    # ready to render 2d objects
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # render 2d UI
    drawUI(window, player)

    # set camera for 3d view
    glEnable(GL_DEPTH_TEST)  # enable shading
    glEnable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV, window.aspect, 0.1, FAR_DIST)
    player.look()

    # refresh display
    glutSwapBuffers()
    glFlush()  # enforce OpenGL command


def reshape(width, height):
    """callback function resize window"""
    window = Window(width, height)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV, window.aspect, 0.1, 100.0)


def redisplay():
    glutPostRedisplay()


if __name__ == "__main__":
    main()
