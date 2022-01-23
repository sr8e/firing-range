import random
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from util import add, clamp, distance, ground, length, travel, scalar, sub


EYE_HEIGHT = 2
HEAD_RADIUS = 0.3

DAMAGE = 13
HEAD_COEF = 1.5
MAX_HEALTH = 100
SHIELD_POINT = 25
MAX_SHIELD_LV = 5
MIN_SHIELD_LV = 2

STRAFE_SPEED = 4
STRAFE_TURN_THRES = 0.01


class Dummy:

    def __init__(self, x, z, shield_lv):
        self.x = x
        self.z = z
        self.health = MAX_HEALTH
        self.shield_lv = clamp(shield_lv, MAX_SHIELD_LV, MIN_SHIELD_LV)
        self.shield = self.shield_lv * SHIELD_POINT

        self.strafe_dir = 1
        self.prevtime = time.monotonic()

    # drawing
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, 0, self.z)
        glRotatef(90, -1, 0, 0)
        glutSolidCylinder(HEAD_RADIUS, EYE_HEIGHT - HEAD_RADIUS, 20, 20)
        glRotatef(90, 1, 0, 0)
        glTranslatef(0, EYE_HEIGHT, 0)
        glutSolidSphere(HEAD_RADIUS, 20, 20)
        glPopMatrix()

    # hit check
    def hitCheck(self, direction, direction_gr, origin):
        head_pos = (self.x, EYE_HEIGHT, self.z)

        diff = sub(head_pos, origin)
        dist = distance(diff, direction)
        traveled = travel(diff, direction)

        diff_gr = ground(diff)

        dist_gr = distance(diff_gr, direction_gr)
        traveled_gr = travel(diff_gr, direction_gr)

        if dist < HEAD_RADIUS and traveled > 0:
            return (2, traveled_gr)

        if dist_gr < HEAD_RADIUS and traveled_gr > 0:

            coef = traveled_gr / length(direction_gr)
            end = add(origin, scalar(coef, direction))
            if 0 < end[1] < EYE_HEIGHT - HEAD_RADIUS:
                return (1, traveled_gr)

        return (0, None)

    # damage calculate
    def damage(self, hittype):
        dmg = DAMAGE if hittype == 1 else DAMAGE * HEAD_COEF
        if self.shield >= dmg:
            self.shield -= dmg
            return (3, self.shield_lv, dmg)

        crack = self.shield > 0

        dmg_p = dmg - self.shield
        self.shield = 0

        if self.health > dmg_p:
            self.health -= dmg_p
            return (2 if crack else 1, 0, dmg)
        else:
            dmg_last = self.health
            self.health = 0
            return (0, 0, dmg_last)

    # strafing
    def strafe(self, targetpos, pause):
        now = time.monotonic()
        dt = now - self.prevtime

        if pause:
            self.prevtime = now
            return

        selfpos = (self.x, self.z)
        diff = sub(ground(targetpos), selfpos)
        normal = (diff[1], -diff[0])

        r = random.random()
        if r < STRAFE_TURN_THRES:
            self.strafe_dir *= -1

        self.x, self.z = add(
            selfpos,
            scalar(self.strafe_dir * STRAFE_SPEED / length(normal) * dt, normal)
        )

        self.x = clamp(self.x, 25, -25)
        self.z = clamp(self.z, 25, -25)

        self.prevtime = now
