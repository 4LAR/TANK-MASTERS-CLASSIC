class world():

    def get_block_num(self, x, y):
        return y * self.world_size[1] + x

    def __init__(self):

        self.size = 8

        self.map_floor = np.array([], dtype='<U32') # пол
        self.map_wall = np.array([], dtype='<U32') # стены



        #self.map_floor = np.full(self.world_size[0] * self.world_size[1], 'grass.0', dtype='<U32')
        #for i in range(32):
        #    self.map_floor[i] = 'dirt.0'

        print("READ WORLD FILE")
        get_obj_other('os_world').read_file('test') # открываем карту

        self.world_size = get_obj_other('os_world').world_size
        if self.world_size[0] > self.world_size[1]:
            self.scale = settings.width/(self.size * self.world_size[0])
        else:
            self.scale = settings.height/(self.size * self.world_size[1])


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
        self.import_images()

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
                    #if SHADOWS:
                    #    image = self.wall_block_img[block[0]].rotate(int(block[1]))
                    #    ibw, ibh = image.size
                    #    image_shadow_wall = get_pil_black_mask(image, self.shadow_alpha)
                    #    for y_ in range(0, self.offs_shadows[0], (1 if (self.offs_shadows[0] > 0) else -1)):
                    #        self.temp_image_shadows.paste(image_shadow_wall, (x * self.size + y_, y * self.size + y_), image_shadow_wall)

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
                    #if SHADOWS:
                    #    image = self.vegetation_block_img[block[0]].rotate(int(block[1]))
                    #    image_vegetation_other = get_pil_black_mask(image, self.shadow_alpha)
                    #    for y_ in range(0, self.offs_shadows[0], (1 if (self.offs_shadows[0] > 0) else -1)):
                    #        self.temp_image_shadows.paste(image_vegetation_other, (x * self.size + y_, y * self.size + y_), mask=image_vegetation_other)


    def set_other_up(self):
        print("SET OTHER UP")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_other_up[self.get_block_num(x, y)].split('.')
                if block[0] != 'none':
                    self.temp_image_other_up.paste(self.other_up_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))
                    #if SHADOWS:
                    #    image = self.other_up_block_img[block[0]].rotate(int(block[1]))
                    #    image_shadow_other = get_pil_black_mask(image, self.shadow_alpha)
                    #    for y_ in range(0, self.offs_shadows[0], (1 if (self.offs_shadows[0] > 0) else -1)):
                    #        self.temp_image_shadows.paste(image_shadow_other, (x * self.size + self.offs_shadows[0], y * self.size + self.offs_shadows[0]), mask=image_shadow_other)

    def set_other_down(self):
        print("SET OTHER DOWN")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_other_down[self.get_block_num(x, y)].split('.')
                if block[0] != 'none':
                    self.temp_image_other_down.paste(self.other_down_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))
                    #if SHADOWS:
                    #    image = self.other_down_block_img[block[0]].rotate(int(block[1]))
                    #    image_shadow_other = get_pil_black_mask(image, self.shadow_alpha)
                    #    for y_ in range(0, self.offs_shadows[0]//2, (1 if (self.offs_shadows[0] > 0) else -1)):
                    #        self.temp_image_shadows_down.paste(image_shadow_other, (x * self.size + y_, y * self.size + y_), mask=image_shadow_other)

    def import_images(self):
        print('IMPORT IMAGES')
        raw_image = self.temp_image_floor.tobytes()
        self.image_floor = pyglet.image.ImageData(self.temp_image_floor.width, self.temp_image_floor.height, 'RGBA', raw_image, pitch=-self.temp_image_floor.width * 4)
        self.image_floor = pyglet.sprite.Sprite(self.image_floor, settings.width, settings.height)
        self.image_floor.scale = self.scale
        self.image_floor.x = (settings.width - self.image_floor.width) / 2
        self.image_floor.y = (settings.height - self.image_floor.height) / 2

        raw_image = self.temp_image_wall.tobytes()
        self.image_wall = pyglet.image.ImageData(self.temp_image_wall.width, self.temp_image_wall.height, 'RGBA', raw_image, pitch=-self.temp_image_wall.width * 4)
        self.image_wall = pyglet.sprite.Sprite(self.image_wall, settings.width, settings.height)
        self.image_wall.scale = self.scale
        self.image_wall.x = (settings.width - self.image_wall.width) / 2
        self.image_wall.y = (settings.height - self.image_wall.height) / 2

        #self.image_floor.width = 1280
        #self.image_floor.height = 720

    def draw(self):
        drawp(self.image_floor)
        drawp(self.image_wall)
