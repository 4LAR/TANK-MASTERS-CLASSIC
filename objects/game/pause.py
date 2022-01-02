class pause():
    def __init__(self):
        self.head = head_menu('pause')
        self.head_down = head_menu(align_top=False)

        self.continue_button = image_button(0, settings.height/4, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='get_obj_display(\'game_settings\').pause = False', image_selected='buttons/button_clear_selected.png', text='continue', text_indent= settings.height//100)
        self.exit_button = image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='get_obj_display(\'game_settings\').pause = False; select_map()', image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100)

    def on_mouse_press(self, x, y, button, modifiers):
        if get_obj_display('game_settings').pause:
            self.continue_button.on_mouse_press(x, y, button, modifiers)
            self.exit_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if get_obj_display('game_settings').pause:
            self.continue_button.on_mouse_motion(x, y, dx, dy)
            self.exit_button.on_mouse_motion(x, y, dx, dy)

    def draw(self):
        if get_obj_display('game_settings').pause:
            drawp(self.head)
            drawp(self.head_down)
            drawp(self.continue_button)
            drawp(self.exit_button)
