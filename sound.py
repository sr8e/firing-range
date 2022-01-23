from openal import *


PATH_PREFIX = 'sound/'
SHOT_SOUND = 'shot.wav'
SHIELD_SOUND = 'shield.wav'
SHIELD_BREAK_SOUND = 'shieldbreak.wav'
SHIELD_HEADSHOT_SOUND = 'shieldhead.wav'
FLESH_SOUND = 'flesh.wav'
HEADSHOT_SOUND = 'head.wav'
KNOCKDOWN_SOUND = 'knock.wav'


class Sound:

    def __init__(self):
        self.shot_source = oalOpen(PATH_PREFIX + SHOT_SOUND)
        self.shield_source = oalOpen(PATH_PREFIX + SHIELD_SOUND)
        self.shield_break_source = oalOpen(PATH_PREFIX + SHIELD_BREAK_SOUND)
        self.shield_headshot_source = oalOpen(PATH_PREFIX + SHIELD_HEADSHOT_SOUND)
        self.flesh_source = oalOpen(PATH_PREFIX + FLESH_SOUND)
        self.headshot_source = oalOpen(PATH_PREFIX + HEADSHOT_SOUND)
        self.knockdown_source = oalOpen(PATH_PREFIX + KNOCKDOWN_SOUND)

    def set_gain(self, gain):
        self.shot_source.set_gain(gain)
        self.shield_source.set_gain(gain)
        self.shield_break_source.set_gain(gain)
        self.shield_headshot_source.set_gain(gain)
        self.flesh_source.set_gain(gain)
        self.headshot_source.set_gain(gain)
        self.knockdown_source.set_gain(gain)
