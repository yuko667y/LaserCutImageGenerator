import json
from LaserCutImageGenerator.lasercv.param import Param


def _decode_param(data: dict) -> Param:
    p = Param(
        mode=data['mode'],
        width=data['width'],
        height=data['height'],
        threshold=data['threshold'],
        num_iter_bold=data['num_iter_bold'],
        num_iter_closing=data['num_iter_closing'],
        blur_size=data['blur_size'],
        detect_white=data['detect_white'],
        detect_black=data['detect_black'],
        detect_gray=data['detect_gray'],
        detect_red=data['detect_red'],
        detect_blue=data['detect_blue'],
        detect_green=data['detect_green'],
        detect_yellow=data['detect_yellow'],
        detect_orange=data['detect_orange'],
        detect_pink=data['detect_pink'],
        detect_purple=data['detect_purple'],
        detect_brown=data['detect_brown'],
        detect_gold=data['detect_gold'],
        detect_silver=data['detect_silver']
    )
    return p


def get_json_obj(path: str):
    param_file = open(path, 'r', encoding="utf-8")
    params: [Param] = json.load(                # type: ignore
        param_file, object_hook=_decode_param)
    return params
