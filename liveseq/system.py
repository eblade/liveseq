#!/usr/bin/env python3

from router import Router
from sequencer import Sequencer, Track
from clock import Clock
from midi import Device

class System:
    def __init__(self, tempo=120, part=8, controller=None):
        self.router = Router()
        self.clock = Clock(60/tempo/part, self.tick)
        self.sequencer = Sequencer(self.clock)
        self.controller = controller
        controller.sequencer = self.sequencer
        self.router.add(controller, identifier='controller_midi')
        controller.midi_identifier = 'controller_midi'

        track = Track("track1")
        self.sequencer.track.append(track)

        device = Device("track1")
        self.router.add(device)

    def tick(self):
        for packet in self.sequencer.read():
            self.router.write(*packet)

    def start(self):
        self.clock.start()
        self.sequencer.state = 'playing'
        self.controller.reflect(self.sequencer)

    def stop(self):
        self.clock.stop()
        self.sequencer.state = 'stopped'
        self.controller.reflect(self.sequencer)
