#!/usr/bin/env python3

from midi import Controller

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

class KorgNanoKontrol2(Controller):
    def write(self, midi):
        t, a, v = midi
        if t == CC:
            if a in range(TRACK_LEVEL, TRACK_LEVEL + 8): 
                self.track_level[a] = v
            elif a in range(TRACK_MOD, TRACK_MOD + 8): 
                self.track_mod[a-TRACK_MOD]
            elif a in range(TRACK_SOLO, TRACK_SOLO + 8): 
                self.track_solo[a-TRACK_SOLO] = v
            elif a in range(TRACK_MUTE, TRACK_MUTE + 8): 
                self.track_mute[a-TRACK_MUTE] = v
            elif a in range(TRACK_RECORD, TRACK_RECORD + 8): 
                self.track_record[a-TRACK_RECORD] = v
            elif a == BACKWARD: 
                self.backward = v
            elif a == FORWARD: 
                self.forward = v
            elif a == STOP: 
                self.stop = v
            elif a == PLAY:
                self.play = v
            elif a == RECORD:
                self.record = v
            elif a == CYCLE:
                self.cycle = v
            elif a == MARKER_SET:
                self.marker_set = v
            elif a == MARKER_PREV:
                self.marker_prev = v
            elif a == MARKER_NEXT:
                self.marker_next = v
            elif a == TRACK_PREV:
                self.track_prev = v
            elif a == TRACK_NEXT:
                self.track_next = v

    def read(self):
        for x in (
            #(CC, 0, self.track_level[0]),
            #(CC, 1, self.track_level[1]),
            #(CC, 2, self.track_level[2]),
            #(CC, 3, self.track_level[3]),
            #(CC, 4, self.track_level[4]),
            #(CC, 5, self.track_level[5]),
            #(CC, 6, self.track_level[6]),
            #(CC, 7, self.track_level[7]),
            #(CC, 16, self.track_mod[0]),
            #(CC, 17, self.track_mod[1]),
            #(CC, 18, self.track_mod[2]),
            #(CC, 19, self.track_mod[3]),
            #(CC, 20, self.track_mod[4]),
            #(CC, 21, self.track_mod[5]),
            #(CC, 22, self.track_mod[6]),
            #(CC, 23, self.track_mod[7]),
            (CC, TRACK_SOLO + 0, self.track_solo[0]),
            (CC, TRACK_SOLO + 1, self.track_solo[1]),
            (CC, TRACK_SOLO + 2, self.track_solo[2]),
            (CC, TRACK_SOLO + 3, self.track_solo[3]),
            (CC, TRACK_SOLO + 4, self.track_solo[4]),
            (CC, TRACK_SOLO + 5, self.track_solo[5]),
            (CC, TRACK_SOLO + 6, self.track_solo[6]),
            (CC, TRACK_SOLO + 7, self.track_solo[7]),
            (CC, TRACK_MUTE + 0, self.track_mute[0]),
            (CC, TRACK_MUTE + 1, self.track_mute[1]),
            (CC, TRACK_MUTE + 2, self.track_mute[2]),
            (CC, TRACK_MUTE + 3, self.track_mute[3]),
            (CC, TRACK_MUTE + 4, self.track_mute[4]),
            (CC, TRACK_MUTE + 5, self.track_mute[5]),
            (CC, TRACK_MUTE + 6, self.track_mute[6]),
            (CC, TRACK_MUTE + 7, self.track_mute[7]),
            (CC, TRACK_RECORD + 0, self.track_record[0]),
            (CC, TRACK_RECORD + 1, self.track_record[1]),
            (CC, TRACK_RECORD + 2, self.track_record[2]),
            (CC, TRACK_RECORD + 3, self.track_record[3]),
            (CC, TRACK_RECORD + 4, self.track_record[4]),
            (CC, TRACK_RECORD + 5, self.track_record[5]),
            (CC, TRACK_RECORD + 6, self.track_record[6]),
            (CC, TRACK_RECORD + 7, self.track_record[7]),
            (CC, BACKWARD, self.backward),
            (CC, FORWARD, self.forward),
            (CC, STOP, self.stop),
            (CC, PLAY, self.play),
            (CC, RECORD, self.record),
            (CC, CYCLE, self.cycle),
            (CC, MARKER_SET, self.marker_set),
            (CC, MARKER_PREV, self.marker_prev),
            (CC, MARKER_NEXT, self.marker_next),
            (CC, TRACK_PREV, self.track_prev),
            (CC, TRACK_NEXT, self.track_next),
        ):
            yield x

    def reflect(self, sequencer):
        if sequencer.state == 'playing':
            self.play = 127
            self.stop = 0
        elif sequencer.state == 'stopped':
            self.play = 0
            self.stop = 127
        self.push((CC, PLAY, self.play))
        self.push((CC, STOP, self.stop))

    def push(self, data):
        if self.router is None: 
            return
        if self.midi_identifier is None:
            return
        self.router.write(self.midi_identifier, data)
