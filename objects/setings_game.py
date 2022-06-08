#
#
# 16.03.2021
#


class setings_game(): # класс который содержит себе информацию о разрешениях и считывает нажатия определённых кнопок
    def __init__(self):
        self.draw_poligons = False # разрешение на прорисовку полигонов
        self.draw_info_text = False # разрешение на прорисовку информации о игроке
        self.draw_console = False # разрешение на прорисовку и использование консоли

        self.draw_rain = False # разрешение на прорисовку дождя

        self.pause = False

    def on_key_press(self, symbol, modifiers): #
        if settings.console:
            if symbol == key.F1: # если мы нажали F1, то мы включаем консоль или выключаем (запрещаем движку всё кроме прорисовки и считывание нажатие клавиш)
                if self.draw_console:
                    self.draw_console = False
                    engine_settings.on_text_bool = False
                    engine_settings.on_mouse_motion_bool   = True
                    engine_settings.on_mouse_drag_bool     = True
                    engine_settings.on_mouse_press_bool    = True
                    engine_settings.on_mouse_release_bool  = True
                else:
                    self.draw_console = True
                    engine_settings.on_text_bool = True
                    engine_settings.on_mouse_motion_bool   = False
                    engine_settings.on_mouse_drag_bool     = False
                    engine_settings.on_mouse_press_bool    = False
                    engine_settings.on_mouse_release_bool  = False


            if symbol == key.F3: # если мы нажали F3, то изменяем показ полигонов
                if self.draw_poligons:
                    self.draw_poligons = False
                else:
                    self.draw_poligons = True

            if symbol == key.F4:
                get_obj_display('world').shaking()

            if symbol == key.F5:
                if self.pause:
                    self.pause = False
                    engine_settings.on_update_bool = True

                else:
                    self.pause = True
                    engine_settings.on_update_bool = False


# добавляем классы в основной цикл
add_objects_other(setings_game())
