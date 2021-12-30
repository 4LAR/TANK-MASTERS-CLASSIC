class players():
    def __init__(self, bot, tanks, tank_settings):
        self.tanks = []

        for i in range(4):
            self.tanks.append(player(i, bot[i], tank_settings[i], tanks[i]))

    def update(self):
        for tank in self.tanks:
            tank.update()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            menu()

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
                    #get_obj_display('world').spawn[self.id][0] * get_obj_display('world').size * get_obj_display('world').scale,
                    #settings.height - get_obj_display('world').image_wall.height - (get_obj_display('world').spawn[self.id][1] * get_obj_display('world').size * get_obj_display('world').scale)
                ]
            except:
                self.pos = [settings.width//2, settings.height//2]
        else:
            self.pos = [-settings.width, -settings.height]

    def __init__(self, id, bot=False, tank_settings=[0, 0], use=True):

        self.tank_settings = tank_settings
        self.use = use

        self.sound = Sound()

        self.id = id
        self.bot = bot

        self.check_fps = 60
        self.norm_fps = 75

        self.pos = [0, 0]
        self.go_spawn()

        print('PLAYER ' + str(id) + ' SPAWN: ', self.pos)

        self.scale_tank = get_obj_display('world').scale / 1.2

        self.default_health = 100
        self.health = 100

        self.protection = True
        self.protection_delay = 2
        self.protection_time = time.perf_counter() + self.protection_delay

        self.protection_ticks = 0
        self.protection_image_num = 0
        self.protection_images = []
        for i in range(4):
            self.protection_images.append(
                image_label(
                    'tanks/protection/protection_' + str(i + 1) + '.png',
                    settings.width//2, settings.height//2,
                    scale=self.scale_tank * 1.2, pixel=False,
                    center=True
                )
            )

        self.death = False
        self.death_delay = 2
        self.death_time = time.perf_counter() + self.death_delay

        self.demage_a = tanks.towers_damage[self.tank_settings[1]]

        self.def_speed = [tanks.bases_speed[self.tank_settings[0]]]
        self.speed_tick = self.def_speed[0]/10
        self.speed = 0
        self.rotation = 0

        self.bot_rotation = 0
        self.time_random_rotation = 0
        self.bot_shoot_a = True

        self.wall_collision_bool = False

        self.anim_ticks = 0
        self.anim_body_state = 0

        self.delay_shoot_a = tanks.towers_delay[self.tank_settings[1]]
        self.time_shoot_a = time.perf_counter() + self.delay_shoot_a

        self.obj_tanks = []

        self.death_tank_image = image_label('tanks/body/no_team/' + tanks.bases[self.tank_settings[0]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True)

        self.obj_tanks.append(PIL_to_pyglet(get_pil_black_mask(Image.open('img/tanks/body/no_team/' + tanks.bases[self.tank_settings[0]] + '.png').convert("RGBA"), get_obj_display('world').shadow_alpha), self.scale_tank, True))
        self.obj_tanks.append([])
        self.obj_tanks[1].append(image_label('tanks/body/no_team/' + tanks.bases[self.tank_settings[0]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        self.obj_tanks[1].append(image_label('tanks/body/no_team/' + tanks.bases[self.tank_settings[0]] + '_1.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        self.obj_tanks.append(image_label('tanks/body/' + tanks.teams[self.id] + '/' + tanks.bases[self.tank_settings[0]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        self.obj_tanks.append(PIL_to_pyglet(get_pil_black_mask(Image.open('img/tanks/tower/' + tanks.towers[self.tank_settings[1]] + '.png').convert("RGBA"), get_obj_display('world').shadow_alpha), self.scale_tank, True))
        self.obj_tanks.append(image_label('tanks/tower/' + tanks.towers[self.tank_settings[1]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))

        self.poligon_body = collision.Poly(v(100, 100),
        [
            v(-self.obj_tanks[0].width/2 + self.obj_tanks[0].width/50, -self.obj_tanks[0].height/2 + self.obj_tanks[0].height/50),
            v(self.obj_tanks[0].width/2 - self.obj_tanks[0].width/50, -self.obj_tanks[0].height/2 + self.obj_tanks[0].height/50),
            v(self.obj_tanks[0].width/2 - self.obj_tanks[0].width/50, self.obj_tanks[0].height/2 - self.obj_tanks[0].height/50),
            v(-self.obj_tanks[0].width/2 + self.obj_tanks[0].width/50, self.obj_tanks[0].height/2 - self.obj_tanks[0].height/50)
        ])

        self.traces_list = []
        self.traces_delay = 0.5
        self.trace_image = image_label('tanks/traces/' + tanks.bases[self.tank_settings[0]] + '.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True, rotation=0, alpha=10)

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

    def anim_protection_tick(self):
        self.protection_ticks += 1
        if self.protection_ticks >= 5:
            if len(self.protection_images) > self.protection_image_num + 1:
                self.protection_image_num += 1
            else:
                self.protection_image_num = 0
            self.protection_ticks = 0

    def update(self):
        if self.use:
            # респавн при смерти
            if self.health <= 0 and not self.death:
                self.health = self.default_health
                self.death_time = time.perf_counter() + self.death_delay
                self.death = True
                get_obj_display('world').shaking(delay=0.2, power=settings.height/150)
                self.sound.play('death.wav')

            if self.death and self.death_time <= time.perf_counter():
                self.death = False
                self.protection_time = time.perf_counter() + self.protection_delay
                self.protection = True
                self.go_spawn()

            # подстройка скорости игрока под FPS
            speed_tick = (self.check_fps / pyglet.clock.get_fps() if pyglet.clock.get_fps() <= self.norm_fps else 1) * self.speed_tick

            if not self.death:

                # логика бота
                if self.bot:

                    #for player in get_obj_display('players').tanks:
                    #    if self.id != player.id:
                    #        if self.pos[0] <= player.pos[0]

                    if (self.wall_collision_bool or (self.time_random_rotation <= time.perf_counter())):
                        self.bot_rotation = [-90, 0, 90, 180][random.randint(0, 3)]
                        self.time_random_rotation = time.perf_counter() + random.randrange(1, 4)

                # передвижение
                move_bool = False # для анимации
                if (eval('keyboard[key.' + KEY_BINDS['P' + str(self.id + 1)]['left'] + ']') and not self.bot) or (self.bot and self.bot_rotation == -90):
                    self.wall_collision_bool = self.set_pos_body(-speed_tick, 0, self.bot)
                    self.rotation = -90
                    move_bool = True
                elif (eval('keyboard[key.' + KEY_BINDS['P' + str(self.id + 1)]['right'] + ']') and not self.bot) or (self.bot and self.bot_rotation == 90):
                    self.wall_collision_bool = self.set_pos_body(speed_tick, 0, self.bot)
                    self.rotation = 90
                    move_bool = True
                elif (eval('keyboard[key.' + KEY_BINDS['P' + str(self.id + 1)]['up'] + ']') and not self.bot) or (self.bot and self.bot_rotation == 0):
                    self.wall_collision_bool = self.set_pos_body(0, speed_tick, self.bot)
                    self.rotation = 0
                    move_bool = True
                elif (eval('keyboard[key.' + KEY_BINDS['P' + str(self.id + 1)]['down'] + ']') and not self.bot) or (self.bot and self.bot_rotation == 180):
                    self.wall_collision_bool = self.set_pos_body(0, -speed_tick, self.bot)
                    self.rotation = 180
                    move_bool = True

                if move_bool or self.tank_settings[0] == 1:
                    self.anim_tick()
                    if get_obj_display('graphics_settings').draw_traces:
                        self.add_trace(self.pos[0], self.pos[1], self.rotation)

                self.poligon_body.pos.x = self.pos[0]
                self.poligon_body.pos.y = self.pos[1]

                # стрельба
                if (((eval('keyboard[key.' + KEY_BINDS['P' + str(self.id+1)]['shoot_a'] + ']') and not self.bot) or (self.bot and self.bot_shoot_a) ) and (self.time_shoot_a <= time.perf_counter())):
                    self.sound.play('shoot.wav')
                    get_obj_display('bullets').spawn(
                        self.id, self.pos[0], self.pos[1], self.rotation,
                        self.speed_tick * 10,
                        ((tanks.towers_scatter[self.tank_settings[1]] + 1) * 2 if move_bool else (tanks.towers_scatter[self.tank_settings[1]])) if get_obj_display('game_settings').scatter_bool else 0
                    )
                    self.time_shoot_a = time.perf_counter() + self.delay_shoot_a

            # перемещение стпрайтов и полигонов по карте
            if self.death:
                self.death_tank_image.x = self.pos[0] + get_obj_display('world').map_offs[1]
                self.death_tank_image.y = self.pos[1] + get_obj_display('world').map_offs[0]
                self.death_tank_image.update_rotation(self.rotation)
                self.death_tank_image.update_image(True)

            if self.protection:
                if self.protection_time <= time.perf_counter():
                    self.protection = False
                else:
                    self.anim_protection_tick()
                    self.protection_images[self.protection_image_num].x = self.pos[0] + get_obj_display('world').map_offs[0]
                    self.protection_images[self.protection_image_num].y = self.pos[1] + get_obj_display('world').map_offs[1]
                    self.protection_images[self.protection_image_num].update_image(True)

            for i in range(len(self.obj_tanks)):
                if i != 1:
                    try:
                        self.obj_tanks[i].update_rotation(self.rotation)
                    except:
                        self.obj_tanks[i].rotation = self.rotation
                    if i in [0, 3]:
                        self.obj_tanks[i].x = self.pos[0] + get_obj_display('world').offs_shadows[0] / 3 + get_obj_display('world').map_offs[0]#6
                        self.obj_tanks[i].y = self.pos[1] - get_obj_display('world').offs_shadows[0] / 3 + get_obj_display('world').map_offs[1]#6
                        #self.obj_tanks[i].update_image(True)
                    else:
                        self.obj_tanks[i].x = self.pos[0] + get_obj_display('world').map_offs[0]
                        self.obj_tanks[i].y = self.pos[1] + get_obj_display('world').map_offs[1]
                        self.obj_tanks[i].update_image(True)

                else:
                    self.obj_tanks[i][self.anim_body_state].update_rotation(self.rotation)

                    self.obj_tanks[i][self.anim_body_state].x = self.pos[0] + get_obj_display('world').map_offs[0]
                    self.obj_tanks[i][self.anim_body_state].y = self.pos[1] + get_obj_display('world').map_offs[1]
                    self.obj_tanks[i][self.anim_body_state].update_image(True)

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
                            if collision.collide(self.poligon_body, poligon):
                                self.pos = [pos_[0] - (x_ * t), pos_[1] - (y_ * t)]
                                self.detect = True
                                t += 0.05

                            else:
                                break
                except:
                    pass

        '''for i in range(len(get_obj_display('players').tanks)):
            t = 1.0
            while True:
                if self.id != i and collision.collide(self.poligon_body, get_obj_display('players').tanks[i].poligon_body):

                    self.pos = [pos_[0] - (x_ * t), pos_[1] - (y_ * t)]
                    self.poligon_body.pos.x = self.pos[0]
                    self.poligon_body.pos.y = self.pos[1]

                    t += 0.05
                else:
                    break
                self.detect = True'''

        if send_return_bool:
            return self.detect

    def draw(self):
        if self.use:
            for trace in self.traces_list:
                self.trace_image.sprite.x = trace[0] + get_obj_display('world').map_offs[0]
                self.trace_image.sprite.y = trace[1] + get_obj_display('world').map_offs[1]
                self.trace_image.sprite.rotation = trace[2]
                drawp(self.trace_image)

            if not self.death:
                for i in range(len(self.obj_tanks)):
                    if i != 1:
                        drawp(self.obj_tanks[i])
                    else:
                        drawp(self.obj_tanks[i][self.anim_body_state])

            if self.death:
                drawp(self.obj_tanks[0])
                drawp(self.death_tank_image)

            if self.protection:
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
