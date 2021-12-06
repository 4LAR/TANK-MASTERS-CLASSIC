class player():
    def __init__(self, id):
        self.id = id

        self.check_fps = 60
        self.norm_fps = 75

        try:
            self.pos = [
                get_obj_display('world').image_floor.x + (get_obj_display('world').spawn[self.id][0] * get_obj_display('world').size * get_obj_display('world').scale),
                get_obj_display('world').image_floor.y + ((get_obj_display('world').world_size[1] - get_obj_display('world').spawn[self.id][1]) * get_obj_display('world').size * get_obj_display('world').scale)
                #get_obj_display('world').spawn[self.id][0] * get_obj_display('world').size * get_obj_display('world').scale,
                #settings.height - get_obj_display('world').image_wall.height - (get_obj_display('world').spawn[self.id][1] * get_obj_display('world').size * get_obj_display('world').scale)
            ]
        except:
            self.pos = [settings.width//2, settings.height//2]

        print('PLAYER ' + str(id) + ' SPAWN: ', self.pos)

        self.scale_tank = get_obj_display('world').scale

        self.def_speed = [settings.height/60]
        self.speed_tick = self.def_speed[0]/10
        self.speed = 0
        self.rotation = 0

        self.anim_ticks = 0
        self.anim_body_state = 0

        self.delay_shoot_a = 1
        self.time_shoot_a = time.perf_counter() + self.delay_shoot_a

        self.obj_tanks = []

        self.obj_tanks.append(PIL_to_pyglet(get_pil_black_mask(Image.open('img/tanks/body/no_team/tank_base.png').convert("RGBA"), get_obj_display('world').shadow_alpha), self.scale_tank, True))
        self.obj_tanks.append([])
        self.obj_tanks[1].append(image_label('tanks/body/no_team/tank_base.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        self.obj_tanks[1].append(image_label('tanks/body/no_team/tank_base_1.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        self.obj_tanks.append(PIL_to_pyglet(get_pil_black_mask(Image.open('img/tanks/tower/gun.png').convert("RGBA"), get_obj_display('world').shadow_alpha), self.scale_tank, True))
        self.obj_tanks.append(image_label('tanks/tower/gun.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))

        self.poligon_body = collision.Poly(v(100, 100),
        [
            v(-self.obj_tanks[0].width/2 + self.obj_tanks[0].width/50, -self.obj_tanks[0].height/2 + self.obj_tanks[0].height/50),
            v(self.obj_tanks[0].width/2 - self.obj_tanks[0].width/50, -self.obj_tanks[0].height/2 + self.obj_tanks[0].height/50),
            v(self.obj_tanks[0].width/2 - self.obj_tanks[0].width/50, self.obj_tanks[0].height/2 - self.obj_tanks[0].height/50),
            v(-self.obj_tanks[0].width/2 + self.obj_tanks[0].width/50, self.obj_tanks[0].height/2 - self.obj_tanks[0].height/50)
        ])

    def anim_tick(self):
        self.anim_ticks += 1
        if self.anim_ticks >= 5:
            if len(self.obj_tanks[1]) > self.anim_body_state + 1:
                self.anim_body_state += 1
            else:
                self.anim_body_state = 0
            self.anim_ticks = 0


    def update(self):
        speed_tick = (self.check_fps/pyglet.clock.get_fps() if pyglet.clock.get_fps()<= self.norm_fps else 1) * self.speed_tick
        if eval('keyboard[key.' + KEY_BINDS['P' + str(self.id+1)]['left'] + ']'):
            #self.pos[0] -= self.speed_tick
            self.set_pos_body(-speed_tick, 0)
            self.rotation = -90
            self.anim_tick()
        elif eval('keyboard[key.' + KEY_BINDS['P' + str(self.id+1)]['right'] + ']'):
            #self.pos[0] += self.speed_tick
            self.set_pos_body(speed_tick, 0)
            self.rotation = 90
            self.anim_tick()
        elif eval('keyboard[key.' + KEY_BINDS['P' + str(self.id+1)]['up'] + ']'):
            #self.pos[1] += self.speed_tick
            self.set_pos_body(0, speed_tick)
            self.rotation = 0
            self.anim_tick()
        elif eval('keyboard[key.' + KEY_BINDS['P' + str(self.id+1)]['down'] + ']'):
            #self.pos[1] -= self.speed_tick
            self.set_pos_body(0, -speed_tick)
            self.rotation = 180
            self.anim_tick()

        self.poligon_body.pos.x = self.pos[0]
        self.poligon_body.pos.y = self.pos[1]


        if (eval('keyboard[key.' + KEY_BINDS['P' + str(self.id+1)]['shoot_a'] + ']') and (self.time_shoot_a <= time.perf_counter())):
            get_obj_display('bullets').spawn(self.id, self.pos[0], self.pos[1], self.rotation, self.speed_tick * 10)
            self.time_shoot_a = time.perf_counter() + self.delay_shoot_a

        for i in range(len(self.obj_tanks)):
            if i != 1:
                try:
                    self.obj_tanks[i].update_rotation(self.rotation)
                except:
                    self.obj_tanks[i].rotation = self.rotation
                if i in [0, 2]:
                    self.obj_tanks[i].x = self.pos[0] + get_obj_display('world').offs_shadows[0] / 3#6
                    self.obj_tanks[i].y = self.pos[1] - get_obj_display('world').offs_shadows[0] / 3#6
                    #self.obj_tanks[i].update_image(True)
                else:
                    self.obj_tanks[i].x = self.pos[0]
                    self.obj_tanks[i].y = self.pos[1]
                    self.obj_tanks[i].update_image(True)

            else:
                self.obj_tanks[i][self.anim_body_state].update_rotation(self.rotation)

                self.obj_tanks[i][self.anim_body_state].x = self.pos[0]
                self.obj_tanks[i][self.anim_body_state].y = self.pos[1]
                self.obj_tanks[i][self.anim_body_state].update_image(True)

    def set_pos_body(self, x_, y_):

        pos_ = [self.pos[0], self.pos[1]]
        self.pos = [self.pos[0] + x_, self.pos[1] + y_]
        pos = [self.pos[0] + ((settings.width - get_obj_display('world').image_wall.width) / 2), self.pos[1] - ((settings.height - get_obj_display('world').image_wall.height) / 2)]
        pos = [int(math.sqrt(pos[0] ** 2)//get_obj_display('world').size_poligon), int(math.sqrt(pos[1] ** 2)//get_obj_display('world').size_poligon)]
        for y in range(pos[1] - get_obj_display('world').range, pos[1] + get_obj_display('world').range, 1):
            for x in range(pos[0] - get_obj_display('world').range, pos[0] + get_obj_display('world').range, 1):
                try:
                    poligon = get_obj_display('world').get_wall_poligon(x, y)
                    if poligon != 'none':
                        self.poligon_body.pos.x = self.pos[0]
                        self.poligon_body.pos.y = self.pos[1]
                        if collision.collide(self.poligon_body, poligon):
                            #
                            self.pos = pos_
                            break
                        else:
                            pass
                        #t = 1.0
                        #while True:
                        #    #print('rr: ', send_return_bool)
                        #    poligon_body = self.poligon_body if self.tank else self.poligon_human


                        #    if collision.collide(poligon_body, poligon):
                        #        self.pos = [pos_[0] - (x_ * t), pos_[1] - (y_ * t)]
                        #        detect = True
                        #        t += 0.05
                        #
                        #    else:
                        #        break
                except:
                    pass

    def draw(self):
        for i in range(len(self.obj_tanks)):
            if i != 1:
                drawp(self.obj_tanks[i])
            else:
                drawp(self.obj_tanks[i][self.anim_body_state])

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
