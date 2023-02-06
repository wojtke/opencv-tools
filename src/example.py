from src.opencvtools import FPS, Capture, VideoPreview

if __name__ == '__main__':
    with VideoPreview() as vid:
        for frame, fps in zip(Capture('rtsp://admin:Cosmo%23eye!@192.168.10.206:554/Streaming/channels/101'), FPS()):
            frame.draw_text(f'{fps:.1f} FPS', (10, 30))
            vid.show_many(frame, frame)
