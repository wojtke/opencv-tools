from time import perf_counter, sleep

import cv2


class StopVideo(Exception):
    """Exception to stop video."""
    pass


class VideoPreview:
    """
    Video display with OpenCV with some common functionality.

    Usage
    -------------------------
    with VideoPreview() as vid:
        for frame in Capture():
            vid.show(frame)

    Alternative usage (throws StopVideo exception on quit):
    -------------------------------------------------------
    vid = VideoPreview()
    for frame in Capture():
        vid.show(frame)

    """

    def __init__(self, window_name="Video preview", framerate=30, fullscreen_key='f', quit_key='esc'):
        self.keys = None
        self.window_name = window_name

        self.fullscreen = False
        self.fullscreen_key = ord(fullscreen_key)
        self.quit_key = 27 if quit_key == 'esc' else ord(quit_key)

        self.delay = 1 / framerate if framerate is not None else 0
        self.last_frame_time = 0

        cv2.namedWindow(self.window_name, cv2.WINDOW_KEEPRATIO)

    def toggle_fullscreen(self):
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN if not self.fullscreen else cv2.WINDOW_NORMAL)
        self.fullscreen = not self.fullscreen

    def show(self, frame):
        cv2.imshow(self.window_name, frame)

        self.keys = cv2.waitKey(1) & 0xFF
        if self.keys == self.quit_key:
            raise StopVideo
        if self.keys == self.fullscreen_key:
            self.toggle_fullscreen()

        sleep(max(self.last_frame_time + self.delay - perf_counter(), 0))
        self.last_frame_time = perf_counter()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        cv2.destroyAllWindows()
        if type == StopVideo:
            return True
        return False
