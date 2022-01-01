class old_gui():
    def __init__(self):

        self.images_gui = []

        self.text_health = []
        self.text_ammo = []
        self.text_score = []

        self.pos = [
            [0, settings.height - settings.height/15],
            [settings.width - settings.width/8, settings.height - settings.height/15],
            [0, 0],
            [settings.width - settings.width/8, 0]
        ]

        self.pos_text = [
            [settings.width/80, settings.height - settings.height/15, 'left'],
            [settings.width - settings.width/80, settings.height - settings.height/15, 'right'],
            [settings.width/80, 0, 'left'],
            [settings.width - settings.width/80, 0, 'right']
        ]

        for i in range(4):
            self.images_gui.append(
                image_label('gui/ramka_' + tanks.teams[i] + '.png',
                    self.pos[i][0], self.pos[i][1],
                    scale=settings.height/240, pixel=True
                )
            )

            self.text_health.append(
                text_label(
                    self.pos_text[i][0], self.pos_text[i][1] + settings.height/18,
                    '100',
                    load_font=True, font='pixel.ttf', size=settings.height//72,
                    anchor_x=self.pos_text[i][2], color=(150, 150, 150, 255)
                )
            )

            self.text_ammo.append(
                text_label(
                    self.pos_text[i][0], self.pos_text[i][1] + settings.height/18 - settings.height/50,
                    '100',
                    load_font=True, font='pixel.ttf', size=settings.height//72,
                    anchor_x=self.pos_text[i][2], color=(150, 150, 150, 255)
                )
            )

            self.text_score.append(
                text_label(
                    self.pos_text[i][0], self.pos_text[i][1] + settings.height/18 - settings.height/50 - settings.height/50,
                    '100',
                    load_font=True, font='pixel.ttf', size=settings.height//72,
                    anchor_x=self.pos_text[i][2], color=(150, 150, 150, 255)
                )
            )

    def update(self):
        for i in range(4):
            if get_obj_display('players').tanks[i].use:
                self.text_health[i].label.text = str(get_obj_display('players').tanks[i].health) if not get_obj_display('players').tanks[i].death_bool else 'dead'

    def draw(self):
        for i in range(4):
            if get_obj_display('players').tanks[i].use:
                drawp(self.images_gui[i])
                drawp(self.text_health[i])
                drawp(self.text_ammo[i])
                drawp(self.text_score[i])

class gui():
    def __init__(self):
        self.label_health = []

        self.health_pos = [
            [settings.width/50, settings.height - settings.height/20],
            [settings.width - (settings.width/50 + settings.width//4), settings.height - settings.height/20],
            [settings.width/50, settings.height/40],
            [settings.width - (settings.width/50 + settings.width//4), settings.height/40]
        ]

        self.team_colors = [
            (128, 0, 0),
            (0, 0, 128),
            (0, 128, 0),
            (128, 128, 0)
        ]

        for i in range(4):
            self.label_health.append([])
            self.label_health[i].append(label(self.health_pos[i][0], self.health_pos[i][1], settings.width//4, settings.height//40, color=(0, 0, 0), alpha=250))
            self.label_health[i].append(label(self.health_pos[i][0], self.health_pos[i][1], ((settings.width/4)/100)*80, settings.height//40, color=self.team_colors[i], alpha=250))
            self.label_health[i].append(
                text_label(
                    self.health_pos[i][0] + (settings.width//4 if i in [1, 3] else 0),
                    self.health_pos[i][1] + (settings.height//40 if i in [2, 3] else 0),
                    'HEALTH: 100', load_font=True, font='pixel.ttf',
                    size=settings.height//40,
                    anchor_x='right' if i in [1, 3] else 'left',
                    color = (180, 180, 180, 250)
                )
            )

    def update(self):
        for i in range(4):
            if get_obj_display('players').tanks[i].use:
                self.label_health[i][2].label.text = ('HEALTH: ' + str(get_obj_display('players').tanks[i].health)) if not get_obj_display('players').tanks[i].death_bool else 'dead'
                if i in [1, 3]:
                    self.label_health[i][1].rec.x = self.health_pos[i][0] + (settings.width//4 - (((settings.width/4)/100) * get_obj_display('players').tanks[i].health))
                self.label_health[i][1].rec.width = ((settings.width/4)/100) * get_obj_display('players').tanks[i].health if not get_obj_display('players').tanks[i].death_bool else 0

    def draw(self):
        for i in range(4):
            if get_obj_display('players').tanks[i].use:
                for l in self.label_health[i]:
                    l.draw()
