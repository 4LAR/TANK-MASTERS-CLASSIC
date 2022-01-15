class alert_buttons():
    def __init__(self):
        pass

class alert():
    def __init__(self):

        self.draw_bool = True

        self.background = label(0, 0, settings.width, settings.height, (0, 0, 0), alpha=128)
        self.alert_image = image_label('alert.png', settings.width/5, settings.height/2, scale=settings.height/120, pixel=True)

        self.text_obj = text_label(
            settings.width/2,#settings.width/4.8,
            settings.height/1.4,
            'hello world',
            load_font=True, font='pixel.ttf', size=settings.height//18,
            anchor_x='center', color=(150, 150, 150, 255)
        )

        self.button_yes = image_button(
            settings.width/5 + settings.width/200,
            settings.height/2,
            'buttons/button_clear.png', scale=settings.height/120,
            center=False, arg='pass',
            function=play_menu, image_selected='buttons/button_clear_selected.png',
            text='yes', text_indent=settings.height/8
            #shadow=graphics_settings.shadows_buttons
        )

        self.button_no = image_button(
            settings.width/5 + settings.width/2.73 + settings.width/200,
            settings.height/2,
            'buttons/button_clear_left.png', scale=settings.height/120,
            center=False, arg='get_obj_display(\'alert\').draw_bool = False',
            function=play_menu, image_selected='buttons/button_clear_left_selected.png',
            text='no', text_indent=settings.height/8
            #shadow=graphics_settings.shadows_buttons
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if self.draw_bool:
            self.button_yes.on_mouse_press(x, y, button, modifiers)
            self.button_no.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.draw_bool:
            self.button_yes.on_mouse_motion(x, y, dx, dy)
            self.button_no.on_mouse_motion(x, y, dx, dy)

    def draw(self):
        if self.draw_bool:
            self.background.draw()
            drawp(self.alert_image)

            drawp(self.button_yes)
            drawp(self.button_no)

            drawp(self.text_obj)
