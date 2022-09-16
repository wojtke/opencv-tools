from collections.abc import Generator

import cv2


class Capture(Generator):
    """
    Capture frames from webcam/stream as a generator.
    """

    def __init__(self, src=0, width=None, height=None, threaded=False):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise IOError(f"Could not open {src}")

        if width is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def send(self, *args, **kwargs):
        ret, frame = self.cap.read()
        if not ret:
            raise StopIteration
        return frame

    def __del__(self):
        self.cap.release()

    def throw(self, **kwargs):
        raise StopIteration
