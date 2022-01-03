class game_setup_flags():

    def read_settings(self):
        self.settings_flags[0].flag = game_settings.scatter_bool
        self.settings_flags[1].flag = game_settings.wind_bool
        self.settings_flags[2].flag = game_settings.rain
        self.settings_flags[3].flag = game_settings.snow

    def save_settings(self):

        # 0 - scatter
        # 1 - wind
        # 2 - rain
        # 3 - snow

        game_settings.scatter_bool = self.settings_flags[0].flag
        game_settings.wind_bool    = self.settings_flags[1].flag
        game_settings.rain         = self.settings_flags[2].flag
        game_settings.snow         = self.settings_flags[3].flag


    def __init__(self):

        self.settings_flags = []

        self.settings_flags.append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/4.5 - (settings.height/8) * 0,
                image='buttons/flag_small/flag.png',
                image_flag='buttons/flag_small/flag_selected.png',
                image_selected_flag='buttons/flag_small/flag_hover_selected.png',
                image_selected='buttons/flag_small/flag_hover.png',
                scale=settings.height/160,

                text='scatter',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8

            )
        )

        self.settings_flags.append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/4.5 - (settings.height/8) * 1,
                image='buttons/flag_small/flag.png',
                image_flag='buttons/flag_small/flag_selected.png',
                image_selected_flag='buttons/flag_small/flag_hover_selected.png',
                image_selected='buttons/flag_small/flag_hover.png',
                scale=settings.height/160,

                text='wind',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8

            )
        )

        self.settings_flags.append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/4.5 - (settings.height/8) * 2,
                image='buttons/flag_small/flag.png',
                image_flag='buttons/flag_small/flag_selected.png',
                image_selected_flag='buttons/flag_small/flag_hover_selected.png',
                image_selected='buttons/flag_small/flag_hover.png',
                scale=settings.height/160,

                text='rain',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8

            )
        )

        self.settings_flags.append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/4.5 - (settings.height/8) * 3,
                image='buttons/flag_small/flag.png',
                image_flag='buttons/flag_small/flag_selected.png',
                image_selected_flag='buttons/flag_small/flag_hover_selected.png',
                image_selected='buttons/flag_small/flag_hover.png',
                scale=settings.height/160,

                text='snow',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8

            )
        )

        self.read_settings()

    def on_mouse_press(self, x, y, button, modifiers):
        for s in self.settings_flags:
            s.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for s in self.settings_flags:
            s.on_mouse_motion(x, y, dx, dy)

    def draw(self):
        for s in self.settings_flags:
            drawp(s)
