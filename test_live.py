#!/usr/bin/env python3

import time
import rtmidi
from rtmidi.midiutil import open_midiport

from liveseq.korg import KorgNanoKontrol2
from liveseq.system import System

ktrl = KorgNanoKontrol2('k')
s = System(controller=ktrl)

class MidiInputHandler:
    def __init__(self, port, system):
        self.port = port
        self._wallclock = time.time()
        self._system = system

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        self._system.router.write('controller_midi', message)

port = 'start:playback'
try:
    midiin, port_name = open_midiport(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name, s))

print("Entering main loop. Press Control-C to exit.")
try:
    # just wait for keyboard interrupt in main thread
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin


#midiout = rtmidi.MidiOut()
#available_ports = [x for x, p in enumerate(midiout.get_ports()) if p.endswith('start')]
#print(midiout.get_ports())
#
#note_on = [0x90, 60, 112] # ch1 middle C, v112
#note_off = [0x80, 60, 0]
#
#if available_ports:
#    midiout.open_port(0)
#else:
#    print("VIRTUELL")
#    midiout.open_virtual_port("JOHAN VP")
#time.sleep(10)
#
#
#midiout.send_message(note_on)
#time.sleep(0.5)
#midiout.send_message(note_off)
#
#del midiout
