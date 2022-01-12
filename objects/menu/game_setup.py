class game_setup_flags():

    def read_settings(self):
        self.settings_flags[0].flag = game_settings.scatter_bool
        self.settings_flags[1].flag = game_settings.wind_bool
        self.settings_flags[2].flag = game_settings.rain
        self.settings_flags[3].flag = game_settings.snow

        self.settings_flags[4].flag = game_settings.collide_players

        self.settings_flags[5].flag = game_settings.time_bool
        self.settings_flags[6].text_obj.text_label.label.text = str(game_settings.time_set_min)
        self.settings_flags[7].text_obj.text_label.label.text = str(game_settings.time_set_sec)

    def save_settings(self):

        # 0 - scatter
        # 1 - wind
        # 2 - rain
        # 3 - snow
        # 4 - time bool
        # 5 - time min
        # 6 - time sec

        game_settings.scatter_bool = self.settings_flags[0].flag
        game_settings.wind_bool    = self.settings_flags[1].flag
        game_settings.rain         = self.settings_flags[2].flag
        game_settings.snow         = self.settings_flags[3].flag

        game_settings.collide_players = self.settings_flags[4].flag

        game_settings.time_bool    = self.settings_flags[5].flag
        game_settings.time_set_min = int(self.settings_flags[6].text_obj.text_label.label.text)
        game_settings.time_set_sec = int(self.settings_flags[7].text_obj.text_label.label.text)

        save_settings.save_settings()

    def reset(self):
        self.settings_flags[0].flag = True
        self.settings_flags[1].flag = True
        self.settings_flags[2].flag = False
        self.settings_flags[3].flag = False

        self.settings_flags[4].flag = True

        self.settings_flags[5].flag = True
        self.settings_flags[6].text_obj.text_label.label.text = '2'
        self.settings_flags[7].text_obj.text_label.label.text = '0'

    def __init__(self):

        self.settings_flags = []

        # 1 column
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
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

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
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

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
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

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
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        # 3 column
        self.settings_flags.append(
            image_flag(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/4.5 - (settings.height/8) * 4,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='players collide',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        self.settings_flags.append(
            image_flag(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/4.5 - (settings.height/8) * 0,
                image='buttons/flag_small/flag.png',
                image_flag='buttons/flag_small/flag_selected.png',
                image_selected_flag='buttons/flag_small/flag_hover_selected.png',
                image_selected='buttons/flag_small/flag_hover.png',
                scale=settings.height/160,

                text='time',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        self.settings_flags.append(
            input_label_image(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/2.8 - (settings.height/8) * 0,
                'buttons/button_clear_2_reverse.png', 'buttons/button_clear_selected_2_reverse.png',
                scale=settings.height/160, color_text=(150, 150, 150, 255),
                text='minutes', pre_text='2', font='pixel.ttf',
                text_indent=settings.height/12, text_input_indent=settings.height/6, shadow=graphics_settings.shadows_buttons
            )
        )

        self.settings_flags.append(
            input_label_image(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/2.8 - (settings.height/8) * 1,
                'buttons/button_clear_2_reverse.png', 'buttons/button_clear_selected_2_reverse.png',
                scale=settings.height/160, color_text=(150, 150, 150, 255),
                text='seconds', pre_text='0', font='pixel.ttf',
                text_indent=settings.height/12, text_input_indent=settings.height/6, shadow=graphics_settings.shadows_buttons
            )
        )

        self.read_settings()

    def on_mouse_press(self, x, y, button, modifiers):
        for s in self.settings_flags:
            s.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for s in self.settings_flags:
            s.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        for s in self.settings_flags:
            try:
                s.on_key_press(symbol, modifiers)
            except:
                pass

    def on_text(self, text):
        for s in self.settings_flags:
            try:
                s.on_text(text)
            except:
                pass

    def draw(self):
        for s in self.settings_flags:
            drawp(s)
