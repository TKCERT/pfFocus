#!/usr/bin/env python3
import itertools
import sys
import threading
import time


class AnimationThread(threading.Thread):
    CHARS = ('\u2630', '\u2631', '\u2632', '\u2634')

    def __init__(self):
        super().__init__()
        self.is_running = False

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

def start():
    thread = AnimationThread()
    thread.start()
    return thread

def stop(thread):
    thread.is_running = False
    thread.join()
