class bullets():
    def __init__(self):

        self.check_fps = 60
        self.norm_fps = 75

        self.bullets = []
        self.bullet = image_label('tanks/bullets/bullet.png', settings.width//2, settings.height//2, scale=get_obj_display('world').scale/2, pixel=False, center=True)

        self.bullet_poly = collision.Poly(v(100, 100),
        [
            v(-self.bullet.sprite.width/2, -self.bullet.sprite.height/2),
            v(self.bullet.sprite.width/2, -self.bullet.sprite.height/2),
            v(self.bullet.sprite.width/2, self.bullet.sprite.height/2),
            v(-self.bullet.sprite.width/2, self.bullet.sprite.height/2)
        ])

        #self.players_polygons = ['', '', '', '']

    def spawn(self, id, x, y, rot, speed):
        self.bullets.append([id, x, y, rot, speed])

    def update(self):
        i = -1
        for bullet in self.bullets:
            speed_tick = (self.check_fps / pyglet.clock.get_fps() if pyglet.clock.get_fps() <= self.norm_fps else 1) * bullet[4]
            i += 1
            if bullet[3] == -90:
                bullet[1] -= speed_tick

            elif bullet[3] == 90:
                bullet[1] += speed_tick

            elif bullet[3] == 0:
                bullet[2] += speed_tick

            elif bullet[3] == 180:
                bullet[2] -= speed_tick

            #print(bullet[1], bullet[2])
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
                        dead = True
                        if not get_obj_display('players').tanks[j].death:
                            get_obj_display('players').tanks[j].health -= get_obj_display('players').tanks[bullet[0]].demage_a
                        self.bullets.pop(i)

                if not dead:
                    pos = [bullet[1] + ((settings.width - get_obj_display('world').image_wall.width) / 2), bullet[2] - ((settings.height - get_obj_display('world').image_wall.height) / 2)]
                    pos = [int(math.sqrt(pos[0] ** 2)//get_obj_display('world').size_poligon), int(math.sqrt(pos[1] ** 2)//get_obj_display('world').size_poligon)]

                    block = get_obj_display('world').get_wall_poligon(pos[0], pos[1])
                    if block != 'none':
                        if collision.collide(self.bullet_poly, block):
                            self.bullets.pop(i)

                            # попытка сделать разрушемость
                            #get_obj_display('world').map_wall[get_obj_display('world').get_block_num(pos[0], get_obj_display('world').world_size[1] - pos[1])] = 'none'
                            #get_obj_display('world').clear_images_wall()
                            #get_obj_display('world').set_wall()
                            #get_obj_display('world').update_images_wall()




    def draw(self):

        for bullet in self.bullets:
            self.bullet.sprite.x = bullet[1]
            self.bullet.sprite.y = bullet[2]
            self.bullet.sprite.rotation = bullet[3]
            drawp(self.bullet)

            if objects_other[0].draw_poligons:
                self.bullet_poly.pos.x = bullet[1]
                self.bullet_poly.pos.y = bullet[2]
                self.bullet_poly.angle = math.radians(bullet[3] - 180)
                draw_poly(self.bullet_poly)
