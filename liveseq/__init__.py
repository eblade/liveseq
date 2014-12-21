#!/usr/bin/env python3

import datetime, threading, time


class Router(object):
    def __init__(self):
        self.channels = {}

    def __repr__(self):
        return '<Router>'

    def register(self, channel, reciever):
        if channel in self.channels:
            self.channels[channel].append(reciever)
        else:
            self.channels[channel] = [reciever]

    def unregister(self, channel, reciever):
        if channel in self.channels:
            self.channels[channel].remove(reciever)

    def write(self, channel, message):
        recievers = self.channels.get(channel, [])
        #if channel == 'tkm':
        print('%s -> %s %s' % (message, channel, recievers))
        for reciever in recievers:
            reciever.write(channel, message)

router = Router()
write = router.write

class Node(object):
    name_counter = 0
    def __init__(self):
        self.name = 'Node%i' % self.name_counter
        self.name_counter += 1 

    def __repr__(self):
        return '<Node %s>' % self.name

    def write(self, channel, message):
        raise NotImplemented('This Node has not implement the write method.')


class Clock(Node):
    """
    Clock

    A self-correcting on-interval back-caller using threads.
    
    Usage:
    my_clock = Clock(.1, my_function)
    my_clock.start()
    ...
    my_clock.stop()
    """
    def __init__(self, interval, output_channel='clock'):
        """
        @interval in seconds
        @callback function without arguments
        """
        self.interval = float(interval)
        print("Interval: %f" % self.interval)
        self._on = False
        self.next_call = None
        self.output_channel = output_channel

    def __repr__(self):
        return '<Clock %s>' % self.output_channel

    def write(self, channel, message):
        if channel == 'transport':
            if message == 'play':
                self.start()
            elif message == 'stop':
                self.stop()

    def start(self):
        print("Started")
        self.next_call = time.time() + self.interval
        self._on = True
        threading.Timer( self.next_call - time.time(), self._tick ).start()
        
    def stop(self):
        self._on = False

    @property
    def active(self):
        return self._on

    def _tick(self):
        if not self._on:
            print("Stopped")
            return
        router.write(self.output_channel, 'tick')
        self.next_call += self.interval
        threading.Timer(self.next_call - time.time(), self._tick).start()
