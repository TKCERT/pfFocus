#!/usr/bin/env python3
import itertools
import sys
import threading
import time


class Animation(threading.Thread):
    CHARS = ('\u2630', '\u2631', '\u2632', '\u2634')

    def __init__(self, quiet=False):
        super().__init__()
        self.quiet = quiet
        self.is_running = False

    def __enter__(self):
        if not self.quiet:
            self.start()

    def __exit__(self, type, value, tb):
        if not self.quiet:
            self.is_running = False
            self.join()

    def run(self):
        self.is_running = True
        for char in itertools.cycle(self.CHARS):
            if self.is_running:
                sys.stderr.write('\r{} Working ...'.format(char))
                sys.stderr.flush()
                time.sleep(0.1)
            else:
                sys.stderr.write('\r')
                break
        self.is_running = False
