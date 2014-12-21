#!/usr/bin/env python3

from . import Node, router

class Sequencer(Node):
    def __init__(self, tracks=0, name='s0', resolution=4):
        self.name = name
        if resolution not in range(11):
            ValueError('Resolution must be an integer from 0 to 10')
        self.tick_size = int(1024 // 2**resolution)
        self.track = []
        self.page = 0
        self.state = 'stop'
        self.solo = False
        self.position = 0
        self.transport_monitor_channel = 'tm'

        for t in range(tracks):
            self.track.append(Track('playback_track%i' % t))

    def __repr__(self):
        return '<Sequencer %s>' % self.name

    def write(self, channel, message):
        if channel == 'clock':
            self.tick()
        elif channel == 'transport':
            if message == 'play':
                self.play()
            elif message == 'stop':
                self.stop()
            elif message == 'pause':
                self.pause()
        elif channel == 'track':
            t, p, v = message
            if len(self.track) > t:
                track = self.track[t]
                if p == 'solo':
                    track.solo = not track.solo
                    router.write('tkm', (t, p, track.solo))
                    self.update_solo()
                    if track.solo and track.mute:
                        track.mute = False
                        router.write('tkm', (t, 'mute', track.mute))
                        track.stop()
                elif p == 'mute':
                    track.mute = not track.mute
                    router.write('tkm', (t, p, track.mute))
                    if track.solo and track.mute:
                        track.solo = False
                        router.write('tkm', (t, 'solo', track.solo))
                        self.update_solo()
                    if track.mute:
                        track.stop()
                elif p == 'record':
                    track.record = not track.record
                    router.write('tkm', (t, p, track.record))
                elif p == 'level':
                    track.level = v
                    router.write('tkm', (t, p, track.level))
                elif p == 'mod':
                    track.mod = v
                    router.write('tkm', (t, p, track.mod))
                elif p == 'in_point':
                    track.in_point = v
                    router.write('tkm', (t, p, track.in_point))
                elif p == 'length':
                    track.length = v
                    router.write('tkm', (t, p, track.length))
                elif p == 'loop':
                    track.loop = not track.loop
                    router.write('tkm', (t, p, track.loop))
                elif p == 'set_loop':
                    track.loop = v
                    router.write('tkm', (t, 'loop', track.loop))
                elif p == 'transpose':
                    if track.transpose != v:
                        track.stop()
                    track.transpose = v
                    router.write('tkm', (t, 'transpose', track.transpose))

    def update_solo(self):
        if any([t for t in self.track if t.solo]):
            self.solo = True
        else:
            self.solo = False
        router.write('tm', ('solo', self.solo))

    def tick(self):
        for track in [track for track in self.track if ((self.solo and track.solo) or (not self.solo and not track.mute))]:
            for message in track.read(self.position):
                router.write(track.playback_channel, message)
        router.write('tm', ('position', self.position))
        self.position += self.tick_size

    def play(self):
        self.state = 'play'
        if self.transport_monitor_channel is not None:
            router.write(self.transport_monitor_channel, ('play', True))
            router.write(self.transport_monitor_channel, ('stop', False))
            router.write(self.transport_monitor_channel, ('pause', False))
            router.write(self.transport_monitor_channel, ('position', self.position))
        
    def stop(self):
        self.state == 'stop'
        self.position = 0
        for track in self.track:
            track.stop()
        if self.transport_monitor_channel is not None:
            router.write(self.transport_monitor_channel, ('play', False))
            router.write(self.transport_monitor_channel, ('stop', True))
            router.write(self.transport_monitor_channel, ('pause', False))
            router.write(self.transport_monitor_channel, ('position', 0))

    def pause(self):
        self.state == 'stop'
        for track in self.track:
            track.stop()
        if self.transport_monitor_channel is not None:
            router.write(self.transport_monitor_channel, ('play', False))
            router.write(self.transport_monitor_channel, ('stop', False))
            router.write(self.transport_monitor_channel, ('pause', True))
            router.write(self.transport_monitor_channel, ('position', 0))




class Track(object):
    def __init__(self, playback_channel):
        self.in_point = 0
        self.level = 100
        self.length = 0
        self.loop = False
        self.playback_channel = playback_channel
        self.mute = False
        self.solo = False
        self.record = False
        self.data = {}
        self.note_stack = [0] * 128
        self.transpose = 0

    def __repr__(self):
        return '<Track %s %s %i/%i%s>' % (self.playback_channel, 'M' if self.mute else ('S' if self.solo else '-'), self.in_point, self.length, 'L' if self.loop else '')

    def relative(self, position):
        if position < self.in_point:
            return
        position = position - self.in_point
        if self.loop and self.length > 0:
            position = position % self.length
        elif position > self.length:
            return
        return position

    def read(self, position):
        position = self.relative(position)
        if position is None:
            return
        if self.loop and position == 0:
            for message in self.data.get(self.length, []):
                command, note, velocity = message
                velocity = (self.level * velocity) // 127
                note += self.transpose
                if note < 0 or note > 127:
                    continue
                if command == 'note_on':
                    self.note_stack[note] += 1
                elif command == 'note_off' and self.note_stack[note] > 0:
                    self.note_stack[note] -= 1
                yield (command, note, velocity)
        for message in self.data.get(position, []):
            command, note, velocity = message
            velocity = (self.level * velocity) // 127
            note += self.transpose
            if note < 0 or note > 127:
                continue
            if command == 'note_on':
                self.note_stack[note] += 1
            elif command == 'note_off' and self.note_stack[note] > 0:
                self.note_stack[note] -= 1
            yield (command, note, velocity)

    def stop(self):
        for note, number in enumerate(self.note_stack):
            for i in range(number):
                router.write(self.playback_channel, ('note_off', note, 0)) 

    def record(self, position, message):
        position = self.relative(position)
        if position is None:
            return
        self._record(position, message)

    def _record(self, position, message):
        existing = self.data.get(position, None)
        if existing is None:
            self.data[position] = [message]
        else:
            existing.append(message)

    def clear(self):
        self.data = {}

    def load_matrix(self, data, resolution):
        if resolution not in range(11):
            ValueError('Resolution must be an integer from 0 to 10')
        resolution = 2**resolution
        max_length = self.length
        for k, v in data.items():
            for n, data in enumerate(v):
                if data is not None:
                    length, velocity = data
                    note_on = n*resolution
                    note_off = (n+length)*resolution
                    self._record(note_on, ('note_on', k, velocity))
                    self._record(note_off, ('note_off', k, 0))
                    max_length = max(max_length, note_off)
        self.length = max_length


class Automation(Track):
    def read(self, position):
        position = self.relative(position)
        if position is None:
            return
        for message in self.data.get(position, []):
            yield message

    def load_matrix(self, data, resolution):
        if resolution not in range(11):
            ValueError('Resolution must be an integer from 0 to 10')
        resolution = 2**resolution
        max_length = self.length
        for v in data:
            for n, message in enumerate(v):
                if message is not None:
                    position = n*resolution
                    self._record(position, message)
                    max_length = max(max_length, position+resolution)
        self.length = max_length
