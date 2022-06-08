class players():
    def __init__(self, bot, tanks, tank_settings, enemy_bool=False, enemy_count=0, enemy_bots=False, traning=False):
        self.tanks = []

        for i in range(4):
            self.tanks.append(player(i, bot[i], tank_settings[i], tanks[i]))

        try:
            for i in range(enemy_count):
                self.tanks.append(player(4 + i, enemy_bots, tank_settings[0], True, True, traning))
        except Exception as e:
            print(e)

    def update(self):
        for tank in self.tanks:
            tank.update()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            if get_obj_display('game_settings').pause:
                get_obj_display('game_settings').pause = False
                hide_cursor()
            else:
                get_obj_display('game_settings').pause = True
                show_cursor()

            return pyglet.event.EVENT_HANDLED

    def draw(self):
        for tank in self.tanks:
            tank.draw()

class player():
    def go_spawn(self):
        if self.use:
            try:
                self.pos = [
                    get_obj_display('world').image_floor.x + (get_obj_display('world').spawn[self.id][0] * get_obj_display('world').size * get_obj_display('world').scale) - get_obj_display('world').map_offs[0],
                    get_obj_display('world').image_floor.y + ((get_obj_display('world').world_size[1] - get_obj_display('world').spawn[self.id][1]) * get_obj_display('world').size * get_obj_display('world').scale) - get_obj_display('world').map_offs[1]
                ]

                self.pos[0] += self.obj_tanks[0].width/4
                self.pos[1] -= self.obj_tanks[0].height/4

            except:
                self.pos = [settings.width//2, settings.height//2]
        else:
            self.pos = [-settings.width, -settings.height]

    def __init__(self, id, bot=False, tank_settings=[0, 0], use=True, enemy_bool=False, traning=False):

        self.traning = traning

        self.enemy_bool = enemy_bool

        self.name = 'PLAYER ' + str(id + 1) + (' BOT' if bot else '')

        # info
        self.score = 0
        self.kills = 0
        self.death = 0

        self.ping = 0

        self.tank_settings = tank_settings
        self.use = use

        self.sound = Sound()

        if sound_settings.use_sound_general and sound_settings.use_sound_tanks:
            self.sound.sound_volume(settings.sound_volume * sound_settings.sound_volume_tanks)
        else:
            self.sound.sound_volume(0)

        self.id = id
        self.bot = bot

        self.check_fps = 60
        self.norm_fps = 75

        self.pos = [0, 0]

        self.scale_tank = get_obj_display('world').scale / 1.2

        self.default_health = 100
        self.health = 100
        self.armor_bool = False

        self.protection = False
        self.protection_delay = 2
        self.protection_time = time.perf_counter() + self.protection_delay

        self.protection_ticks = 0
        self.protection_image_num = 0
        self.protection_images = []
        self.protection_up_images = []

        for i in range(4):
            self.protection_images.append(
                image_label(
                    'tanks/protection/protection_' + str(i + 1) + '.png',
                    settings.width//2, settings.height//2,
                    scale=self.scale_tank * 1.2, pixel=False,
                    center=True
                )
            )

            self.protection_up_images.append(
                image_label(
                    'tanks/protection_up/protection_' + str(i + 1) + '.png',
                    settings.width//2, settings.height//2,
                    scale=self.scale_tank * 1.2, pixel=False,
                    center=True
                )
            )



        self.death_bool = False
        self.death_delay = 2
        self.death_time = time.perf_counter() + self.death_delay

        self.demage_a = tanks.towers_damage[self.tank_settings[1]]

        self.def_speed = [tanks.bases_speed[self.tank_settings[0]]]
        self.speed_tick = self.def_speed[0]/10 # 0
        self.speed = 0
        self.rotation = -90 if self.traning else 0

        # bot
        self.bot_rotation = 0
        self.time_random_rotation = 0
        self.bot_shoot_a = True

        self.wall_collision_bool = False

        # for animations
        self.anim_ticks = 0
        self.anim_body_state = 0

        self.anim_ticks_tower = 0
        self.anim_tower_state = 0

        self.shoot_a_bool = False
        # for minigun
        self.temperature_gun = 0
        self.temperature_gun_in_Shoot = 1
        self.max_temperature_gun = 10
        self.gun_overheat = False

        self.gun_overheat_delay = 0.2
        self.gun_overheat_time = time.perf_counter() + self.gun_overheat_delay

        self.gun_twist_delay = 0.5
        self.gun_twist_time = time.perf_counter() + self.gun_twist_delay

        # for laser
        self.gun_laser_count = 0
        self.gun_laser_max_count = 6 if (self.tank_settings[1] == 3) else 3

        self.reload_laser_delay = 0.2
        self.reload_laser_time = time.perf_counter() + self.reload_laser_delay

        # for shoot
        self.delay_shoot_a = tanks.towers_delay[self.tank_settings[1]]
        self.time_shoot_a = time.perf_counter() + self.delay_shoot_a

        # tanks
        self.obj_tanks = []

        self.death_tank_image = image_label('tanks/body/no_team/' + tanks.bases[self.tank_settings[0]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True)

        self.obj_tanks.append(PIL_to_pyglet(get_pil_black_mask(Image.open('assets/img/tanks/body/no_team/' + tanks.bases[self.tank_settings[0]] + '.png').convert("RGBA"), get_obj_display('world').shadow_alpha), self.scale_tank, True))
        self.obj_tanks.append([])
        self.obj_tanks[1].append(image_label('tanks/body/no_team/' + tanks.bases[self.tank_settings[0]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        self.obj_tanks[1].append(image_label('tanks/body/no_team/' + tanks.bases[self.tank_settings[0]] + '_1.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        if not self.enemy_bool:
            self.obj_tanks.append(image_label('tanks/body/' + tanks.teams[self.id] + '/' + tanks.bases[self.tank_settings[0]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        else:
            self.obj_tanks.append(image_label('tanks/body/no_team/' + tanks.bases[self.tank_settings[0]] + '_1.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        self.obj_tanks.append(PIL_to_pyglet(get_pil_black_mask(Image.open('assets/img/tanks/tower/' + tanks.towers[self.tank_settings[1]] + '.png').convert("RGBA"), get_obj_display('world').shadow_alpha), self.scale_tank, True))

        if self.tank_settings[1] in [0, 1]:
            self.obj_tanks.append([image_label('tanks/tower/' + tanks.towers[self.tank_settings[1]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True)])

        elif self.tank_settings[1] in [2]:
            self.obj_tanks.append([])
            self.obj_tanks[4].append(image_label('tanks/tower/' + tanks.towers[self.tank_settings[1]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
            self.obj_tanks[4].append(image_label('tanks/tower/' + tanks.towers[self.tank_settings[1]] + '_1.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
            self.obj_tanks.append(image_label('tanks/tower/mgun_heat.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))

        elif self.tank_settings[1] in [3, 4]:
            self.obj_tanks.append([])
            self.obj_tanks[4].append(image_label('tanks/tower/' + tanks.towers[self.tank_settings[1]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
            self.obj_tanks.append([])
            for i in range(self.gun_laser_max_count):
                self.obj_tanks[5].append(PIL_to_pyglet(get_pil_color_mask(Image.open('assets/img/tanks/tower/' + tanks.towers[self.tank_settings[1]] + '/' + str(i) + '.png').convert("RGBA"), tanks.towers_laser_color[id]), self.scale_tank, True))

        self.poligon_body = collision.Poly(v(100, 100),
        [
            v(-self.obj_tanks[0].width/2 + self.obj_tanks[0].width/50, -self.obj_tanks[0].height/2 + self.obj_tanks[0].height/50),
            v(self.obj_tanks[0].width/2 - self.obj_tanks[0].width/50, -self.obj_tanks[0].height/2 + self.obj_tanks[0].height/50),
            v(self.obj_tanks[0].width/2 - self.obj_tanks[0].width/50, self.obj_tanks[0].height/2 - self.obj_tanks[0].height/50),
            v(-self.obj_tanks[0].width/2 + self.obj_tanks[0].width/50, self.obj_tanks[0].height/2 - self.obj_tanks[0].height/50)
        ])

        self.spawn_collision = collision.Poly(v(100, 100),
        [
            v(-self.obj_tanks[0].width/2 + self.obj_tanks[0].width/50, -self.obj_tanks[0].height/2 + self.obj_tanks[0].height/50),
            v(self.obj_tanks[0].width/2 - self.obj_tanks[0].width/50, -self.obj_tanks[0].height/2 + self.obj_tanks[0].height/50),
            v(self.obj_tanks[0].width/2 - self.obj_tanks[0].width/50, self.obj_tanks[0].height/2 - self.obj_tanks[0].height/50),
            v(-self.obj_tanks[0].width/2 + self.obj_tanks[0].width/50, self.obj_tanks[0].height/2 - self.obj_tanks[0].height/50)
        ])

        self.traces_list = []
        self.traces_delay = 0.5
        self.trace_image = image_label('tanks/traces/' + tanks.bases[self.tank_settings[0]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True, rotation=0, alpha=10)

        self.offs = {
            -90: [-self.obj_tanks[0].width/2, 0], # -90
            0: [0, self.obj_tanks[0].height/2], # 0
            90: [self.obj_tanks[0].width/2, 0], # 90
            180: [0, -self.obj_tanks[0].height/2]  # 180
        }

        self.go_spawn()

        self.spawn_collision.pos.x = self.pos[0]
        self.spawn_collision.pos.y = self.pos[1]

        self.team_color_label = label(self.pos[0] - self.obj_tanks[0].width/2, self.pos[1] - self.obj_tanks[0].height/2, self.obj_tanks[0].width, self.obj_tanks[0].height, (tanks.team_colors[self.id]) if (not self.enemy_bool) else tanks.team_colors[4], alpha = 128)
        print('PLAYER ' + str(id) + ' SPAWN: ', self.pos)

    def add_trace(self, x, y, rotation):
        self.traces_list.append([x, y, rotation, time.perf_counter() + self.traces_delay])
        if len(self.traces_list) > get_obj_display('graphics_settings').max_traces:
            self.traces_list.pop(0)

    def anim_tick(self):
        self.anim_ticks += 1
        if self.anim_ticks >= 5:
            if len(self.obj_tanks[1]) > self.anim_body_state + 1:
                self.anim_body_state += 1
            else:
                self.anim_body_state = 0
            self.anim_ticks = 0

    def anim_tick_tower(self):
        if len(self.obj_tanks[4]) > self.anim_tower_state + 1:
            self.anim_tower_state += 1
        else:
            self.anim_tower_state = 0

    def anim_protection_tick(self):
        self.protection_ticks += 1
        if self.protection_ticks >= 5:
            if len(self.protection_images) > self.protection_image_num + 1:
                self.protection_image_num += 1
            else:
                self.protection_image_num = 0
            self.protection_ticks = 0

    def shoot(self, move_bool, type='bullet'):
        if type == 'bullet':
            self.sound.play('shoot.wav')
            get_obj_display('bullets').spawn(
                self.id, self.pos[0], self.pos[1], self.rotation,
                tanks.towers_speed[self.tank_settings[1]],
                ((tanks.towers_scatter[self.tank_settings[1]] + 1) * 2 if move_bool else (tanks.towers_scatter[self.tank_settings[1]])) if get_obj_display('game_settings').scatter_bool else 0,
                type=type
            )
            get_obj_display('smoke').add_smoke(self.pos[0] + self.offs[self.rotation][0], self.pos[1] + self.offs[self.rotation][1], 9)

        elif type == 'laser':
            self.sound.play('laser.wav')
            get_obj_display('bullets').spawn(
                self.id, self.pos[0], self.pos[1], self.rotation,
                tanks.towers_speed[self.tank_settings[1]],
                ((tanks.towers_scatter[self.tank_settings[1]] + 1) * 2 if move_bool else (tanks.towers_scatter[self.tank_settings[1]])) if get_obj_display('game_settings').scatter_bool else 0,
                type=type
            )

    def update(self):
        if self.use and not get_obj_display('game_settings').pause and not get_obj_display('game_settings').end_game:
            #self.old_perf_counter = time.perf_counter()
            # респавн при смерти
            if self.health <= 0 and not self.death_bool:
                get_obj_display('smoke').add_smoke(self.pos[0], self.pos[1])
                self.health = self.default_health
                self.death_time = time.perf_counter() + self.death_delay
                self.death_bool = True
                get_obj_display('world').shaking(delay=0.2, power=settings.height/108)
                self.sound.play('death.wav')
                self.death += 1

            if self.death_bool and self.death_time <= time.perf_counter():
                self.death_bool = False
                if not self.traning:
                    self.protection_time = time.perf_counter() + self.protection_delay
                    self.protection = True

                self.gun_laser_count = 0
                self.temperature_gun = 0
                self.gun_overheat = False
                self.go_spawn()

            # подстройка скорости игрока под FPS
            speed_tick = (self.check_fps / pyglet.clock.get_fps() if pyglet.clock.get_fps() <= self.norm_fps else 1) * self.speed_tick

            if not self.death_bool:

                # логика бота
                if self.bot:

                    #for player in get_obj_display('players').tanks:
                    #    if self.id != player.id:
                    #        if self.pos[0] <= player.pos[0]

                    if (self.wall_collision_bool or (self.time_random_rotation <= time.perf_counter())):
                        self.bot_rotation = [-90, 0, 90, 180][random.randint(0, 3)]
                        self.time_random_rotation = time.perf_counter() + random.randrange(1, 4)

                # передвижение
                if not game_settings.multiplayer or self.id == game_settings.multiplayer_id:
                    keys = (KEY_BINDS['main'] if game_settings.multiplayer else KEY_BINDS['P' + str(self.id + 1)]) if (not self.enemy_bool) else KEY_BINDS['P' + str(1)]
                    move_bool = False # для анимации
                    if (eval('keyboard[key.' + keys['left'] + ']') and not self.bot and not self.enemy_bool) or (self.bot and self.bot_rotation == -90):
                        self.wall_collision_bool = self.set_pos_body(-speed_tick, 0, self.bot)
                        self.rotation = -90
                        move_bool = True
                    elif (eval('keyboard[key.' + keys['right'] + ']') and not self.bot and not self.enemy_bool) or (self.bot and self.bot_rotation == 90):
                        self.wall_collision_bool = self.set_pos_body(speed_tick, 0, self.bot)
                        self.rotation = 90
                        move_bool = True
                    elif (eval('keyboard[key.' + keys['up'] + ']') and not self.bot and not self.enemy_bool) or (self.bot and self.bot_rotation == 0):
                        self.wall_collision_bool = self.set_pos_body(0, speed_tick, self.bot)
                        self.rotation = 0
                        move_bool = True
                    elif (eval('keyboard[key.' + keys['down'] + ']') and not self.bot and not self.enemy_bool) or (self.bot and self.bot_rotation == 180):
                        self.wall_collision_bool = self.set_pos_body(0, -speed_tick, self.bot)
                        self.rotation = 180
                        move_bool = True

                    #if move_bool:
                    #    if self.speed_tick < self.def_speed[0]/10:
                    #        self.speed_tick += self.def_speed[0]/10

                    #else:
                    #    self.speed_tick = 0

                    if not get_obj_display('game_settings').run:
                        self.go_spawn()
                        move_bool = False

                    if move_bool or self.tank_settings[0] == 1:
                        self.anim_tick()
                        if get_obj_display('graphics_settings').draw_traces:
                            self.add_trace(self.pos[0], self.pos[1], self.rotation)

                    # стрельба
                    if ( (eval('keyboard[key.' + keys['shoot_a'] + ']') and not self.bot and not self.enemy_bool) or (self.bot and self.bot_shoot_a) ) and get_obj_display('game_settings').run:
                        self.shoot_a_bool = True
                        if self.time_shoot_a <= time.perf_counter():
                            # Обычные пушки
                            if self.tank_settings[1] in [0, 1]:
                                self.shoot(move_bool)

                            # пулемёт
                            elif self.tank_settings[1] in [2]:
                                if self.gun_twist_time <= time.perf_counter():
                                    if (self.temperature_gun < self.max_temperature_gun) and not self.gun_overheat:
                                        self.temperature_gun += self.temperature_gun_in_Shoot
                                        if self.temperature_gun >= self.max_temperature_gun:
                                            self.gun_overheat = True
                                        self.shoot(move_bool)

                                self.anim_tick_tower()

                            # лазер
                            elif self.tank_settings[1] in [3, 4]:
                                if self.gun_laser_count < self.gun_laser_max_count:
                                    self.gun_laser_count += 1

                                if (self.bot and self.bot_shoot_a):
                                    if self.gun_laser_count >= self.gun_laser_max_count:
                                        self.shoot(move_bool, type='laser')
                                        self.gun_laser_count = 0

                            self.time_shoot_a = time.perf_counter() + self.delay_shoot_a
                    else:
                        if self.tank_settings[1] in [3, 4]:
                            if self.gun_laser_count >= self.gun_laser_max_count:
                                self.shoot(move_bool, type='laser')
                            self.gun_laser_count = 0

                        if self.tank_settings[1] in [2]:
                            self.gun_twist_time = time.perf_counter() + self.gun_twist_delay

                        self.shoot_a_bool = False

                    if self.tank_settings[1] in [2]:
                        if (self.temperature_gun > 0) and (self.gun_overheat_time <= time.perf_counter()):
                            self.temperature_gun -= self.temperature_gun_in_Shoot
                            if self.temperature_gun <= self.max_temperature_gun / 4:
                                self.gun_overheat = False

                            self.gun_overheat_time = time.perf_counter() + self.gun_overheat_delay

                            if self.gun_overheat:
                                get_obj_display('smoke').add_smoke(self.pos[0] + self.offs[self.rotation][0], self.pos[1] + self.offs[self.rotation][1], 9)

                        self.obj_tanks[5].alpha = (200 / self.max_temperature_gun) * self.temperature_gun
                        self.obj_tanks[5].update_image(True)

            self.poligon_body.pos.x = self.pos[0]
            self.poligon_body.pos.y = self.pos[1]

            # перемещение стпрайтов и полигонов по карте
            if self.death_bool:
                self.death_tank_image.x = self.pos[0] + get_obj_display('world').map_offs[1]
                self.death_tank_image.y = self.pos[1] + get_obj_display('world').map_offs[0]
                self.death_tank_image.update_rotation(self.rotation)
                self.death_tank_image.update_image(True)

            if self.protection or self.armor_bool:
                if self.protection_time <= time.perf_counter() and not self.armor_bool:
                    self.protection = False
                else:
                    self.anim_protection_tick()
                    if self.armor_bool:
                        self.protection_up_images[self.protection_image_num].x = self.pos[0] + get_obj_display('world').map_offs[0]
                        self.protection_up_images[self.protection_image_num].y = self.pos[1] + get_obj_display('world').map_offs[1]
                        self.protection_up_images[self.protection_image_num].update_image(True)
                    else:
                        self.protection_images[self.protection_image_num].x = self.pos[0] + get_obj_display('world').map_offs[0]
                        self.protection_images[self.protection_image_num].y = self.pos[1] + get_obj_display('world').map_offs[1]
                        self.protection_images[self.protection_image_num].update_image(True)

            for i in range(len(self.obj_tanks)):

                if i == 1:
                    self.obj_tanks[i][self.anim_body_state].update_rotation(self.rotation)

                    self.obj_tanks[i][self.anim_body_state].x = self.pos[0] + get_obj_display('world').map_offs[0]
                    self.obj_tanks[i][self.anim_body_state].y = self.pos[1] + get_obj_display('world').map_offs[1]
                    self.obj_tanks[i][self.anim_body_state].update_image(True)

                elif i == 4:
                    self.obj_tanks[i][self.anim_tower_state].x = self.pos[0] + get_obj_display('world').map_offs[0]
                    self.obj_tanks[i][self.anim_tower_state].y = self.pos[1] + get_obj_display('world').map_offs[1]
                    self.obj_tanks[i][self.anim_tower_state].update_image(True)
                    self.obj_tanks[i][self.anim_tower_state].update_rotation(self.rotation)

                elif i == 5 and self.tank_settings[1] in [3, 4]:
                    if self.gun_laser_count > 0:
                        self.obj_tanks[i][self.gun_laser_count - 1].x = self.pos[0] + get_obj_display('world').map_offs[0]
                        self.obj_tanks[i][self.gun_laser_count - 1].y = self.pos[1] + get_obj_display('world').map_offs[1]
                        self.obj_tanks[i][self.gun_laser_count - 1].rotation = self.rotation

                else:
                    try:
                        self.obj_tanks[i].update_rotation(self.rotation)
                    except:
                        self.obj_tanks[i].rotation = self.rotation

                    if i in [0, 3]:
                        self.obj_tanks[i].x = self.pos[0] + get_obj_display('world').offs_shadows[0] / 3 + get_obj_display('world').map_offs[0]#6
                        self.obj_tanks[i].y = self.pos[1] - get_obj_display('world').offs_shadows[0] / 3 + get_obj_display('world').map_offs[1]#6

                    else:
                        self.obj_tanks[i].x = self.pos[0] + get_obj_display('world').map_offs[0] + get_obj_display('world').map_offs[0]
                        self.obj_tanks[i].y = self.pos[1] + get_obj_display('world').map_offs[1] + get_obj_display('world').map_offs[1]
                        self.obj_tanks[i].update_image(True)

            # удаление следов
            for i in range(len(self.traces_list)-1, -1, -1):
                if self.traces_list[i][3] <= time.perf_counter():
                    self.traces_list.pop(i)

    def set_pos_body(self, x_, y_, send_return_bool = False):
        self.detect = False
        pos_ = [self.pos[0], self.pos[1]]
        self.pos = [self.pos[0] + x_, self.pos[1] + y_]
        pos = [self.pos[0] + ((settings.width - get_obj_display('world').image_wall.width) / 2), self.pos[1] - ((settings.height - get_obj_display('world').image_wall.height) / 2)]
        pos = [int(math.sqrt(pos[0] ** 2)//get_obj_display('world').size_poligon), int(math.sqrt(pos[1] ** 2)//get_obj_display('world').size_poligon)]
        for y in range(pos[1] - get_obj_display('world').range, pos[1] + get_obj_display('world').range, 1):
            for x in range(pos[0] - get_obj_display('world').range, pos[0] + get_obj_display('world').range, 1):
                try:
                    poligon = get_obj_display('world').get_wall_poligon(x, y) if (get_obj_display('world').get_wall_poligon(x, y) != 'none' or self.tank_settings[0] == 1) else get_obj_display('world').get_water_poligon(x, y)
                    if poligon != 'none':
                        self.poligon_body.pos.x = self.pos[0]
                        self.poligon_body.pos.y = self.pos[1]
                        if collision.collide(self.poligon_body, poligon):
                            self.detect = True
                            self.pos = pos_
                            break
                        else:
                            pass
                        t = 1.0
                        while True:
                            self.poligon_body.pos.x = self.pos[0]
                            self.poligon_body.pos.y = self.pos[1]
                            if collision.collide(self.poligon_body, poligon):
                                self.pos = [pos_[0] - (x_ * t), pos_[1] - (y_ * t)]
                                self.detect = True
                                t += 0.05

                            else:
                                break
                except:
                    pass

        if game_settings.collide_players:
            for i in range(len(get_obj_display('players').tanks)):
                self.poligon_body.pos.x = self.pos[0]
                self.poligon_body.pos.y = self.pos[1]

                if (self.id != i
                        and ((collision.collide(self.poligon_body, get_obj_display('players').tanks[i].poligon_body)
                        or collision.collide(self.poligon_body, get_obj_display('players').tanks[i].spawn_collision) ) and get_obj_display('players').tanks[i].use)
                    ):
                    self.pos = [pos_[0], pos_[1]]
                    self.poligon_body.pos.x = self.pos[0]
                    self.poligon_body.pos.y = self.pos[1]
                    self.detect = True

        if send_return_bool:
            return self.detect

    def draw(self):
        if self.use:
            for trace in self.traces_list:
                self.trace_image.sprite.x = trace[0] + get_obj_display('world').map_offs[0]
                self.trace_image.sprite.y = trace[1] + get_obj_display('world').map_offs[1]
                self.trace_image.sprite.rotation = trace[2]
                drawp(self.trace_image)

            if not self.death_bool:
                for i in range(len(self.obj_tanks)):
                    if i == 1:
                        drawp(self.obj_tanks[i][self.anim_body_state])
                    elif i == 4:
                        drawp(self.obj_tanks[i][self.anim_tower_state])
                    elif i == 5 and self.tank_settings[1] in [3, 4]:
                        if self.gun_laser_count > 0:
                            drawp(self.obj_tanks[i][self.gun_laser_count - 1])
                    else:
                        drawp(self.obj_tanks[i])


            if self.death_bool:
                drawp(self.obj_tanks[0])
                drawp(self.death_tank_image)

            if self.protection or self.armor_bool:
                if self.armor_bool:
                    drawp(self.protection_up_images[self.protection_image_num])
                else:
                    drawp(self.protection_images[self.protection_image_num])

            if objects_other[0].draw_poligons:
                points = (
                    int(self.poligon_body.points[0][0]), int(self.poligon_body.points[0][1]),
                    int(self.poligon_body.points[1][0]), int(self.poligon_body.points[1][1]),
                    int(self.poligon_body.points[2][0]), int(self.poligon_body.points[2][1]),
                    int(self.poligon_body.points[3][0]), int(self.poligon_body.points[3][1])
                )
                pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
                    ('v2i', points)
                )

                pos = [self.pos[0] + ((settings.width - get_obj_display('world').image_wall.width) / 2), self.pos[1] - ((settings.height - get_obj_display('world').image_wall.height) / 2)]
                pos = [int(math.sqrt(pos[0] ** 2)//get_obj_display('world').size_poligon), int(math.sqrt(pos[1] ** 2)//get_obj_display('world').size_poligon)]
                for y in range(pos[1] - get_obj_display('world').range, pos[1] + get_obj_display('world').range, 1):
                    for x in range(pos[0] - get_obj_display('world').range, pos[0] + get_obj_display('world').range, 1):
                        try:
                            poligon = get_obj_display('world').get_wall_poligon(x, y)
                            if poligon != 'none':
                                points = []
                                for p in poligon.points:
                                    points.append(int(p[0]))
                                    points.append(int(p[1]))
                                pyglet.graphics.draw(len(poligon.points), pyglet.gl.GL_LINE_LOOP,
                                    ('v2i', points))
                        except:
                            pass
