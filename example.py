from src import FPS, Capture, VideoPreview

if __name__ == '__main__':
    with VideoPreview(framerate=30) as vid:
        for frame, fps in zip(Capture(), FPS()):
            vid.show(frame)
