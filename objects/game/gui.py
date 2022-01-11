class gui():
    def __init__(self):
        self.label_health = []

        self.time = text_label(
            settings.width / 2, settings.height - settings.height / 40,
            '100',
            load_font=True, font='pixel.ttf', size=settings.height//36,
            anchor_x='center', color=(150, 150, 150, 255)
        )

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

        self.old_perf_counter = 0

    def update(self):
        for i in range(4):
            if get_obj_display('players').tanks[i].use:
                self.label_health[i][2].label.text = ('HEALTH: ' + str(get_obj_display('players').tanks[i].health)) if not get_obj_display('players').tanks[i].death_bool else 'dead'
                if i in [1, 3]:
                    self.label_health[i][1].rec.x = self.health_pos[i][0] + (settings.width//4 - (((settings.width/4)/100) * get_obj_display('players').tanks[i].health))
                self.label_health[i][1].rec.width = ((settings.width/4)/100) * get_obj_display('players').tanks[i].health if not get_obj_display('players').tanks[i].death_bool else 0

        if game_settings.time_bool:
            if not get_obj_display('game_settings').pause:
                get_obj_display('world').time -= time.perf_counter() - self.old_perf_counter
                time_split = str(datetime.timedelta(seconds=get_obj_display('world').time)).split(':')
                self.time.label.text = time_split[1] + ':' + time_split[2].split('.')[0]

    def draw(self):
        for i in range(4):
            if get_obj_display('players').tanks[i].use:
                for l in self.label_health[i]:
                    l.draw()

        if game_settings.time_bool:
            self.time.draw()
