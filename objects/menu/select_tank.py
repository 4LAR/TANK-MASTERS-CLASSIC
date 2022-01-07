class select_tank_buttons():
    def tank_up(self, id, type=0):
        self.tank_settings[id][type] += 1
        if self.tank_settings[id][type] > ((len(tanks.bases)-1) if type == 0 else (len(tanks.towers)-1)):
            self.tank_settings[id][type] = 0
        self.update_tanks()

    def tank_down(self, id, type=0):
        self.tank_settings[id][type] -= 1
        if self.tank_settings[id][type] < 0:
            self.tank_settings[id][type] = (len(tanks.bases)-1) if type == 0 else (len(tanks.towers)-1)
        self.update_tanks()

    def update_tanks(self):
        self.image_body = []
        self.image_tower = []
        self.image_team = []
        for i in range(4):
            self.image_body.append(
                image_label(
                    'tanks/body/no_team/' + tanks.bases[self.tank_settings[i][0]] + '.png',
                    settings.width/12 + (i * settings.width/4),
                    settings.height - settings.height/2.1,
                    scale=settings.height/120, pixel=True
                )
            )
            self.image_tower.append(
                image_label(
                    'tanks/tower/' + tanks.towers[self.tank_settings[i][1]] + '.png',
                    settings.width/12 + (i * settings.width/4),
                    settings.height - settings.height/2.1,
                    scale=settings.height/120, pixel=True
                )
            )
            self.image_team.append(
                image_label(
                    'tanks/body/' + tanks.teams[i] + '/' + tanks.bases[self.tank_settings[i][0]] + '.png',
                    settings.width/12 + (i * settings.width/4),
                    settings.height - settings.height/2.1,
                    scale=settings.height/120, pixel=True
                )
            )

    def __init__(self):
        self.background = []
        self.buttons = []
        self.buttons_bot = []
        self.text = []
        self.text_bot = []
        self.background_tank = []

        self.image_body = []
        self.image_tower = []
        self.image_team = []

        self.tank_settings = [[0, 1], [0, 1], [0, 1], [0, 1]]

        self.buttons_body_up = []
        self.buttons_body_down = []
        self.buttons_tower_up = []
        self.buttons_tower_down = []

        self.update_tanks()
        for i in range(4):
            # фон настроек танка
            self.background_tank.append(
                image_label(
                    'menu/select tank/tank_background.png',
                    settings.width/15.9 + (i * settings.width/4),
                    settings.height - settings.height/1.9375,
                    scale=settings.height/160, pixel=True
                )
            )

            # кнопки выбора деталей танка
            self.buttons_body_up.append(
                image_button(
                    settings.width/5.58 + (i * settings.width/4),
                    settings.height - settings.height/2.4,
                    'buttons/button_right_page.png',
                    image_selected='buttons/button_right_page_selected.png',
                    scale=settings.height/160, center=False, arg='get_obj_display(\'select_tank_buttons\').tank_up('+str(i)+', 1)'
                )
            )
            self.buttons_body_down.append(
                image_button(
                    settings.width/100 + (i * settings.width/4),
                    settings.height - settings.height/2.4,
                    'buttons/button_left_page.png',
                    image_selected='buttons/button_left_page_selected.png',
                    scale=settings.height/160, center=False, arg='get_obj_display(\'select_tank_buttons\').tank_down('+str(i)+', 1)'
                )
            )
            self.buttons_tower_up.append(
                image_button(
                    settings.width/5.58 + (i * settings.width/4),
                    settings.height - settings.height/1.94,
                    'buttons/button_right_page.png',
                    image_selected='buttons/button_right_page_selected.png',
                    scale=settings.height/160, center=False, arg='get_obj_display(\'select_tank_buttons\').tank_up('+str(i)+', 0)'
                )
            )
            self.buttons_tower_down.append(
                image_button(
                    settings.width/100 + (i * settings.width/4),
                    settings.height - settings.height/1.94,
                    'buttons/button_left_page.png',
                    image_selected='buttons/button_left_page_selected.png',
                    scale=settings.height/160, center=False, arg='get_obj_display(\'select_tank_buttons\').tank_down('+str(i)+', 0)'
                )
            )

            # флаг выбора игрока
            self.buttons.append(
                image_flag(
                    settings.width/100 + (i * settings.width/4),
                    settings.height - settings.height/5,
                    image='menu/select tank/flag.png',
                    image_flag='menu/select tank/flag_selected.png',
                    image_selected_flag='menu/select tank/flag_hover_selected.png',
                    image_selected='menu/select tank/flag_hover.png',
                    scale=settings.height/160, shadow=graphics_settings.shadows_buttons

                )
            )

            # флаг на включения бота
            self.buttons_bot.append(
                image_flag(
                    settings.width/100 + (i * settings.width/4),
                    settings.height - settings.height/3.34,
                    image='menu/select tank/flag.png',
                    image_flag='menu/select tank/flag_selected.png',
                    image_selected_flag='menu/select tank/flag_hover_selected.png',
                    image_selected='menu/select tank/flag_hover.png',
                    scale=settings.height/160, shadow=graphics_settings.shadows_buttons

                )
            )

            # фон настроек игрока
            self.background.append(
                image_label(
                    'menu/select tank/background.png',
                    settings.width/100 + (i * settings.width/4),
                    settings.height - settings.height/1.45,
                    scale=settings.height/160, pixel=True, shadow=graphics_settings.shadows_buttons
                )
            )

            # текст
            self.text.append(
                text_label(
                    settings.width/12 + (i * settings.width/4),
                    settings.height - settings.height/5.6,
                    'player ' + str(i + 1),
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )

            self.text_bot.append(
                text_label(
                    settings.width/12 + (i * settings.width/4),
                    settings.height - settings.height/3.6,
                    'bot',
                    load_font=True, font='pixel.ttf',
                    size=settings.height//24, anchor_x='left', anchor_y='bottom',
                    color = (150, 150, 150, 255)
                )
            )

        self.buttons[0].flag = True

    def on_mouse_press(self, x, y, button, modifiers):
        for i in range(len(self.buttons)):
            self.buttons[i].on_mouse_press(x, y, button, modifiers)
            if self.buttons[i].flag:
                self.buttons_bot[i].on_mouse_press(x, y, button, modifiers)

                self.buttons_body_down[i].on_mouse_press(x, y, button, modifiers)
                self.buttons_body_up[i].on_mouse_press(x, y, button, modifiers)
                self.buttons_tower_down[i].on_mouse_press(x, y, button, modifiers)
                self.buttons_tower_up[i].on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for i in range(len(self.buttons)):
            self.buttons[i].on_mouse_motion(x, y, dx, dy)
            if self.buttons[i].flag:
                self.buttons_bot[i].on_mouse_motion(x, y, dx, dy)

                self.buttons_body_down[i].on_mouse_motion(x, y, dx, dy)
                self.buttons_body_up[i].on_mouse_motion(x, y, dx, dy)
                self.buttons_tower_down[i].on_mouse_motion(x, y, dx, dy)
                self.buttons_tower_up[i].on_mouse_motion(x, y, dx, dy)

    def draw(self):
        for i in range(len(self.buttons)):
            if self.buttons[i].flag:
                drawp(self.background[i])

            if self.buttons[i].flag:
                drawp(self.buttons_bot[i])
                drawp(self.text_bot[i])

                drawp(self.background_tank[i])

                drawp(self.image_body[i])
                drawp(self.image_team[i])
                drawp(self.image_tower[i])

                drawp(self.buttons_body_down[i])
                drawp(self.buttons_body_up[i])
                drawp(self.buttons_tower_down[i])
                drawp(self.buttons_tower_up[i])

            drawp(self.buttons[i])
            drawp(self.text[i])
