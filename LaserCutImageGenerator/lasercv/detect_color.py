import cv2
import numpy as np
from LaserCutImageGenerator.lasercv.param import Param

HSV_COLORS = {
    "White": {'min': [0, 0, 200], 'max': [180, 30, 255]},
    "Black": {'min': [0, 0, 0], 'max': [180, 255, 30]},
    "Gray": {'min': [0, 0, 31], 'max': [180, 30, 200]},
    "Red": {'min': [0, 100, 100], 'max': [10, 255, 255]},
    "Blue": {'min': [90, 100, 100], 'max': [130, 255, 255]},
    "Green": {'min': [30, 100, 100], 'max': [80, 255, 255]},
    "Yellow": {'min': [20, 100, 100], 'max': [40, 255, 255]},
    "Orange": {'min': [10, 100, 100], 'max': [20, 255, 255]},
    "Pink": {'min': [150, 100, 100], 'max': [170, 255, 255]},
    "Purple": {'min': [120, 100, 100], 'max': [150, 255, 255]},
    "Brown": {'min': [0, 50, 50], 'max': [30, 255, 150]},
    "Gold": {'min': [20, 100, 100], 'max': [35, 255, 255]},
    "Silver": {'min': [0, 0, 150], 'max': [180, 30, 220]},
}


class DetectColor:
    def __init__(self, param: Param):
        self._param = None
        self._colors = {}
        self.update_param(param)

    def update_param(self, param: Param):
        self._param = param
        self._set_detect_colors()

    def _set_detect_colors(self):
        colors_to_update = \
            {color: HSV_COLORS[color] for color in HSV_COLORS
             if getattr(self._param, f"detect_{color.lower()}")}
        self._colors.clear()
        self._colors.update(colors_to_update)

    def _detect_colors(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        masks = {key: cv2.inRange(hsv, np.array(value['min']), np.array(value['max']))
                 for key, value in self._colors.items()}
        if "Red" in masks.keys():
            masks["Red"], _ = self._detect_red_color(img)
        return masks

    def _detect_red_color(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        lower_red2 = np.array([150, 100, 100])
        upper_red2 = np.array([179, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
        masked_img = cv2.bitwise_and(img, img, mask=mask)
        return mask, masked_img
