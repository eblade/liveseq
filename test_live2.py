#!/usr/bin/env python3

from liveseq import router, Clock
from liveseq.sequencer import Sequencer, Automation
from liveseq.korg.nano import NanoKontrol2
from liveseq.generic import Port

import time

clock = Clock(60.0/112.0/6.0)
sequencer = Sequencer(8)


router.register('transport', sequencer)
router.register('track', sequencer)
router.register('clock', sequencer)
router.register('transport', clock)

nk = NanoKontrol2()
router.register('tm', nk)
router.register('tkm', nk)
nk.open_midi_in('nanoKONTROL2')
nk.open_midi_out('nanoKONTROL2')

sequencer.track[0] = Automation('track')
sequencer.track[0].load_matrix([
    [(1, 'transpose', 0), None, (1, 'transpose', -4), (1, 'transpose', -2)],
], 10)
sequencer.track[1].load_matrix({
    60: [(1, 100), (1, 80), (1, 80), None    , (1, 80), (1, 80), (1, 100), (1, 100), None    , (1, 100), (1, 100), None    , (1, 100), (1, 100)],
    72: [None,     None   , None   , (1, 100), None   , None   , None    , None    , (1, 100), None    , None    , (1, 100), None    , None    ],
}, 7)
sequencer.track[2].load_matrix({
    64: [(1, 127), None   , (1, 30), None    , None   , (1,80)],
}, 8)
sequencer.track[3].load_matrix({
    64: [(1, 127), (1, 80), (1, 100), None],
    60: [None    , (1, 80), None    , None],
}, 9)
sequencer.track[4].load_matrix({
    72: [(1, 127), None, (1, 100), None],
    67: [None    , (1, 80), None    , (1, 100)],
}, 7)

port = Port('Instrument')
router.register('playback_track1', port)
port.channel2midi['playback_track1'] = 0
router.register('playback_track2', port)
port.channel2midi['playback_track2'] = 1
router.register('playback_track3', port)
port.channel2midi['playback_track3'] = 2
router.register('playback_track4', port)
port.channel2midi['playback_track4'] = 2
port.open_midi_out('MidiSport 2x2:0')

#keyboard = Port('Keyboard')
#keyboard.midi2channel[0] = 'record_track3'
#keyboard.open_midi_in('nanoKEY2')

nk.blink()
router.write('transport', 'stop')

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    del nk
    del port
    #del keyboard
