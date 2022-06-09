#
#
#
#

class Engine_settings():
    def __init__(self):
        self.on_text_bool           = False # разрешение на ввод текста
        self.on_mouse_motion_bool   = False # разрешение на получение информации о положении мыши (не работает когда нажата клавиша)
        self.on_mouse_drag_bool     = False # разрешение на получение информации о положении мыши (работает когда нажата клавиша)
        self.on_key_press_bool      = False # разрешение на получение информации о клавишах клавиатуры (нажатие)
        self.on_mouse_press_bool    = False # разрешение на получение информации о клавишах мыши (нажатие)
        self.on_mouse_scroll_bool   = False # разрешение на получение информации о клавишах мыши (скроллинг)
        self.on_mouse_release_bool  = False # разрешение на получение информации о клавишах мыши (отпускание)
        self.on_draw_bool           = False # разрешение на прорисовку
        self.on_update_bool         = False # разрешение на обновление всез классов

        self.window_event_list = { #
            'on_text': 'text',
            'on_mouse_motion': 'x, y, dx, dy',
            'on_mouse_drag': 'x, y, dx, dy, buttons, modifiers',
            'on_key_press': 'symbol, modifiers',
            'on_mouse_press': 'x, y, button, modifiers',
            'on_mouse_scroll': 'x, y, scroll_x, scroll_y',
            'on_mouse_release': 'x, y, button, modifiers'
        }
