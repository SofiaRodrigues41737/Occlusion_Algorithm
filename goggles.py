from PIL import Image
import math
from PIL import ImageColor
from data_utils import detect_faces


class GogglesTransform(object):
    def __call__(self, sample):
        bounding_boxes, landmarks = detect_faces(sample)
        if len(landmarks) == 0:
            return sample
        left_eye_x = landmarks[0][0]
        left_eye_y = landmarks[0][5]
        right_eye_x = landmarks[0][1]
        right_eye_y = landmarks[0][6]
        nose_x = landmarks[0][2]
        nose_y = landmarks[0][7]
        middle_eyes_x = (right_eye_x + left_eye_x) / 2
        middle_eyes_y = (right_eye_y + left_eye_y) / 2
        googles_width = 2.2 * math.sqrt((right_eye_y - left_eye_y) ** 2 + (right_eye_x - left_eye_x) ** 2)
        googles_height = 1.5 * math.sqrt((middle_eyes_y - nose_y) ** 2 + (middle_eyes_x - nose_x) ** 2)
        rectangle = Image.new("RGBA", (int(googles_width), int(googles_height)), color=ImageColor.getrgb("LightGray"))
        middle_rectangle_x,middle_rectangle_y = googles_width / 2, googles_height/2
        angle = (right_eye_y - left_eye_y) / (right_eye_x - left_eye_x) * 180 / math.pi
        rectangle = rectangle.rotate(-angle, expand=True, center=(middle_rectangle_x, middle_rectangle_y))
        final_size = rectangle.size
        sample.paste(rectangle, (int(middle_eyes_x - final_size[0]/2), int(middle_eyes_y - final_size[1]/2)), rectangle)
        return sample
