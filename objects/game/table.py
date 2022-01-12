class table_game():
    def __init__(self, end_game=False):
        self.end_game = end_game

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
        for i in range( (len(get_obj_display('end_game_table').info['players'])) if self.end_game else (len(get_obj_display('players').tanks)) ):
            self.score_text.append([])
            self.score_text[i].append(
                text_label(
                    settings.width / 2.5 + settings.width/100,
                    settings.height / 9.2 + (settings.height / 1.4) - (settings.height / 15) * (i + 1),
                    'name',
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )

            self.score_text[i].append(
                text_label(
                    settings.width / 2.5 + settings.width/100 + settings.width/3.3,
                    settings.height / 9.2 + (settings.height / 1.4) - (settings.height / 15) * (i + 1),
                    'score',
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )
            self.score_text[i].append(
                text_label(
                    settings.width / 2.5 + settings.width/100 + settings.width/3.3 + settings.width/10,
                    settings.height / 9.2 + (settings.height / 1.4) - (settings.height / 15) * (i + 1),
                    'kills',
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )
            self.score_text[i].append(
                text_label(
                    settings.width / 2.5 + settings.width/100 + settings.width/3.3 + settings.width/5,
                    settings.height / 9.2 + (settings.height / 1.4) - (settings.height / 15) * (i + 1),
                    'death',
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )

        if self.end_game:
            for i in range(len(get_obj_display('end_game_table').info['players'])-1, -1, -1):
                player = get_obj_display('end_game_table').info['players'][i]
                if player['use']:
                    self.score_text[i][0].label.text = player['name']
                    self.score_text[i][1].label.text = str(player['score'])
                    self.score_text[i][2].label.text = str(player['kills'])
                    self.score_text[i][3].label.text = str(player['death'])

                else:
                    self.score_text[i][0].label.text = 'none'
                    self.score_text[i][1].label.text = 'none'
                    self.score_text[i][2].label.text = 'none'
                    self.score_text[i][3].label.text = 'none'

    def update(self):
        if not self.end_game:
            if get_obj_display('game_settings').pause:
                for i in range(len(get_obj_display('players').tanks)-1, -1, -1):
                    if get_obj_display('players').tanks[i].use:
                        self.score_text[i][0].label.text = get_obj_display('players').tanks[i].name
                        self.score_text[i][1].label.text = str(get_obj_display('players').tanks[i].score)
                        self.score_text[i][2].label.text = str(get_obj_display('players').tanks[i].kills)
                        self.score_text[i][3].label.text = str(get_obj_display('players').tanks[i].death)
                    else:
                        self.score_text[i][0].label.text = 'none'
                        self.score_text[i][1].label.text = 'none'
                        self.score_text[i][2].label.text = 'none'
                        self.score_text[i][3].label.text = 'none'

    def draw(self):
        if get_obj_display('game_settings').pause or self.end_game:
            self.score_panel.draw()
            for l in self.score_lines:
                l.draw()
            for t in self.score_panel_text:
                t.draw()

            for i in range( (len(get_obj_display('end_game_table').info['players'])) if self.end_game else (len(get_obj_display('players').tanks)) ):
                for t in self.score_text[i]:
                    t.draw()
