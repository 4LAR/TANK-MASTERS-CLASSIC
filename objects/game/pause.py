class pause():
    def __init__(self):
        self.head = head_menu('pause')
        self.head_down = head_menu(align_top=False)

        self.continue_button = image_button(0, settings.height/4, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='get_obj_display(\'game_settings\').pause = False', image_selected='buttons/button_clear_selected.png', text='continue', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons)
        self.exit_button = image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='get_obj_display(\'game_settings\').pause = False; select_map()', image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons)

        self.score_panel = label(
            settings.width / 2.5, settings.height / 10,
            settings.width / 1.5, settings.height - settings.height / 5,
            (0, 0, 0), alpha = 128
        )

        # text name columns
        self.score_panel_text = []
        self.score_panel_text.append(
            text_label(
                settings.width / 2 + settings.width/20,
                settings.height / 1.2,
                'name',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )
        self.score_panel_text.append(
            text_label(
                settings.width / 2 + settings.width/100 + settings.width/5,
                settings.height / 1.2,
                'score',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )
        self.score_panel_text.append(
            text_label(
                settings.width / 2 + settings.width/100 + settings.width/10 + settings.width/5,
                settings.height / 1.2,
                'kills',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )
        self.score_panel_text.append(
            text_label(
                settings.width / 2 + settings.width/100 + settings.width/5 + settings.width/5,
                settings.height / 1.2,
                'death',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )

        # lines columns
        self.score_lines = []
        self.score_lines.append(
            label(
                settings.width / 2 + settings.width/5, settings.height / 10,
                settings.width / 200, settings.height - settings.height / 5,
                (150, 150, 150), alpha = 255
            )
        )
        self.score_lines.append(
            label(
                settings.width / 2 + settings.width/5 + settings.width/10, settings.height / 10,
                settings.width / 200, settings.height - settings.height / 5,
                (150, 150, 150), alpha = 255
            )
        )
        self.score_lines.append(
            label(
                settings.width / 2 + settings.width/5 + settings.width/10 + settings.width/10, settings.height / 10,
                settings.width / 200, settings.height - settings.height / 5,
                (150, 150, 150), alpha = 255
            )
        )
        # horizontally
        self.score_lines.append(
            label(
                settings.width / 2.5, settings.height / 10 + settings.height / 1.4,
                settings.width / 1.5, settings.height/150,
                (150, 150, 150), alpha = 255
            )
        )

        for i in range(4):
            self.score_lines.append(
                label(
                    settings.width / 2.5, settings.height / 10 + (settings.height / 1.4) - (settings.height / 15) * (i + 1),
                    settings.width / 1.5, settings.height/150,
                    (150, 150, 150), alpha = 255
                )
            )

        self.score_text = []
        for i in range(len(get_obj_display('players').tanks)):
            self.score_text.append([])
            self.score_text[i].append(
                text_label(
                    settings.width / 2.5 + settings.width/100,
                    settings.height / 9.2 + (settings.height / 1.4) - (settings.height / 15) * (i + 1),
                    get_obj_display('players').tanks[(len(get_obj_display('players').tanks) - 1) - i].name,
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )

            self.score_text[i].append(
                text_label(
                    settings.width / 2.5 + settings.width/100 + settings.width/3.3,
                    settings.height / 9.2 + (settings.height / 1.4) - (settings.height / 15) * (i + 1),
                    str(get_obj_display('players').tanks[(len(get_obj_display('players').tanks) - 1) - i].score),
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )
            self.score_text[i].append(
                text_label(
                    settings.width / 2.5 + settings.width/100 + settings.width/3.3 + settings.width/10,
                    settings.height / 9.2 + (settings.height / 1.4) - (settings.height / 15) * (i + 1),
                    str(get_obj_display('players').tanks[(len(get_obj_display('players').tanks) - 1) - i].kills),
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )
            self.score_text[i].append(
                text_label(
                    settings.width / 2.5 + settings.width/100 + settings.width/3.3 + settings.width/5,
                    settings.height / 9.2 + (settings.height / 1.4) - (settings.height / 15) * (i + 1),
                    str(get_obj_display('players').tanks[(len(get_obj_display('players').tanks) - 1) - i].death),
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )

    def update(self):
        for i in range(len(get_obj_display('players').tanks)):
            self.score_text[i][0].label.text = get_obj_display('players').tanks[(len(get_obj_display('players').tanks) - 1) - i].name
            self.score_text[i][1].label.text = str(get_obj_display('players').tanks[(len(get_obj_display('players').tanks) - 1) - i].score)
            self.score_text[i][2].label.text = str(get_obj_display('players').tanks[(len(get_obj_display('players').tanks) - 1) - i].kills)
            self.score_text[i][3].label.text = str(get_obj_display('players').tanks[(len(get_obj_display('players').tanks) - 1) - i].death)

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

            self.score_panel.draw()
            for l in self.score_lines:
                l.draw()
            for t in self.score_panel_text:
                t.draw()
            for score_text in self.score_text:
                for t in score_text:
                    t.draw()
