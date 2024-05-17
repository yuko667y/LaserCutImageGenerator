import cv2
import numpy as np


def get_img(path: str):
    img = cv2.imread(path)
    if img is None:
        raise ValueError('Faild to load image.: ' + path)
    return img


def write_img(path: str, img):
    if img is None:
        raise ValueError('Faild to save image.: ' + path)
    cv2.imwrite(path, img)


def del_window():
    cv2.destroyAllWindows()


def concat(imgs: list):
    width = 400
    padding = 4

    img = np.zeros((int(padding/2), width, 3), np.uint8)
    img[:, :, :] = 255
    imgbottom = img
    for i in range(0, len(imgs), 2):
        img1 = imgs[0+i]
        h1, w1, ch = img1.shape

        if len(imgs) == i + 1:
            img2 = np.ones((int(width/2), int(width/2), 3), np.uint8) * 255
            h2, w2, ch = img2.shape
        else:
            img2 = imgs[1+i]
            h2, w2, ch = img2.shape

        r1 = (width - padding*3) * h2 / (h2*w1 + h1*w2)
        r2 = (width - padding*3) * h1 / (h2*w1 + h1*w2)

        h1r = int(h1*r1)
        w1r = int(w1*r1)
        h2r = int(h2*r2)
        w2r = int(w2*r2)

        img1r = cv2.resize(img1, (w1r, h1r))
        img2r = cv2.resize(img2, (w2r, h2r))

        img12 = np.ones((h1r+padding, width, 3), np.uint8) * 255

        img12[int(padding/2):int(padding/2)+h1r,
              padding:padding+w1r, :] = img1r
        img12[int(padding/2):int(padding/2)+h2r, padding *
              2+w1r:padding*2+w1r+w2r, :] = img2r

        img = cv2.vconcat([img, img12])
    img = cv2.vconcat([img, imgbottom])
    return img


def show_imgs(imgs):
    img = concat(imgs)
    cv2.imshow('WINDOW', img)
    cv2.waitKey(1)
