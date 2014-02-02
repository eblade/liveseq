#!/usr/bin/env python3

class Device:
    def __init__(self, identifier, router=None):
        self.identifier = identifier
        self.router = router
        self.midi_identifier = None

    def write(self, midi):
        pass

    def read(self, midi):
        pass

class Controller(Device):
    def __init__(self, identifier, router=None, sequencer=None):
        super().__init__(identifier, router)
        self.sequencer = sequencer
        self.track_offset = 0
        self._track_level = [0,0,0,0,0,0,0,0]
        self._track_mod = [0,0,0,0,0,0,0,0]
        self._track_solo = [0,0,0,0,0,0,0,0]
        self._track_mute = [0,0,0,0,0,0,0,0]
        self._track_record = [0,0,0,0,0,0,0,0]
        self._forward = 0
        self._backward = 0
        self._stop = 0
        self._play = 0
        self._record = 0
        self._cycle = 0
        self._marker_set = 0
        self._marker_prev = 0
        self._marker_next = 0
        self._track_prev = 0
        self._track_next = 0

    @property
    def track_level(self):
        return self._track_level

    @track_level.setter
    def track_level(self, data):
        track, value = data
        self._track_level[track] = value
        if not self.sequencer is None:
            self.sequencer.track_level = (self.track_offset + track, value)

    @property
    def track_mod(self):
        return self._track_mod

    @track_mod.setter
    def track_mod(self, data):
        track, value = data
        self._track_mod[track] = value
        if not self.sequencer is None:
            self.sequencer.track_mod = (self.track_offset + track, value)

    @property
    def track_solo(self):
        return self._track_solo

    @track_solo.setter
    def track_solo(self, data):
        track, value = data
        self._track_solo[track] = value
        if not self.sequencer is None:
            self.sequencer.track_solo = (self.track_offset + track, value > 0)

    @property
    def track_mute(self):
        return self._track_mute

    @track_mute.setter
    def track_mute(self, data):
        track, value = data
        self._track_mute[track] = value
        if not self.sequencer is None:
            self.sequencer.track_mute = (self.track_offset + track, value > 0)

    @property
    def track_record(self):
        return self._track_record

    @track_record.setter
    def track_record(self, data):
        track, value = data
        self._track_record[track] = value
        #if not self.sequencer is None:
        #    self.sequencer.track_record = (self.track_offset + track, value > 0)

    @property
    def backward(self):
        return self._backward

    @backward.setter
    def backward(self, value):
        self._backward = value
        #if not self.sequencer is None:
        #    self.sequencer.backward = value > 0

    @property
    def forward(self):
        return self._forward

    @forward.setter
    def forward(self, value):
        self._forward = value
        #if not self.sequencer is None:
        #    self.sequencer.forward = value > 0

    @property
    def play(self):
        return self._play

    @play.setter
    def play(self, value):
        self._play = value
        if not self.sequencer is None:
            self.sequencer.play = value > 0

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        self._stop = value
        if not self.sequencer is None:
            self.sequencer.stop = value > 0

    @property
    def record(self):
        return self._record

    @record.setter
    def record(self, value):
        self._record = value
        #if not self.sequencer is None:
        #    self.sequencer.record = value > 0

    @property
    def cycle(self):
        return self._cycle

    @cycle.setter
    def cycle(self, value):
        self._cycle = value
        #if not self.sequencer is None:
        #    self.sequencer.cycle = value > 0

    @property
    def marker_set(self):
        return self._marker_set

    @marker_set.setter
    def marker_set(self, value):
        self._marker_set = value
        #if not self.sequencer is None:
        #    self.sequencer.marker_set = value > 0

    @property
    def marker_prev(self):
        return self._marker_prev

    @marker_prev.setter
    def marker_prev(self, value):
        self._marker_prev = value
        #if not self.sequencer is None:
        #    self.sequencer.marker_prev = value > 0

    @property
    def marker_next(self):
        return self._marker_next

    @marker_next.setter
    def marker_next(self, value):
        self._marker_next = value
        #if not self.sequencer is None:
        #    self.sequencer.marker_next = value > 0

    @property
    def track_prev(self):
        return self._track_prev

    @track_prev.setter
    def track_prev(self, value):
        self._track_prev = value
        #if not self.sequencer is None:
        #    self.sequencer.track_prev = value > 0

    @property
    def track_next(self):
        return self._track_next

    @track_next.setter
    def track_next(self, value):
        self._track_next = value
        #if not self.sequencer is None:
        #    self.sequencer.track_next = value > 0
