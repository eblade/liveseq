#!/usr/bin/env python3

from ..midi import MidiIn, MidiOut
from .. import router, Node
import time

# NanoKontrol2 CC codes
CC = 176
TRACK_LEVEL = 0
TRACK_MOD = 16
TRACK_SOLO = 32
TRACK_MUTE = 48
TRACK_RECORD = 64
BACKWARD = 43
FORWARD = 44
STOP = 42
PLAY = 41
RECORD = 45
CYCLE = 46
MARKER_SET = 60
MARKER_PREV = 61
MARKER_NEXT = 62
TRACK_PREV = 58
TRACK_NEXT = 59

# Set the device in control mode CC and set LED to external. Keep default mappings.

class NanoKontrol2(Node, MidiIn, MidiOut):
    def __init__(self, name='NK2'):
        Node.__init__(self)
        MidiIn.__init__(self)
        MidiOut.__init__(self)
        self.name = name
        self.track_channel = 'track'
        self.transport_channel = 'transport'
        self.track_monitor_channel = 'tkm'
        self.transport_monitor_channel = 'tm'
        self.solo_mapping = 'loop' # or 'solo'
        self.mod_mapping = 'transpose'
        self.mod_min = 0 
        self.mod_max = 5

    def blink(self):
        for track in range(8):
            self.write_midi(CC, TRACK_SOLO + track, 127)
            self.write_midi(CC, TRACK_MUTE + track, 127)
            self.write_midi(CC, TRACK_RECORD + track, 127)

        self.write_midi(CC, BACKWARD, 127)
        self.write_midi(CC, FORWARD, 127)
        self.write_midi(CC, STOP, 127)
        self.write_midi(CC, PLAY, 127)
        self.write_midi(CC, RECORD, 127)
        self.write_midi(CC, CYCLE, 127)
        self.write_midi(CC, MARKER_SET, 127)
        self.write_midi(CC, MARKER_PREV, 127)
        self.write_midi(CC, MARKER_NEXT, 127)
        self.write_midi(CC, TRACK_PREV, 127)
        self.write_midi(CC, TRACK_NEXT, 127)

        time.sleep(0.7)

        for track in range(8):
            self.write_midi(CC, TRACK_SOLO + track, 0)
            self.write_midi(CC, TRACK_MUTE + track, 0)
            self.write_midi(CC, TRACK_RECORD + track, 0)

        self.write_midi(CC, BACKWARD, 0)
        self.write_midi(CC, FORWARD, 0)
        self.write_midi(CC, STOP, 0)
        self.write_midi(CC, PLAY, 0)
        self.write_midi(CC, RECORD, 0)
        self.write_midi(CC, CYCLE, 0)
        self.write_midi(CC, MARKER_SET, 0)
        self.write_midi(CC, MARKER_PREV, 0)
        self.write_midi(CC, MARKER_NEXT, 0)
        self.write_midi(CC, TRACK_PREV, 0)
        self.write_midi(CC, TRACK_NEXT, 0)

    def on_midi(self, t, a, v):
        if t == CC:
            if a in range(TRACK_LEVEL, TRACK_LEVEL + 8): 
                router.write(self.track_channel, (a - TRACK_LEVEL, 'level', v))
            elif a in range(TRACK_MOD, TRACK_MOD + 8): 
                router.write(self.track_channel, (a - TRACK_MOD, self.mod_mapping, [-4, -2, 0, 2, 5, 7][self.mod_min + v * (self.mod_max - self.mod_min) // 127]))
            elif a in range(TRACK_SOLO, TRACK_SOLO + 8) and v > 0: 
                router.write(self.track_channel, (a - TRACK_SOLO, self.solo_mapping, v > 0))
            elif a in range(TRACK_MUTE, TRACK_MUTE + 8) and v > 0: 
                router.write(self.track_channel, (a - TRACK_MUTE, 'mute', v > 0))
            elif a in range(TRACK_RECORD, TRACK_RECORD + 8) and v > 0: 
                router.write(self.track_channel, (a - TRACK_RECORD, 'record', v > 0))
            elif a == BACKWARD and v > 0: 
                router.write(self.transport_channel, 'backward')
            elif a == FORWARD and v > 0: 
                router.write(self.transport_channel, 'forward')
            elif a == STOP and v > 0: 
                router.write(self.transport_channel, 'stop')
            elif a == PLAY and v > 0:
                router.write(self.transport_channel, 'play')
            elif a == RECORD and v > 0:
                router.write(self.transport_channel, 'record')
            elif a == CYCLE and v > 0:
                router.write(self.transport_channel, 'cycle')
            elif a == MARKER_SET and v > 0:
                router.write(self.transport_channel, 'marker_set')
            elif a == MARKER_PREV and v > 0:
                router.write(self.transport_channel, 'marker_prev')
            elif a == MARKER_NEXT and v > 0:
                router.write(self.transport_channel, 'marker_next')
            elif a == TRACK_PREV and v > 0:
                router.write(self.transport_channel, 'track_prev')
            elif a == TRACK_NEXT and v > 0:
                router.write(self.transport_channel, 'track_next')

    def write(self, channel, message):
        if channel == self.track_monitor_channel:
            track, p, v = message
            if p == self.solo_mapping:
                self.write_midi(CC, TRACK_SOLO + track, 127 if v else 0)
            elif p == 'mute':
                self.write_midi(CC, TRACK_MUTE + track, 127 if v else 0)
            elif p == 'record':
                self.write_midi(CC, TRACK_RECORD + track, 127 if v else 0)
        elif channel == self.transport_monitor_channel:
            k, v = message
            if k == 'backward':
                self.write_midi(CC, BACKWARD, 127 if v else 0)
            elif k == 'forward':
                self.write_midi(CC, FORWARD, 127 if v else 0)
            elif k == 'stop':
                self.write_midi(CC, STOP, 127 if v else 0)
            elif k == 'play':
                self.write_midi(CC, PLAY, 127 if v else 0)
            elif k == 'record':
                self.write_midi(CC, RECORD, 127 if v else 0)
            elif k == 'cycle':
                self.write_midi(CC, CYCLE, 127 if v else 0)
            elif k == 'marker_set':
                self.write_midi(CC, MARKER_SET, 127 if v else 0)
            elif k == 'marker_prev':
                self.write_midi(CC, MARKER_PREV, 127 if v else 0)
            elif k == 'marker_next':
                self.write_midi(CC, MARKER_NEXT, 127 if v else 0)
            elif k == 'track_prev':
                self.write_midi(CC, TRACK_PREV, 127 if v else 0)
            elif k == 'track_next':
                self.write_midi(CC, TRACK_NEXT, 127 if v else 0)

