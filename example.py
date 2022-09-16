from src import FPS, Capture, VideoPreview

if __name__ == '__main__':
    with VideoPreview() as vid:
        for frame, fps in zip(Capture(), FPS()):
            frame.draw_text(f'{fps:.1f} FPS', (10, 30))
            vid.show(frame)
