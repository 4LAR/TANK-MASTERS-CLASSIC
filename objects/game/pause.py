class pause():
    def __init__(self, traning):
        self.traning = traning

        self.head = head_menu('pause')
        self.head_down = head_menu(align_top=False, draw_user=False)

        self.continue_button = image_button(0, settings.height/4, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='get_obj_display(\'game_settings\').pause = False', image_selected='buttons/button_clear_selected.png', text='continue', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons)
        self.exit_button = image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='game_settings.reload(); select_map()' if not self.traning else 'game_settings.reload(); training_start()', image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons)

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
