class bullets():

    def get_speed_by_deg_sp(self, deg, speed):
        #deg += 90
        if deg < 0:
            deg = 180 + (180 + deg)
        if deg >= 360:
            deg = 0
        a = speed/math.sin(math.radians(90))
        x = a * math.sin(math.radians(deg))
        y = a * math.sin(math.radians(180 - 90 - deg))
        return x, y

    def __init__(self):

        self.check_fps = 60
        self.norm_fps = 75

        self.bullets = []
        self.bullet = [
            image_label('tanks/bullets/bullet.png', settings.width//2, settings.height//2, scale=get_obj_display('world').scale/2, pixel=False, center=True),
            [
                image_label('tanks/bullets/laser/laser_red.png', settings.width//2, settings.height//2, scale=get_obj_display('world').scale/2, pixel=False, center=True),
                image_label('tanks/bullets/laser/laser_blue.png', settings.width//2, settings.height//2, scale=get_obj_display('world').scale/2, pixel=False, center=True),
                image_label('tanks/bullets/laser/laser_green.png', settings.width//2, settings.height//2, scale=get_obj_display('world').scale/2, pixel=False, center=True),
                image_label('tanks/bullets/laser/laser_yellow.png', settings.width//2, settings.height//2, scale=get_obj_display('world').scale/2, pixel=False, center=True)
            ]
        ]


        self.bullet_poly = collision.Poly(v(100, 100),
        [
            v(-self.bullet[0].sprite.width/2, -self.bullet[0].sprite.height/2),
            v(self.bullet[0].sprite.width/2, -self.bullet[0].sprite.height/2),
            v(self.bullet[0].sprite.width/2, self.bullet[0].sprite.height/2),
            v(-self.bullet[0].sprite.width/2, self.bullet[0].sprite.height/2)
        ])

    def spawn(self, id, x, y, rot, speed, scatter=0, type='bullet'):
        types = {
            'bullet': 0,
            'laser': 1
        }
        self.bullets.append([id, x, y, rot + ((random.randrange(-scatter, scatter)) if scatter > 0 else 0), speed, types[type]])

    def update(self):
        if not get_obj_display('game_settings').pause:
            i = -1
            for bullet in self.bullets:
                speed_tick = (self.check_fps / pyglet.clock.get_fps() if pyglet.clock.get_fps() <= self.norm_fps else 1) * bullet[4]
                i += 1

                if get_obj_display('game_settings').wind_bool and bullet[5] != 1:

                    wind_deg = get_obj_display('game_settings').wind_deg
                    wind_power = speed_tick / get_obj_display('game_settings').wind_power
                    wind = bullet[3] + wind_deg
                    if wind > 180:
                        wind = wind - 360
                    if wind < -180:
                        wind = wind + 360

                    if wind < 0:
                        bullet[3] -= wind_power
                    elif wind > 0:
                        bullet[3] += wind_power

                x, y = self.get_speed_by_deg_sp(bullet[3], speed_tick)
                bullet[1] += x
                bullet[2] += y

                if ((bullet[1] > settings.width)
                or (bullet[1] < 0)
                or (bullet[2] > settings.height)
                or (bullet[2] < 0)):
                    self.bullets.pop(i)

                else:
                    self.bullet_poly.pos.x = bullet[1]
                    self.bullet_poly.pos.y = bullet[2]
                    self.bullet_poly.angle = math.radians(bullet[3])

                    dead = False
                    for j in range(len(get_obj_display('players').tanks)):
                        if bullet[0] != j and collision.collide(self.bullet_poly, get_obj_display('players').tanks[j].poligon_body):
                            if get_obj_display('players').tanks[j].use:
                                dead = True
                                if not get_obj_display('players').tanks[j].death_bool and not get_obj_display('players').tanks[j].protection:
                                    get_obj_display('players').tanks[j].health -= get_obj_display('players').tanks[bullet[0]].demage_a
                                    if get_obj_display('players').tanks[j].health <= 0:
                                        get_obj_display('players').tanks[bullet[0]].kills += 1
                                    #get_obj_display('world').shaking(delay=0.2, power=settings.height/1000)
                                self.bullets.pop(i)
                                #get_obj_display('smoke').add_smoke(bullet[1], bullet[2], 9)

                    if not dead:
                        pos = [bullet[1] + ((settings.width - get_obj_display('world').image_wall.width) / 2), bullet[2] - ((settings.height - get_obj_display('world').image_wall.height) / 2)]
                        pos = [int(math.sqrt(pos[0] ** 2)//get_obj_display('world').size_poligon), int(math.sqrt(pos[1] ** 2)//get_obj_display('world').size_poligon)]

                        block = get_obj_display('world').get_wall_poligon(pos[0], pos[1])
                        if block != 'none':
                            if collision.collide(self.bullet_poly, block):
                                self.bullets.pop(i)
                                get_obj_display('smoke').add_smoke(bullet[1], bullet[2], 9)
                                # попытка сделать разрушемость
                                #get_obj_display('world').map_wall[get_obj_display('world').get_block_num(pos[0], get_obj_display('world').world_size[1] - pos[1])] = 'none'
                                #get_obj_display('world').clear_images_wall()
                                #get_obj_display('world').set_wall()
                                #get_obj_display('world').update_images_wall()

    def draw(self):
        for bullet in self.bullets:
            if bullet[5] == 0:
                image_bullet = self.bullet[0]
            elif bullet[5] == 1:
                image_bullet = self.bullet[1][bullet[0]]

            image_bullet.sprite.x = bullet[1] + get_obj_display('world').map_offs[0]
            image_bullet.sprite.y = bullet[2] + get_obj_display('world').map_offs[1]
            image_bullet.sprite.rotation = bullet[3]
            drawp(image_bullet)

            if objects_other[0].draw_poligons:
                self.bullet_poly.pos.x = bullet[1]
                self.bullet_poly.pos.y = bullet[2]
                self.bullet_poly.angle = math.radians(bullet[3] - 180)
                draw_poly(self.bullet_poly)
