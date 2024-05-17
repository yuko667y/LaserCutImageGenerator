from LaserCutImageGenerator.utils import utils, json
from LaserCutImageGenerator.gui.gui import SimpleGui
from LaserCutImageGenerator.lasercv.generate import LaserCv

MODE_ID = 0  # 0: Felt 1: Seaweed
IMG_PATH = './data/paw_badge_orange.jpg'
JSON_PATH = 'config.json'
OUTPUT_DIR = './'
OUTPUT_EXT = '.jpg'


def main():
    _jdata = json.get_json_obj(JSON_PATH)
    param = _jdata[MODE_ID]
    print(param)

    lcv = LaserCv(param)
    gui = SimpleGui(param)
    src_img = utils.get_img(IMG_PATH)

    while True:
        view_imgs, save_imgs = lcv.generate(src_img)
        utils.show_imgs(view_imgs)
        event_ret, param_ret = gui.process()

        if not event_ret:
            break
        if param_ret:
            param = gui.param
            lcv.update_param(param)
            utils.del_window()

    for key, img in save_imgs.items():
        output_path = OUTPUT_DIR + '/output_' + key + OUTPUT_EXT
        utils.write_img(output_path, img)
    del gui, lcv


if __name__ == '__main__':
    main()
