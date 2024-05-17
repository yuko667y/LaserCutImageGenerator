import PySimpleGUI as sg
from LaserCutImageGenerator.lasercv.param import Param


class SimpleGui():
    param = None
    _layout = None
    _window = None

    def __init__(self, param: Param):
        self.param = param
        self._set_layout()
        self._set_window()

    def __del__(self):
        self._window.close()

    def _set_layout(self):
        self._layout = [
            [
                sg.Button('Exit & Save', size=(30, 3), key='BUTTON'),
            ],
            [
                sg.Text('threshold'),
                sg.Slider((0, 255), self.param.threshold, 1, orientation='h',
                          disable_number_display=False, enable_events=True, key='SLIDER_threshold')
            ],
            [
                sg.Text('num_iter_bold'),
                sg.Slider((0, 10), self.param.num_iter_bold, 1, orientation='h',
                          disable_number_display=False, enable_events=True, key='SLIDER_num_iter_bold')
            ],
            [
                sg.Text('num_iter_closing'),
                sg.Slider((0, 10), self.param.num_iter_closing, 1, orientation='h',
                          disable_number_display=False, enable_events=True, key='SLIDER_num_iter_closing')
            ],
            [
                sg.Text('blur_size'),
                sg.Slider((0, 30), self.param.blur_size, 1, orientation='h',
                          disable_number_display=False, enable_events=True, key='SLIDER_blur_size')
            ],
            [
                sg.Text('Detect Colors'),
                sg.Checkbox('White', default=self.param.detect_white,
                            enable_events=True, key='CHECK_white'),
                sg.Checkbox('Black', default=self.param.detect_black,
                            enable_events=True, key='CHECK_black'),
                sg.Checkbox('Gray', default=self.param.detect_gray,
                            enable_events=True, key='CHECK_gray'),
                sg.Checkbox('Red', default=self.param.detect_red,
                            enable_events=True, key='CHECK_red'),
                sg.Checkbox('Blue', default=self.param.detect_blue,
                            enable_events=True, key='CHECK_blue'),
                sg.Checkbox('Green', default=self.param.detect_green,
                            enable_events=True, key='CHECK_green'),
                sg.Checkbox('Yellow', default=self.param.detect_yellow,
                            enable_events=True, key='CHECK_yellow'),
                sg.Checkbox('Orange', default=self.param.detect_orange,
                            enable_events=True, key='CHECK_orange'),
                sg.Checkbox('Pink', default=self.param.detect_pink,
                            enable_events=True, key='CHECK_pink'),
                sg.Checkbox('Purple', default=self.param.detect_purple,
                            enable_events=True, key='CHECK_purple'),
                sg.Checkbox('Brown', default=self.param.detect_brown,
                            enable_events=True, key='CHECK_brown'),
                sg.Checkbox('Gold', default=self.param.detect_gold,
                            enable_events=True, key='CHECK_gold'),
                sg.Checkbox('Silver', default=self.param.detect_silver,
                            enable_events=True, key='CHECK_silver'),
            ]
        ]

    def _set_window(self):
        self._window = sg.Window(
            title='Window title',
            layout=self._layout
        )
        self._window.finalize()

    def process(self):
        """ GUI process

        @note call at while in main()
         """
        event_ret, param_ret = True, False
        event, values = self._window.read(timeout=None)
        if event is None:
            event_ret = False
        elif event == 'BUTTON':
            event_ret = False
        elif event == 'SLIDER_threshold':
            self.param.threshold = int(values['SLIDER_threshold'])
            param_ret = True
        elif event == 'SLIDER_num_iter_bold':
            self.param.num_iter_bold = int(values['SLIDER_num_iter_bold'])
            param_ret = True
        elif event == 'SLIDER_num_iter_closing':
            self.param.num_iter_closing = int(
                values['SLIDER_num_iter_closing'])
            param_ret = True
        elif event == 'SLIDER_blur_size':
            self.param.blur_size = int(values['SLIDER_blur_size'])
            param_ret = True
        elif event.startswith('CHECK_'):
            color = event.split('_')[1]
            setattr(self.param, f"detect_{color.lower()}", values[event])
            param_ret = True
        else:
            print(event)
        return event_ret, param_ret
