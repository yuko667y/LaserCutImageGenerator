from dataclasses import dataclass


class MODE(str):
    Felt = 'Felt'
    Seaweed = 'Seaweed'


@dataclass
class Param:
    mode: MODE
    width: int
    height: int
    threshold: int
    num_iter_bold: int
    num_iter_closing: int
    blur_size: int
    detect_white: bool
    detect_black: bool
    detect_gray: bool
    detect_red: bool
    detect_blue: bool
    detect_green: bool
    detect_yellow: bool
    detect_orange: bool
    detect_pink: bool
    detect_purple: bool
    detect_brown: bool
    detect_gold: bool
    detect_silver: bool
