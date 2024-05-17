import cv2
import numpy as np
from LaserCutImageGenerator.lasercv.param import Param, MODE
from LaserCutImageGenerator.lasercv.detect_color import DetectColor


class LaserCv:
    def __init__(self, param: Param):
        self._param = None
        self._view_imgs = []
        self._dc = DetectColor(param)
        self.update_param(param)

    def __del__(self):
        print(self._param)

    def generate(self, src_img):
        self._view_imgs, save_imgs = [], {}
        if self._param.mode == MODE.Seaweed:
            img = self._img_aline(src_img)
            img = self._img_blur(img)
            img = self._img_binary(img)
            img = self._img_bold_blackline(img)
            img = self._img_closing(img)
            img = self._img_crop_margin(img)
            img = self._img_square_add_margin(img)
            img = self._img_resize(img)
            self._view_imgs.append(img)
            save_imgs.update({'Seaweed': img})
        elif self._param.mode == MODE.Felt:
            img = self._img_crop_margin(src_img)
            img = self._img_square_add_margin(img)
            img = self._img_resize(img)
            img = self._img_bold_blackline(img)
            img = self._img_closing(img)
            img = self._img_blur(img)
            masks = self._img_bianry_per_color(img)
            for key, img in masks.items():
                # img = self._img_draw_contour(img)
                img = self.draw_white_edge(img, 2, [0, 0, 0])
                self._view_imgs.append(img)
                save_imgs.update({key: img})
        else:
            raise ValueError(
                'This mode is not supported. Check at config.json. Mode:', self._param.mode)
        return self._view_imgs, save_imgs

    def update_param(self, param: Param):
        self._param = param
        self._dc.update_param(param)

    def _img_blur(self, img):
        size = self._param.blur_size
        if size == 0:
            return img
        img = cv2.blur(img, (size, size))
        return img

    def _img_binary(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img_thresh = cv2.threshold(
            img_gray, self._param.threshold, 255, cv2.THRESH_BINARY)
        return img_thresh

    def _img_resize(self, img):
        return cv2.resize(img, (self._param.height, self._param.width))

    def _img_aline(self, img):
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img, kernel, iterations=1)
        img_diff = cv2.absdiff(img, img_dilate)
        return cv2.bitwise_not(img_diff)

    def _img_bold_blackline(self, img):
        kernel = np.ones((3, 3), np.uint8)
        for _ in range(self._param.num_iter_bold):
            img = cv2.erode(img, kernel, iterations=1)
        return img

    def _img_closing(self, img):
        kernel = np.ones((3, 3), np.uint8)
        for _ in range(self._param.num_iter_closing):
            img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return img

    def _img_crop_margin(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(
            img.shape) == 3 else img
        _, img_thresh = cv2.threshold(
            img_gray, self._param.threshold, 255, cv2.THRESH_BINARY)
        img_inv = cv2.bitwise_not(img_thresh)
        contours, _ = cv2.findContours(
            img_inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contours = max(contours, key=lambda x: cv2.contourArea(x))
            x, y, w, h = cv2.boundingRect(contours)
            return img[y:y+h, x:x+w]
        else:
            return img

    def _img_square_add_margin(self, img):
        h, w = img.shape[:2]
        white = [0xFF, 0xFF, 0xFF]
        if h > w:
            pad_size = (h - w) // 2
            return cv2.copyMakeBorder(img, 0, 0, pad_size, pad_size, cv2.BORDER_CONSTANT, value=white)
        elif w > h:
            pad_size = (w - h) // 2
            return cv2.copyMakeBorder(img, pad_size, pad_size, 0, 0, cv2.BORDER_CONSTANT, value=white)
        else:
            return img

    def _img_draw_contour(self, img):
        img_inv = cv2.bitwise_not(img)
        contours, _ = cv2.findContours(
            img_inv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cnt = max(contours, key=lambda x: cv2.contourArea(x))
            epsilon = 0.00005 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            cv2.drawContours(img, [approx], -1, (0, 0, 0), thickness=1)
        return img

    def _img_bianry_per_color(self, img):
        masks = self._dc._detect_colors(img)
        return {key: cv2.bitwise_not(mask) for key, mask in masks.items()}

    def draw_white_edge(self, img, thickness=1, color=[255, 255, 255]):
        if len(img.shape) < 3:  # gray scale
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        else:
            pass

        height, width = img.shape[0], img.shape[1]
        img[height - thickness:height, :, :] = color  # bottom
        img[0: thickness, :, :] = color   # top
        img[:, 0:thickness, :] = color    # left
        img[:, width - thickness:width, :] = color    # right
        return img
