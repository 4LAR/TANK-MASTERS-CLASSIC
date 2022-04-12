class select_map_filter_buttons():
    def __init__(self):
        self.flags = []

        flags_names = ['DM', 'CP', 'RC']

        for i in range(len(flags_names)):
            self.flags.append(
                image_flag(
                    settings.width/100,
                    (settings.height - settings.height/4.0) - (i * settings.height/8),
                    image='buttons/flag_small/flag.png',
                    image_flag='buttons/flag_small/flag_selected.png',
                    image_selected_flag='buttons/flag_small/flag_hover_selected.png',
                    image_selected='buttons/flag_small/flag_hover.png',
                    scale=settings.height/160,

                    text=flags_names[i],
                    text_color = (150, 150, 150, 255),
                    font='pixel.ttf',
                    text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

                )
            )

            self.flags[i].flag = True

        self.background = label(
            settings.width/300,
            settings.height - settings.height/3.5 - (settings.height/8) * 1.8,
            (settings.width / 2.15) / 1.95,
            settings.height/2.30,
            (0, 0, 0), alpha=120
        )

        self.backgraund_text = text_label(
            settings.width/100,
            settings.height - settings.height/3.5 + (settings.height/8) * 1.2,
            'filter',
            load_font=True, font='pixel.ttf',
            size=settings.height//24, anchor_x='left', anchor_y='bottom',
            color = (150, 150, 150, 255)
        )

    def on_mouse_press(self, x, y, button, modifiers):
        for f in self.flags:
            f.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for f in self.flags:
            f.on_mouse_motion(x, y, dx, dy)

    def draw(self):
        self.background.draw()
        self.backgraund_text.draw()
        for f in self.flags:
            f.draw()
