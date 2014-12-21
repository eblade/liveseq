#!/usr/bin/env python3

from ..midi import MidiIn, MidiOut
from .. import router, Node

# MIDI Control Codes
NOTE_OFF = 128
NOTE_ON = 144


class Port(Node, MidiIn, MidiOut):
    def __init__(self, name='Port'):
        Node.__init__(self)
        MidiIn.__init__(self)
        MidiOut.__init__(self)
        self.name = name
        self.midi2channel = {} # midi channel (0-based) -> channel
        self.channel2midi = {} # channel -> midi channel (0-based)

    def write(self, channel, message):
        midi_channel = self.channel2midi.get(channel, 0)
        command, key, velocity = message
        if command == 'note_on':
            self.write_midi(NOTE_ON + midi_channel, key, velocity)
        elif command == 'note_off':
            self.write_midi(NOTE_OFF + midi_channel, key, velocity)

    def on_midi(self, t, a, v):
        if t >= NOTE_OFF and t <= 143:
            midi_channel = t - NOTE_OFF
            channel = self.midi2channel.get(midi_channel, None)
            if channel is not None:
                router.write(channel, ('note_off', a, v))
        elif t >= NOTE_ON and t <= 159:
            midi_channel = t - NOTE_ON
            channel = self.midi2channel.get(midi_channel, None)
            if channel is not None:
                router.write(channel, ('note_on', a, v))
