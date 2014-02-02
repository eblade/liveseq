#!/usr/bin/env python3

class Track:
    def __init__(self, identifier):
        self.position = 0
        self.in_point = 0
        self.loop = False
        self.identifier = identifier
        self.mute = False
        self.solo = False

    def read(self, position):
        yield (0x90, 60, 112) if self.position % 1 else (0x80, 60, 0)

class Sequencer:
    def __init__(self, clock):
        self.track = []
        self.page = 0
        self.state = 'stopped'
        self.solo = False
        self.position = 0
        self.clock = clock

    def read(self):
        current_position = self.position
        self.position += 1
        for track in [track for track in self.track if ((self.solo and track.solo) or (not self.solo and not track.mute))]:
            for midi in track.read(current_position):
                yield track.identifier, midi
        
    @property
    def play(self):
        return self.state == 'playing'

    @play.setter
    def play(self, value):
        if value and not self.clock.active:
            self.clock.start()
               
    @property
    def stop(self):
        return self.state == 'stopped'

    @stop.setter
    def stop(self, value):
        if value:
            if self.clock.active:
                self.clock.stop()
            else:
                self.position = 0
               
