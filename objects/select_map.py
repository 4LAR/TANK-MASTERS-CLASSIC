class select_map_buttons():
    def __init__(self):
        self.buttons = []
        self.image_maps = []
        for y in range(2):
            for x in range(5):
                self.buttons.append(
                    image_button(x * settings.width/5 + settings.width/50,
                        (settings.height - settings.height/2.5) - (y * settings.height/3),
                        'buttons/ramka.png', scale=settings.height/120,
                        center=False, function=settings_menu,
                        image_selected='buttons/ramka_selected.png'
                        #text='settings',
                        #text_indent= settings.height//100)
                    )
                )

                self.image_maps.append(
                    image_label('file_not_found.png',
                        x * settings.width/5 + settings.width/50 + settings.width/200,
                        (settings.height - settings.height/2.5) - (y * settings.height/3 - settings.height/100),
                        scale=settings.height/130, pixel=True
                    )
                )

    def on_mouse_press(self, x, y, button, modifiers):
        for b in self.buttons:
            b.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for b in self.buttons:
            b.on_mouse_motion(x, y, dx, dy)

    def draw(self):
        for b in self.image_maps:
            drawp(b)
        for b in self.buttons:
            drawp(b)
