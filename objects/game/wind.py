class wind():

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

        size = get_obj_display('world').size

        image = Image.open('img/world/' +
            ('snow/leaf' if get_obj_display('game_settings').snow else 'leaf')
         + '.png').resize((size, size), Image.NEAREST).convert("RGBA")

        self.random_offs = [0, 3]
        self.random_count = [0, 4]
        self.random_spawn = 20
        self.speed = settings.height/1500

        self.max_count = 36
        self.images_count = 6

        self.wind_images = []
        self.wind_shadows_images = []

        for i in range(self.images_count):
            self.temp_wind_image = Image.new('RGBA',
                (
                    get_obj_display('world').world_size[0] * size,
                    get_obj_display('world').world_size[1] * size
                )
            )

            for y in range(get_obj_display('world').world_size[1]):
                for x in range(get_obj_display('world').world_size[0]):
                    block = get_obj_display('world').map_vegetation[get_obj_display('world').get_block_num(x, y)].split('.')
                    if block[0] != 'none':
                        if random.randint(0, 100) <= self.random_spawn:
                            for j in range(random.randint(self.random_count[0], self.random_count[1])):
                                self.temp_wind_image.paste(image.rotate([0, 90][random.randint(0, 1)]), (x * size + random.randint(self.random_offs[0], self.random_offs[1]), y * size + random.randint(self.random_offs[0], self.random_offs[1])))

            x, y = self.get_speed_by_deg_sp(game_settings.wind_deg, ((self.speed * self.max_count) / self.images_count) * i)

            self.wind_images.append([PIL_to_pyglet(self.temp_wind_image, get_obj_display('world').scale), int((self.max_count/self.images_count) * i)])
            self.wind_images[i][0].x = ((settings.width - get_obj_display('world').image_wall.width) / 2) + x
            self.wind_images[i][0].y = ((settings.height - get_obj_display('world').image_wall.height) / 2) + y

            temp_shadow = get_pil_black_mask(self.temp_wind_image, 255//2)
            self.wind_shadows_images.append(PIL_to_pyglet(temp_shadow, get_obj_display('world').scale))

    def update(self):
        if graphics_settings.draw_leaf and not get_obj_display('game_settings').pause:
            x, y = self.get_speed_by_deg_sp(180 - game_settings.wind_deg, self.speed)
            for i in range(self.images_count):
                self.wind_images[i][0].x += x
                self.wind_images[i][0].y += y
                self.wind_images[i][1] += 1
                self.wind_images[i][0].opacity = (255/self.max_count) * (self.max_count - self.wind_images[i][1])

                if self.wind_images[i][1] > self.max_count:
                    self.wind_images[i][0].x = (settings.width - get_obj_display('world').image_wall.width) / 2
                    self.wind_images[i][0].y = (settings.height - get_obj_display('world').image_wall.height) / 2
                    self.wind_images[i][1] = 0
                    self.wind_images[i][0].opacity = 255

                self.wind_shadows_images[i].x = self.wind_images[i][0].x + get_obj_display('world').offs_shadows[0]
                self.wind_shadows_images[i].y = self.wind_images[i][0].y + get_obj_display('world').offs_shadows[1]
                self.wind_shadows_images[i].opacity = self.wind_images[i][0].opacity//2

    def draw(self):
        if graphics_settings.draw_leaf:
            for w in self.wind_shadows_images:
                w.x += get_obj_display('world').map_offs[0]
                w.y += get_obj_display('world').map_offs[1]
                drawp(w)
                w.x -= get_obj_display('world').map_offs[0]
                w.y -= get_obj_display('world').map_offs[1]

            for w in self.wind_images:
                w[0].x += get_obj_display('world').map_offs[0]
                w[0].y += get_obj_display('world').map_offs[1]
                drawp(w[0])
                w[0].x -= get_obj_display('world').map_offs[0]
                w[0].y -= get_obj_display('world').map_offs[1]
