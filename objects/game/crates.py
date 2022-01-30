class crates():
    def __init__(self):
        self.sound = Sound()

        self.creates_obj = []
        scale = get_obj_display('world').scale / 1.2

        self.crates_list = []

        self.crates_obj_shadow = PIL_to_pyglet(
            get_pil_black_mask(
                Image.open('img/crates/crate.png').convert("RGBA"),
                get_obj_display('world').shadow_alpha
            ),
            scale, True
        )

        self.creates_obj.append(
            image_label(
                'crates/crate.png',
                settings.width//2, settings.height//2,
                scale=scale, pixel=False,
                center=True
            )
        )

        self.crate_poly = collision.Poly(v(100, 100),
        [
            v(-self.creates_obj[0].sprite.width/2 + self.creates_obj[0].sprite.width/50, -self.creates_obj[0].sprite.height/2 + self.creates_obj[0].sprite.height/50),
            v(self.creates_obj[0].sprite.width/2 - self.creates_obj[0].sprite.width/50, -self.creates_obj[0].sprite.height/2 + self.creates_obj[0].sprite.height/50),
            v(self.creates_obj[0].sprite.width/2 - self.creates_obj[0].sprite.width/50, self.creates_obj[0].sprite.height/2 - self.creates_obj[0].sprite.height/50),
            v(-self.creates_obj[0].sprite.width/2 + self.creates_obj[0].sprite.width/50, self.creates_obj[0].sprite.height/2 - self.creates_obj[0].sprite.height/50)
        ])
        '''self.crate_poly = collision.Poly(v(100, 100),
        [
            v(0, 0),
            v(self.creates_obj[0].sprite.width, 0),
            v(self.creates_obj[0].sprite.width, self.creates_obj[0].sprite.height),
            v(0, self.creates_obj[0].sprite.height)
        ])'''

        self.add_crate()

    def add_crate(self):
        while True:
            rand_pos = [
                random.randint(0, get_obj_display('world').world_size[0]),
                random.randint(0, get_obj_display('world').world_size[1])
            ]

            '''check_pos_list = [
                [0, 0],
                [1, 0],
                [0, 1],
                [1, 1]
            ]'''
            check_pos_list = [
                [-1, 1],
                [0, 1],
                [1, 1],

                [-1, 0],
                [0, 0],
                [1, 0],

                [-1, -1],
                [0, -1],
                [1, -1]
            ]

            ok = True
            for i in range(len(check_pos_list)):
                try:
                    if (
                        get_obj_display('world').get_wall_poligon(rand_pos[0] + check_pos_list[i][0], rand_pos[1] + check_pos_list[i][1]) != 'none'
                        or get_obj_display('world').get_water_poligon(rand_pos[0] + check_pos_list[i][0], rand_pos[1] + check_pos_list[i][1]) != 'none'
                    ):
                        ok = False
                except:
                    ok = False

            if ok:
                rand_pos = [
                    get_obj_display('world').image_floor.x + (rand_pos[0] * get_obj_display('world').size * get_obj_display('world').scale) - get_obj_display('world').map_offs[0],
                    get_obj_display('world').image_floor.y + ((get_obj_display('world').world_size[1] - rand_pos[1]) * get_obj_display('world').size * get_obj_display('world').scale) - get_obj_display('world').map_offs[1]
                ]

                self.crates_list.append([rand_pos[0], rand_pos[1]])

                break


    def update(self):
        for i in range(len(self.crates_list)-1, -1, -1):
            self.crate_poly.pos.x = self.crates_list[i][0]
            self.crate_poly.pos.y = self.crates_list[i][1]

            for p in get_obj_display('players').tanks:
                if collision.collide(p.poligon_body, self.crate_poly):
                    self.crates_list.pop(i)
                    self.sound.play('upgrade.wav')
                    self.add_crate()
                    break

    def draw(self):
        for c in self.crates_list:
            self.crates_obj_shadow.x = c[0] + get_obj_display('world').offs_shadows[0] / 3 + get_obj_display('world').map_offs[0]
            self.crates_obj_shadow.y = c[1] - get_obj_display('world').offs_shadows[0] / 3 + get_obj_display('world').map_offs[1]
            drawp(self.crates_obj_shadow)
            self.creates_obj[0].x = c[0] + get_obj_display('world').map_offs[0]
            self.creates_obj[0].y = c[1] + get_obj_display('world').map_offs[1]
            self.creates_obj[0].update_image(True)
            drawp(self.creates_obj[0])
