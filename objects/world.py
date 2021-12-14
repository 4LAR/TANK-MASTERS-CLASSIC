SHADOWS = True

class world():

    def get_block_num(self, x, y):
        return y * self.world_size[0] + x

    def __init__(self, map_name='test'):
        self.map_name = map_name

        self.size = 8

        self.range = 2

        self.shadow_alpha = 84

        self.offs_shadows = [-settings.width//180, settings.width//300]#[-settings.width//80, settings.width//200]



        #self.map_floor = np.full(self.world_size[0] * self.world_size[1], 'grass.0', dtype='<U32')
        #for i in range(32):
        #    self.map_floor[i] = 'dirt.0'

        print("READ WORLD FILE")
        get_obj_other('os_world').read_file(self.map_name) # открываем карту

        self.world_size = get_obj_other('os_world').world_size
        if self.world_size[0] > self.world_size[1]:
            self.scale = settings.width/(self.size * self.world_size[0])
        else:
            self.scale = settings.height/(self.size * self.world_size[1])

        self.size_poligon = self.size * self.scale
        self.poligons_wall = [] # список полигонов блоков
        self.poligons_water = [] # список полигонов блоков

        self.spawn = get_obj_other('os_world').save_world_obj.spawn

        self.floor_blocks_img = get_obj_other('os_world').floor_blocks_img
        self.wall_block_img = get_obj_other('os_world').wall_block_img
        self.water_block_img = get_obj_other('os_world').water_block_img
        self.vegetation_block_img = get_obj_other('os_world').vegetation_block_img
        self.ceiling_block_img = get_obj_other('os_world').ceiling_block_img
        self.other_up_block_img = get_obj_other('os_world').other_up_block_img
        self.other_down_block_img = get_obj_other('os_world').other_down_block_img

        # создаём пустые изображения для слоёв карты
        self.temp_image_floor = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_wall = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_water = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_vegetation = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_ceiling = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_other_up = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_other_down = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_effect_up = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))

        self.temp_image_shadows = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_shadows_down = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_shadows_up = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        #self.image_shadows = None

        self.map_floor = get_obj_other('os_world').map_floor
        self.map_wall = get_obj_other('os_world').map_wall
        self.map_water = get_obj_other('os_world').map_water
        self.map_vegetation = get_obj_other('os_world').map_vegetation
        self.map_ceiling = get_obj_other('os_world').map_ceiling
        self.map_other_up = get_obj_other('os_world').map_other_up
        self.map_other_down = get_obj_other('os_world').map_other_down
        self.map_effect_up = get_obj_other('os_world').map_effect_up


        self.set_floor()
        self.set_wall()
        self.set_water()
        self.set_vegetation()
        self.set_other_up()
        self.set_other_down()

        self.import_images()

        self.generate_wall_polygons()
        self.generate_water_polygons()

    def get_wall_poligon(self, x, y):
        return self.poligons_wall[self.get_block_num(x, y)]

    def get_water_poligon(self, x, y):
        return self.poligons_water[self.get_block_num(x, y)]

    def set_floor(self):
        print("SET FLOOR")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_floor[self.get_block_num(x, y)].split('.')
                if block[0] != 'none':
                    self.temp_image_floor.paste(self.floor_blocks_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

    def set_wall(self):
        print("SET WALL")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_wall[self.get_block_num(x, y)].split('.')
                if block[0] != 'none':
                    self.temp_image_wall.paste(self.wall_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))
                    if SHADOWS:
                        image = self.wall_block_img[block[0]].rotate(int(block[1]))
                        ibw, ibh = image.size
                        image_shadow_wall = get_pil_black_mask(image, self.shadow_alpha)
                        for y_ in range(0, self.offs_shadows[0], (1 if (self.offs_shadows[0] > 0) else -1)):
                            self.temp_image_shadows.paste(image_shadow_wall, (x * self.size + y_, y * self.size + y_), image_shadow_wall)

    def set_water(self):
        print("SET WATER")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_water[self.get_block_num(x, y)].split('.')
                if block[0] != 'none':
                    self.temp_image_water.paste(self.water_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

    def set_vegetation(self):
        print("SET VEGETATION")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_vegetation[self.get_block_num(x, y)].split('.')
                if block[0] != 'none':
                    self.temp_image_vegetation.paste(self.vegetation_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))
                    if SHADOWS:
                        image = self.vegetation_block_img[block[0]].rotate(int(block[1]))
                        image_vegetation_other = get_pil_black_mask(image, self.shadow_alpha)
                        for y_ in range(0, self.offs_shadows[0], (1 if (self.offs_shadows[0] > 0) else -1)):
                            self.temp_image_shadows.paste(image_vegetation_other, (x * self.size + y_, y * self.size + y_), mask=image_vegetation_other)


    def set_other_up(self):
        print("SET OTHER UP")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_other_up[self.get_block_num(x, y)].split('.')
                if block[0] != 'none':
                    self.temp_image_other_up.paste(self.other_up_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))
                    if SHADOWS:
                        image = self.other_up_block_img[block[0]].rotate(int(block[1]))
                        image_shadow_other = get_pil_black_mask(image, self.shadow_alpha)
                        for y_ in range(0, self.offs_shadows[0], (1 if (self.offs_shadows[0] > 0) else -1)):
                            self.temp_image_shadows.paste(image_shadow_other, (x * self.size + self.offs_shadows[0], y * self.size + self.offs_shadows[0]), mask=image_shadow_other)

    def set_other_down(self):
        print("SET OTHER DOWN")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_other_down[self.get_block_num(x, y)].split('.')
                if block[0] != 'none':
                    self.temp_image_other_down.paste(self.other_down_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))
                    if SHADOWS:
                        image = self.other_down_block_img[block[0]].rotate(int(block[1]))
                        image_shadow_other = get_pil_black_mask(image, self.shadow_alpha)
                        for y_ in range(0, self.offs_shadows[0]//2, (1 if (self.offs_shadows[0] > 0) else -1)):
                            self.temp_image_shadows_down.paste(image_shadow_other, (x * self.size + y_, y * self.size + y_), mask=image_shadow_other)

    def generate_wall_polygons(self):
        print("GENERATE WALL POLYGONS")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_wall[self.get_block_num(x, (self.world_size[1] - 1) - y)]
                if block != 'none':
                    array_pol = []
                    if os.path.isfile('img/world/wall/'+block.split('.')[0]+'.info'):
                        f = open('img/world/wall/'+block.split('.')[0]+'.info', 'r')
                        arr_info = f.read().split('\n')
                        for info in arr_info:
                            array_pol.append(v(int(info.split(' ')[0]) * (self.size_poligon/8)-self.size_poligon/2, int(info.split(' ')[1]) * (self.size_poligon/8)-self.size_poligon/2))
                    else:
                        array_pol = [
                            v(-self.size_poligon/2, -self.size_poligon/2),
                            v(self.size_poligon/2, -self.size_poligon/2),
                            v(self.size_poligon/2, self.size_poligon/2),
                            v(-self.size_poligon/2, self.size_poligon/2)
                        ]
                    poligon_block = collision.Poly(v(((settings.width - self.image_wall.width) / 2) + x * self.size_poligon + self.size_poligon/2,
                    ((settings.height - self.image_wall.height) / 2) + y * self.size_poligon + self.size_poligon/2), array_pol)
                    poligon_block.angle = math.radians(int(block.split('.')[1]) - 180)

                    poligon_block.x = ((settings.width - self.image_wall.width) / 2) + (x * self.size * self.scale)
                    poligon_block.y = ((settings.height - self.image_wall.height) / 2) + (y * self.size * self.scale)

                    self.poligons_wall.append(poligon_block)
                else:
                    self.poligons_wall.append('none')

    def generate_water_polygons(self):
        print("GENERATE WATER POLYGONS")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_water[self.get_block_num(x, (self.world_size[1] - 1) - y)]
                if block != 'none':
                    array_pol = []
                    if os.path.isfile('img/world/wall/'+block.split('.')[0]+'.info'):
                        f = open('img/world/wall/'+block.split('.')[0]+'.info', 'r')
                        arr_info = f.read().split('\n')
                        for info in arr_info:
                            array_pol.append(v(int(info.split(' ')[0]) * (self.size_poligon/8)-self.size_poligon/2, int(info.split(' ')[1]) * (self.size_poligon/8)-self.size_poligon/2))
                    else:
                        array_pol = [
                            v(-self.size_poligon/2, -self.size_poligon/2),
                            v(self.size_poligon/2, -self.size_poligon/2),
                            v(self.size_poligon/2, self.size_poligon/2),
                            v(-self.size_poligon/2, self.size_poligon/2)
                        ]
                    poligon_block = collision.Poly(v(((settings.width - self.image_wall.width) / 2) + x * self.size_poligon + self.size_poligon/2,
                    ((settings.height - self.image_wall.height) / 2) + y * self.size_poligon + self.size_poligon/2), array_pol)
                    poligon_block.angle = math.radians(int(block.split('.')[1]) - 180)

                    poligon_block.x = ((settings.width - self.image_wall.width) / 2) + (x * self.size * self.scale)
                    poligon_block.y = ((settings.height - self.image_wall.height) / 2) + (y * self.size * self.scale)

                    self.poligons_water.append(poligon_block)
                else:
                    self.poligons_water.append('none')

    def clear_images_wall(self):
        self.temp_image_shadows_up = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_wall = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))

    def update_images_wall(self):
        self.image_wall = PIL_to_pyglet(self.temp_image_wall, self.scale)
        self.image_wall.x = (settings.width - self.image_wall.width) / 2
        self.image_wall.y = (settings.height - self.image_wall.height) / 2

        self.image_shadows = PIL_to_pyglet(self.temp_image_shadows, self.scale)
        self.image_shadows.x = (settings.width - self.image_wall.width) / 2
        self.image_shadows.y = (settings.height - self.image_wall.height) / 2

    def import_images(self):
        print('IMPORT IMAGES')
        #self.image_floor = pyglet.image.ImageData(self.temp_image_floor.width, self.temp_image_floor.height, 'RGBA', raw_image, pitch=-self.temp_image_floor.width * 4)
        #self.image_floor = pyglet.sprite.Sprite(self.image_floor, settings.width, settings.height)
        #self.image_floor.scale = self.scale

        self.image_floor = PIL_to_pyglet(self.temp_image_floor, self.scale)
        self.image_floor.x = (settings.width - self.image_floor.width) / 2
        self.image_floor.y = (settings.height - self.image_floor.height) / 2

        self.image_other_down = PIL_to_pyglet(self.temp_image_other_down, self.scale)
        self.image_other_down.x = (settings.width - self.image_other_down.width) / 2
        self.image_other_down.y = (settings.height - self.image_other_down.height) / 2

        self.image_wall = PIL_to_pyglet(self.temp_image_wall, self.scale)
        self.image_wall.x = (settings.width - self.image_wall.width) / 2
        self.image_wall.y = (settings.height - self.image_wall.height) / 2

        self.image_water = PIL_to_pyglet(self.temp_image_water, self.scale)
        self.image_water.x = (settings.width - self.image_wall.width) / 2
        self.image_water.y = (settings.height - self.image_wall.height) / 2

        self.image_vegetation = PIL_to_pyglet(self.temp_image_vegetation, self.scale)
        self.image_vegetation.x = (settings.width - self.image_wall.width) / 2
        self.image_vegetation.y = (settings.height - self.image_wall.height) / 2

        self.image_other_up = PIL_to_pyglet(self.temp_image_other_up, self.scale)
        self.image_other_up.x = (settings.width - self.image_other_up.width) / 2
        self.image_other_up.y = (settings.height - self.image_other_up.height) / 2

        # тени
        self.image_shadows = PIL_to_pyglet(self.temp_image_shadows, self.scale)
        self.image_shadows.x = (settings.width - self.image_wall.width) / 2
        self.image_shadows.y = (settings.height - self.image_wall.height) / 2

        self.image_shadows_down = PIL_to_pyglet(self.temp_image_shadows_down, self.scale)
        self.image_shadows_down.x = (settings.width - self.image_wall.width) / 2
        self.image_shadows_down.y = (settings.height - self.image_wall.height) / 2

        #self.image_floor.width = 1280
        #self.image_floor.height = 720

    def draw(self):
        drawp(self.image_floor)
        drawp(self.image_water)
        drawp(self.image_shadows_down)
        drawp(self.image_other_down)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            menu()

        return pyglet.event.EVENT_HANDLED

class walls():
    def __init__(self):
        pass

    def draw(self):
        drawp(get_obj_display('world').image_shadows)
        drawp(get_obj_display('world').image_wall)

        drawp(get_obj_display('world').image_vegetation)
        drawp(get_obj_display('world').image_other_up)
