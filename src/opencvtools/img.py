import cv2
import numpy as np


class Img(np.ndarray):
    def __new__(cls, input_array):
        if not isinstance(input_array, np.ndarray):
            raise TypeError('Input must be a numpy array.')

        if input_array.dtype != np.uint8:
            max, min = np.min(input_array), np.max(input_array)
            if input_array.dtype in (np.float32, np.float64):
                if 0 <= min and max <= 1:
                    input_array = (input_array * 255).astype(np.uint8)
                else:
                    raise ValueError('Input array must be between 0 and 1 to be converted from float to uint8.')
            if input_array.dtype in (np.int32, np.int64):
                if 0 <= min and max <= 255:
                    input_array = input_array.astype(np.uint8)
                else:
                    raise ValueError('Input array must be between 0 and 255 to be converted from int to uint8.')

        if not 2 <= input_array.ndim <= 3:
            raise ValueError('Input must be 2 or 3 dimensional.')

        obj = np.asarray(input_array).view(cls)

        obj.height, obj.width = obj.shape[:2]

        obj.draw_color = (255, 255, 255)
        return obj

    def draw_line(self, *pts, thickness=2, color=None):
        pts = np.array(pts, np.int32)
        cv2.polylines(self, [pts], isClosed=0, color=color or self.draw_color, thickness=thickness)
        return self

    def draw_circle(self, center, radius, thickness=2, color=None):
        center = np.array(center, np.int32)
        cv2.circle(self, center, int(radius), color=color or self.draw_color, thickness=thickness)
        return self

    def draw_text(self, text, pos, font_scale=0.8, color=None, thickness=2, bg_color=None):
        pos = np.array(pos, np.int32)
        if bg_color is not None:
            (w, h), b = cv2.getTextSize(text, 0, font_scale, thickness)
            cv2.rectangle(self, pos + [0, b], pos + [w + 2 * thickness, -h - b // 2], bg_color, -1)
        cv2.putText(self, text, pos + [thickness, 0], cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
        return self

    def draw_rect(self, tl, br, thickness=2, color=None):
        tl = np.array(tl, np.int32)
        br = np.array(br, np.int32)
        cv2.rectangle(self, tl, br, color=color or self.draw_color, thickness=thickness)
        return self

    def box_label(self, tlbr, label, color=None):
        t, l, b, r = tlbr
        color = color or self.draw_color
        text_color = (0, 0, 0) if np.array(color).mean() > 127 else (255, 255, 255)
        self.draw_text(label, (t, l), color=text_color, bg_color=color)
        return self

    def blend(self, other, alpha=1):
        cv2.addWeighed(self, other, alpha=alpha, dst=self)
        return self
