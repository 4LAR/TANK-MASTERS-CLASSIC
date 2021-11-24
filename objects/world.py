class world():

    def get_block_num(self, x, y):
        return y * self.world_size[1] + x

    def __init__(self):
        self.world_size = [32, 32]
        self.size = 8

        self.map_floor = np.array([], dtype='<U32') # пол
        self.map_wall = np.array([], dtype='<U32') # стены

        self.scale = settings.height/(self.size * self.world_size[1])

        self.map_floor = np.full(self.world_size[0] * self.world_size[1], 'grass.0', dtype='<U32')
        for i in range(32):
            self.map_floor[i] = 'dirt.0'



        self.temp_image_floor = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        self.temp_image_wall = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))

        self.floor_blocks_img = get_obj_other('os_world').floor_blocks_img
        self.wall_block_img = get_obj_other('os_world').wall_block_img
        self.water_block_img = get_obj_other('os_world').water_block_img
        self.vegetation_block_img = get_obj_other('os_world').vegetation_block_img
        self.ceiling_block_img = get_obj_other('os_world').ceiling_block_img
        self.other_up_block_img = get_obj_other('os_world').other_up_block_img
        self.other_down_block_img = get_obj_other('os_world').other_down_block_img

        self.set_floor()
        self.import_images()

    def set_floor(self):
        print("SET FLOOR")
        for y in range(self.world_size[1]):
            #print(y)
            for x in range(self.world_size[0]):
                block = self.map_floor[self.get_block_num(x, y)].split('.')
                if block[0] != 'none':
                    self.temp_image_floor.paste(self.floor_blocks_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

    def import_images(self):
        print('IMPORT IMAGES')
        raw_image = self.temp_image_floor.tobytes()
        self.image_floor = pyglet.image.ImageData(self.temp_image_floor.width, self.temp_image_floor.height, 'RGBA', raw_image, pitch=-self.temp_image_floor.width * 4)
        self.image_floor = pyglet.sprite.Sprite(self.image_floor, settings.width, settings.height)
        self.image_floor.scale = self.scale
        self.image_floor.x = (settings.width - self.image_floor.width) / 2
        self.image_floor.y = 0

        #self.image_floor.width = 1280
        #self.image_floor.height = 720

    def draw(self):
        drawp(self.image_floor)
