import math
import random
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from dummy import Dummy
from util import add, clamp, sub


# mouse sensitivity
SENSITIVITY = 0.005

# camera height
EYE_HEIGHT = 2

# player moving speed
VELOCITY = 10

# interval between shots (ms)
FIRE_INTERVAL = 110

# directions to move (* pi rad)
ANGLES = [0, 0, 0.75, 0.5, 0.25, 1.25, 1.5, 1.75, 1]

# number of dummies on the world at a time
MAX_DUMMY_NUM = 5

# number of dummies need to beat
DUMMY_TO_BEAT = 20

# how far dummies spawn from player
INITIAL_RADIUS = 8


class Player:

    def __init__(self, window, x, z, phi, theta, sound):
        self.window = window
        self.x = x
        self.z = z
        self.phi = phi
        self.theta = theta
        self.dummies = [
            Dummy(
                INITIAL_RADIUS * math.cos(i * 2 * math.pi / MAX_DUMMY_NUM),
                INITIAL_RADIUS * math.sin(i * 2 * math.pi / MAX_DUMMY_NUM),
                random.randint(2, 5)
            )
            for i in range(MAX_DUMMY_NUM)
        ]
        self.sound = sound

        self.pause = True
        self.fire = False

        self.movement = [0, 0]
        self.prevtime = time.monotonic()
        self.damage_conseq = 0
        self.damage_shield = 0
        self.damage_total = 0
        self.last_target = None
        self.fired = 0
        self.hit = 0
        self.dummy_beated = 0
        self.dummy_alive = MAX_DUMMY_NUM

    # properties
    @property
    def position(self):
        return (self.x, EYE_HEIGHT, self.z)

    @property
    def direction(self):
        return (
            math.sin(self.phi) * math.cos(self.theta),
            math.cos(self.phi),
            math.sin(self.phi) * math.sin(self.theta)
        )

    @property
    def direction_horizontal(self):
        return (
            math.cos(self.theta),
            math.sin(self.theta)
        )

    @property
    def accuracy(self):
        if self.fired == 0:
            return 0
        return self.hit / self.fired * 100

    # windowsize reset
    def setWindow(self, window):
        self.window = window

    # events
    def mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.fire = True
                self.shot(2)
            elif state == GLUT_UP:
                self.fire = False

    def motion(self, x, y):
        center = self.window.center
        pos = (x, y)
        dx, dy = sub(pos, center)
        glutWarpPointer(*center)
        self.phi = clamp(self.phi + dy * SENSITIVITY, math.pi, 0)
        self.theta = (self.theta + dx * SENSITIVITY) % (math.pi * 2)
        glFlush()

    def keyboard(self, key, x, y):
        if key == b'\033':
            self.pause = not self.pause
            if self.pause:
                glutMotionFunc(None)
                glutPassiveMotionFunc(None)
                glutSetCursor(GLUT_CURSOR_LEFT_ARROW)
            else:
                glutMotionFunc(self.motion)
                glutPassiveMotionFunc(self.motion)
                glutSetCursor(GLUT_CURSOR_NONE)
                glutWarpPointer(*self.window.center)

        if self.pause:
            self.movement = [0, 0]
            return

        if key == b'w':
            self.movement[0] = 1
        elif key == b's':
            self.movement[0] = -1

        if key == b'a':
            self.movement[1] = -1
        elif key == b'd':
            self.movement[1] = 1

    def keyboardup(self, key, x, y):
        if key == b'w' and self.movement[0] == 1:
            self.movement[0] = 0
        if key == b's' and self.movement[0] == -1:
            self.movement[0] = 0
        if key == b'd' and self.movement[1] == 1:
            self.movement[1] = 0
        if key == b'a' and self.movement[1] == -1:
            self.movement[1] = 0

    # Repeating functions
    def move(self, value):
        glutTimerFunc(10, self.move, 1)
        now = time.monotonic()

        if (input_index := self.movement[0] + 3 * self.movement[1]) == 0:
            self.prevtime = now
            return

        d = self.direction_horizontal
        dt = now - self.prevtime
        th = ANGLES[input_index] * math.pi
        self.x += (d[0] * math.cos(th) - d[1] * math.sin(th)) * VELOCITY * dt
        self.z += (d[0] * math.sin(th) + d[1] * math.cos(th)) * VELOCITY * dt
        self.prevtime = now

    def shot(self, value):
        if self.pause:
            return

        self.sound.shot_source.play()
        self.fired += 1

        if self.fire:
            glutTimerFunc(FIRE_INTERVAL, self.shot, 3)

        min_dummy = (float('inf'), None, None)
        for dummy in self.dummies:
            ht, dist = dummy.hitCheck(
                self.direction,
                self.direction_horizontal,
                self.position
            )

            if ht > 0 and dist < min_dummy[0]:
                min_dummy = (dist, dummy, ht)

        if (target := min_dummy[1]) is not None:
            self.hit += 1
            hittype = min_dummy[2]
            damage_dealt = target.damage(hittype)
            soundtype, shield, damage = damage_dealt

            if soundtype == 3:
                if hittype == 2:
                    self.sound.shield_headshot_source.play()
                else:
                    self.sound.shield_source.play()
            elif soundtype == 2:
                self.sound.shield_break_source.play()
            elif soundtype == 1:
                if hittype == 2:
                    self.sound.headshot_source.play()
                else:
                    self.sound.flesh_source.play()
            else:
                self.sound.knockdown_source.play()

            if target is self.last_target:
                self.damage_conseq += damage

            else:
                self.damage_conseq = damage

            self.damage_shield = shield
            self.damage_total += damage
            self.last_target = target

        else:
            self.damage_conseq = 0

    def strafe(self, value):
        glutTimerFunc(10, self.strafe, 5)

        for d in self.dummies:
            d.strafe(self.position, self.pause)

    # rendering related
    def look(self):
        gluLookAt(
            *self.position,
            *add(self.position, self.direction),
            -math.cos(self.phi) * self.direction[0],
            1,
            -math.cos(self.phi) * self.direction[2]
        )

    def draw(self):
        self.dummies = [dummy for dummy in self.dummies if dummy.health > 0]
        self.dummy_beated += self.dummy_alive - len(self.dummies)
        self.dummy_alive = len(self.dummies)

        while (
            self.dummy_alive < MAX_DUMMY_NUM and
            (self.dummy_alive + self.dummy_beated) < DUMMY_TO_BEAT
        ):
            r = random.random()
            self.dummies.append(
                Dummy(
                    INITIAL_RADIUS * math.cos(r * 2 * math.pi),
                    INITIAL_RADIUS * math.sin(r * 2 * math.pi),
                    random.randint(2, 5)
                )
            )
            self.dummy_alive += 1

        for d in self.dummies:
            d.draw()
