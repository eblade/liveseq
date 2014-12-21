#!/usr/bin/env python3

import rtmidi
import sys
import time
from rtmidi.midiutil import open_midiport


class MidiIn(object):
    def __init__(self):
        self._midi_in = None
        self._midi_in_port = '<unknown>'
        self.port_in = None

    def __call__(self, event, data=None):
        midi, deltatime = event
        t, a, v = midi
        print("[%s] >>> %r" % (self.port_in, midi))
        self.on_midi(t, a, v)

    def on_midi(self, t, a, v):
        pass # implement this

    def __del__(self):
        if self._midi_in is not None:
            self._midi_in.close_port()
            del self._midi_in

    def open_midi_in(self, port):
        try:
            midiin, port_name = open_midiport(port, 'input', client_name='liveseq', interactive=False)
        except (EOFError, KeyboardInterrupt):
            sys.exit()
        self._midi_in = midiin
        self.port_in = port_name
        midiin.set_callback(self)
        print("MIDI In (virtual): %s" % port_name)

    def open_virtual_midi_in(self, port_name='virtual_input'):
        midiin = rtmidi.MidiIn()
        midiin.open_virtual_port(port_name)
        self._midi_in = midiin
        self.port_in = port_name
        midiin.set_callback(self)
        print("MIDI In: %s" % port_name)



class MidiOut(object):
    def __init__(self):
        self._midi_out = None
        self.port_out = None

    def write_midi(self, t, a, v):
        if self._midi_out is not None:
            midi = [t, a, v]
            print("[%s] <<< %r" % (self.port_out, midi))
            self._midi_out.send_message(midi)

    def __del__(self):
        if self._midi_out is not None:
            del self._midi_out
        
    def open_midi_out(self, port):
        try:
            midiout, port_name = open_midiport(port, 'output', client_name='liveseq', interactive=False)
        except (EOFError, KeyboardInterrupt):
            sys.exit()
        self._midi_out = midiout
        self.port_out = port_name
        print("MIDI Out: %s" % port_name)

    def open_virtual_midi_out(self, port_name='virtual_output'):
        midiout = rtmidi.MidiOut()
        midiout.open_virtual_port(port_name)
        self._midi_out = midiout
        self.port_out = port_name
        print("MIDI Out (virtual): %s" % port_name)
