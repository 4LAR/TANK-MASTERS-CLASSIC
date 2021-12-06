class bullets():
    def __init__(self):

        self.bullets = []
        self.bullet = image_label('tanks/bullets/bullet.png', settings.width//2, settings.height//2, scale=get_obj_display('world').scale/2, pixel=False, center=True)

        self.bullet_poly = collision.Poly(v(100, 100),
        [
            v(-self.bullet.sprite.width/2, -self.bullet.sprite.height/2),
            v(self.bullet.sprite.width/2, -self.bullet.sprite.height/2),
            v(self.bullet.sprite.width/2, self.bullet.sprite.height/2),
            v(-self.bullet.sprite.width/2, self.bullet.sprite.height/2)
        ])

    def spawn(self, id, x, y, rot, speed):
        self.bullets.append([id, x, y, rot, speed])

    def update(self):
        i = -1
        for bullet in self.bullets:
            i += 1
            if bullet[3] == -90:
                bullet[1] -= bullet[4]

            elif bullet[3] == 90:
                bullet[1] += bullet[4]

            elif bullet[3] == 0:
                bullet[2] += bullet[4]

            elif bullet[3] == 180:
                bullet[2] -= bullet[4]

            #print(bullet[1], bullet[2])
            if ((bullet[1] > settings.width)
            or (bullet[1] < 0)
            or (bullet[2] > settings.height)
            or (bullet[2] < 0)):
                self.bullets.pop(i)

            '''else:
                pos = [bullet[1] + ((settings.width - get_obj_display('world').image_wall.width) / 2), bullet[2] - ((settings.height - get_obj_display('world').image_wall.height) / 2)]
                pos = [int(math.sqrt(pos[0] ** 2)//get_obj_display('world').size_poligon), int(math.sqrt(pos[1] ** 2)//get_obj_display('world').size_poligon)]
                #print(pos)
                block = get_obj_display('world').get_wall_poligon(pos[1], pos[2])
                print(block)
                if block != 'none':
                    if collision.collide(self.bullet_poly, block):
                        self.bullets.pop(i)'''

            #if get_obj_display('world').map_wall[get_obj_display('world').get_block_num(0, 0)] != 'none':
            #    get_obj_display('world').map_wall[get_obj_display('world').get_block_num(0, 0)] = 'none'
            #    get_obj_display('world').set_wall()
            #    get_obj_display('world').import_images()
            #    self.bullets.pop(i)


    def draw(self):

        for bullet in self.bullets:
            self.bullet.sprite.x = bullet[1]
            self.bullet.sprite.y = bullet[2]
            self.bullet.sprite.rotation = bullet[3]
            drawp(self.bullet)
