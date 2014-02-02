#!/usr/bin/env python3

import datetime, threading, time

next_call = time.time()

class Clock:
    """
    Clock

    A self-correcting on-interval back-caller using threads.
    
    Usage:
    my_clock = Clock(.1, my_function)
    my_clock.start()
    ...
    my_clock.stop()
    """
    def __init__(self, interval, callback):
        """
        @interval in seconds
        @callback function without arguments
        """
        self.interval = interval
        self._on = False
        self.next_call = None
        self.callback = callback

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
        (self.callback)()
        self.next_call += self.interval
        threading.Timer( self.next_call - time.time(), self._tick ).start()
