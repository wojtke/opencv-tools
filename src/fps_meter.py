from time import perf_counter

import numpy as np


class FPS:
    """
    Iterator that yields FPS. It is a moving average of FPS over last qsize frames.
    Each iteration is counted as a new frame.
    """

    def __init__(self, qsize=100):
        self.Q = np.zeros(qsize)
        self.qsize = qsize
        self.i = 0

        self.first_frame_time = None

        self.__current_next = self.__warmup_next

    def __iter__(self):
        return self

    def __next__(self):
        return self.__current_next()

    def __warmup_next(self):
        if self.i == 0:
            self.Q[0] = perf_counter()
            self.i += 1
            return 0

        self.Q[self.i] = perf_counter()
        self.i += 1

        if self.i == self.qsize:
            self.i = 0
            self.__current_next = self.__proper_next

        return self.i / (self.Q[self.i - 1] - self.Q[0])

    def __proper_next(self):
        old = self.Q[self.i]
        new = self.Q[self.i] = perf_counter()
        self.i = (self.i + 1) % self.qsize
        return self.qsize / (new - old)
