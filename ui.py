import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


shield_colors = [
    [1, 0, 0],
    [0, 0, 0],
    [0.5, 0.5, 0.5],
    [0, 0, 1],
    [0.8, 0, 0.8],
    [0.5, 0, 0]
]


def drawReticle(cx, cy):
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2d(cx - 10, cy)
    glVertex2d(cx + 10, cy)
    glVertex2d(cx, cy - 10)
    glVertex2d(cx, cy + 10)
    glEnd()


def drawCompass(cx, h, theta):
    glPushMatrix()
    glTranslated(cx - 27, h - 40, 0)
    glScaled(0.25, 0.25, 0)
    angle_str = f'{int(theta * 180 / math.pi):03}'
    for c in angle_str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
    glPopMatrix()
    glBegin(GL_LINE_STRIP)
    glVertex2d(cx - 45, h)
    glVertex2d(cx - 30, h - 50)
    glVertex2d(cx + 30, h - 50)
    glVertex2d(cx + 45, h)
    glEnd()


def drawDamage(cx, cy, damage, shield):
    glColor3f(*shield_colors[shield])
    glPushMatrix()
    glTranslated(cx + 20, cy + 20, 0)
    glScaled(0.2, 0.2, 0)
    damage_str = f'{int(damage)}'
    for c in damage_str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
    glPopMatrix()


def drawTotalDamage(w, h, totaldamage):
    glPushMatrix()
    glTranslated(w - 200, h - 40, 0)
    glScaled(0.2, 0.2, 0)
    damage_str = f'DAMAGE {int(totaldamage)}'
    for c in damage_str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
    glPopMatrix()

    glBegin(GL_LINE_STRIP)
    glVertex2d(w - 210, h)
    glVertex2d(w - 210, h - 50)
    glVertex2d(w, h - 50)
    glEnd()


def drawKills(w, h, kills):
    glPushMatrix()
    glTranslated(w - 400, h - 40, 0)
    glScaled(0.2, 0.2, 0)
    damage_str = f'KILLS {int(kills)}/20'
    for c in damage_str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
    glPopMatrix()

    glBegin(GL_LINE_STRIP)
    glVertex2d(w - 410, h)
    glVertex2d(w - 410, h - 50)
    glVertex2d(w - 210, h - 50)
    glEnd()


def drawAccuracy(h, accuracy):
    glPushMatrix()
    glTranslated(10, h - 40, 0)
    glScaled(0.2, 0.2, 0)
    acc_str = f'ACCURACY {accuracy:.2f}%'
    for c in acc_str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
    glPopMatrix()

    glBegin(GL_LINE_STRIP)
    glVertex2d(0, h - 50)
    glVertex2d(300, h - 50)
    glVertex2d(300, h)
    glEnd()


def drawPause(cx, cy):
    glPushMatrix()
    glTranslated(cx - 100, cy + 30, 0)
    glScaled(0.4, 0.4, 0)
    pause_str = 'PAUSED'
    for c in pause_str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
    glPopMatrix()


def drawUI(window, player):
    w, h = window.size
    cx, cy = window.center
    drawReticle(cx, cy)
    drawCompass(cx, h, player.theta)
    drawTotalDamage(w, h, player.damage_total)
    drawKills(w, h, player.dummy_beated)
    drawAccuracy(h, player.accuracy)

    if player.damage_conseq > 0:
        drawDamage(cx, cy, player.damage_conseq, player.damage_shield)

    if player.pause:
        drawPause(cx, cy)
