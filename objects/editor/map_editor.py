class map(object):
    def get_block_num(self, x, y):
        return y * self.world_size[0] + x

    def __init__(self, name, new=False):

        self.inventory_bool = False

        self.show_celling = True
        self.show_vegetation = True
        self.show_other_down = True
        self.show_other_up = True

        self.show_effect_up = True

        self.show_grid = True

        self.cut = False
        # True - Press ; False - line
        self.press_or_line = True

        self.batch = pyglet.graphics.Batch()

        self.range = 5

        self.world_size = [64, 64]

        self.map_floor = np.array([], dtype='<U32')

        self.map_wall = np.array([], dtype='<U32')

        self.poligons_wall = []

        self.size = 8
        self.resize = (8, 8)

        self.size_poligon = self.size * settings.height/1400

        self.world_max_size = [self.world_size[0] * self.size_poligon, self.world_size[1] * self.size_poligon]

        self.floor_blocks_img = objects_display[0].floor_blocks_img
        self.wall_block_img = objects_display[0].wall_block_img
        self.water_block_img = objects_display[0].water_block_img
        self.vegetation_block_img = objects_display[0].vegetation_block_img
        self.ceiling_block_img = objects_display[0].ceiling_block_img

        self.other_up_block_img = objects_display[0].other_up_block_img
        self.other_down_block_img = objects_display[0].other_down_block_img

        self.effect_up_img = objects_display[0].effect_up_img

        self.circle_spawn = circle_label(0, 0, 360, size_circle=5, color=(9, 0, 0, 255))
        self.image_spawn = image_label('spawn.png', 0, 0, pixel=False, center=False)

        self.image_floor = None
        self.image_wall = None

        self.image_water = None

        self.image_vegetation = None

        self.image_ceiling = None

        self.image_grid = None

        self.world_file_name = ''

        self.world_file_name = name
        print("READ WORLD FILE")
        if len(name) < 1:
            select_map(editor=True)
        if new:
            width = 64
            height = 32
            objects_display[0].generate_world([width, height])
        else:
            objects_display[0].read_file(self.world_file_name, False)

        '''inp = input('1 - generate (test.map)\n2 - open (test.map)\n3 - update map (43 to 44)\n>')
        if inp == '1':
            self.world_file_name = input('WRITE WORLD NAME: ')
            print("START GENERATE")
            width = int(input('WIDTH: '))
            height = int(input('HEIGHT: '))
            objects_display[0].generate_world([width, height])
        elif inp == '2':

            self.world_file_name = input('WRITE WORLD NAME: ')
            print("READ WORLD FILE")
            objects_display[0].read_file(self.world_file_name, False)
        elif inp == '3':
            self.world_file_name = input('WRITE WORLD NAME: ')
            self.world_file_name_new = input('WRITE NEW WORLD NAME: ')
            print("READ WORLD FILE")
            objects_display[0].read_file('os_world', False)
            print("READ WORLD FILE")
            objects_display[0].read_file(self.world_file_name, True)
            print("SAVE WORLD")
            objects_display[0].save_file(self.world_file_name_new)'''

        self.spawn = objects_display[0].save_world_obj.spawn
        print(self.spawn)

        self.world_size = objects_display[0].world_size

        self.map_floor = objects_display[0].map_floor

        self.map_wall = objects_display[0].map_wall

        self.map_water = objects_display[0].map_water

        self.map_vegetation = objects_display[0].map_vegetation

        self.map_ceiling = objects_display[0].map_ceiling
        print('==> ', len(self.map_wall))
        #
        self.map_other_up = objects_display[0].map_other_up
        self.map_other_down = objects_display[0].map_other_down

        self.map_effect_up = objects_display[0].map_effect_up
        self.map_effect_down = objects_display[0].map_effect_down

        #self.scale = settings.height/1400
        if self.world_size[0] > self.world_size[1]:
            self.scale = settings.width/(self.size * self.world_size[0])
        else:
            self.scale = settings.height/(self.size * self.world_size[1])
        self.tick_scale = settings.height/30000
        self.pos = [-((self.world_size[0] * self.size)//4), -((self.world_size[1] * self.size)//4)]   # позиция камеры

        self.speed = settings.height//144

        self.temp_image_floor = None
        self.temp_image_wall = None
        self.temp_image_water = None
        self.temp_image_vegetation = None
        self.temp_image_ceiling = None
        #
        self.temp_image_other_up = None
        self.temp_image_other_down = None

        self.update_render()

    def get_floor(self, x, y):
        return self.map_floor[self.get_block_num(x, y)]

    def get_wall(self, x, y):
        return self.map_wall[self.get_block_num(x, y)]

    def get_wall_poligon(self, x, y):
        return self.poligons_wall[self.get_block_num(x, y)]

    def update_render(self):
        self.update_render_floor()
        self.update_render_wall()
        self.update_render_water()
        self.update_render_vegetation()
        self.update_render_ceiling()
        #
        self.update_render_other_up()
        self.update_render_other_down()

        self.update_render_effect_up()

        self.update_render_grid()

    ########

    def update_render_effect_up(self, pos=None):
        if pos == None:
            temp_image_other_up = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
            print("UPDATE EFFECT UP")
            for y in range(self.world_size[1]):
                for x in range(self.world_size[0]):
                    block = self.map_effect_up[self.get_block_num(x, y)].split('.')
                    if block[0] != 'none':
                        temp_image_other_up.paste(self.effect_up_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

        else:
            temp_image_other_up = self.temp_image_effect_up
            block = self.map_effect_up[self.get_block_num(pos[0], pos[1])].split('.')
            if block[0] != 'none':
                temp_image_other_up.paste(self.effect_up_img[block[0]].rotate(int(block[1])), (pos[0] * self.size, pos[1] * self.size))

        self.temp_image_effect_up = temp_image_other_up
        raw_image = temp_image_other_up.tobytes()
        self.image_effect_up = pyglet.image.ImageData(temp_image_other_up.width, temp_image_other_up.height, 'RGBA', raw_image, pitch=-temp_image_other_up.width * 4)
        self.image_effect_up = pyglet.sprite.Sprite(self.image_effect_up, settings.width//4, settings.height//2)
        self.image_effect_up.scale = self.scale

    ########
    def update_render_other_up(self, pos=None):
        if pos == None:
            temp_image_other_up = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
            print("UPDATE OTHER UP")
            for y in range(self.world_size[1]):
                for x in range(self.world_size[0]):
                    block = self.map_other_up[self.get_block_num(x, y)].split('.')
                    if block[0] != 'none':
                        temp_image_other_up.paste(self.other_up_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

        else:
            temp_image_other_up = self.temp_image_other_up
            block = self.map_other_up[self.get_block_num(pos[0], pos[1])].split('.')
            if block[0] != 'none':
                temp_image_other_up.paste(self.other_up_block_img[block[0]].rotate(int(block[1])), (pos[0] * self.size, pos[1] * self.size))

        self.temp_image_other_up = temp_image_other_up
        raw_image = temp_image_other_up.tobytes()
        self.image_other_up = pyglet.image.ImageData(temp_image_other_up.width, temp_image_other_up.height, 'RGBA', raw_image, pitch=-temp_image_other_up.width * 4)
        self.image_other_up = pyglet.sprite.Sprite(self.image_other_up, settings.width//4, settings.height//2)
        self.image_other_up.scale = self.scale

    def update_render_grid(self):
        temp_image_grid = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
        print("UPDATE GRID")
        resize = (8, 8)
        grid_image = Image.open('img/editor/grid.png').resize(resize, Image.NEAREST).convert("RGBA")
        for y in range(self.world_size[1]):
            for x in range(self.world_size[0]):
                temp_image_grid.paste(grid_image, (x * self.size, y * self.size))

        self.temp_image_grid = temp_image_grid
        raw_image = temp_image_grid.tobytes()
        self.image_grid = pyglet.image.ImageData(temp_image_grid.width, temp_image_grid.height, 'RGBA', raw_image, pitch=-temp_image_grid.width * 4)
        self.image_grid = pyglet.sprite.Sprite(self.image_grid, settings.width//4, settings.height//2)
        self.image_grid.scale = self.scale

    def update_render_other_down(self, pos=None):
        if pos == None:
            temp_image_other_down = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
            print("UPDATE OTHER DOWN")
            for y in range(self.world_size[1]):
                for x in range(self.world_size[0]):
                    block = self.map_other_down[self.get_block_num(x, y)].split('.')
                    if block[0] != 'none':
                        temp_image_other_down.paste(self.other_down_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

        else:
            temp_image_other_down = self.temp_image_other_down
            block = self.map_other_down[self.get_block_num(pos[0], pos[1])].split('.')
            if block[0] != 'none':
                temp_image_other_down.paste(self.other_down_block_img[block[0]].rotate(int(block[1])), (pos[0] * self.size, pos[1] * self.size))

        self.temp_image_other_down = temp_image_other_down
        raw_image = temp_image_other_down.tobytes()
        self.image_other_down = pyglet.image.ImageData(temp_image_other_down.width, temp_image_other_down.height, 'RGBA', raw_image, pitch=-temp_image_other_down.width * 4)
        self.image_other_down = pyglet.sprite.Sprite(self.image_other_down, settings.width//4, settings.height//2)
        self.image_other_down.scale = self.scale

    ############

    def update_render_wall(self, pos=None):
        if pos == None:
            temp_image_wall = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
            print("UPDATE WALL")
            for y in range(self.world_size[1]):
                for x in range(self.world_size[0]):
                    block = self.get_wall(x, y).split('.')
                    if block[0] != 'none':
                        temp_image_wall.paste(self.wall_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

        else:
            temp_image_wall = self.temp_image_wall
            block = self.get_wall(pos[0], pos[1]).split('.')
            if block[0] != 'none':
                temp_image_wall.paste(self.wall_block_img[block[0]].rotate(int(block[1])), (pos[0] * self.size, pos[1] * self.size))

        self.temp_image_wall = temp_image_wall
        raw_image = temp_image_wall.tobytes()
        self.image_wall = pyglet.image.ImageData(temp_image_wall.width, temp_image_wall.height, 'RGBA', raw_image, pitch=-temp_image_wall.width * 4)
        self.image_wall = pyglet.sprite.Sprite(self.image_wall, settings.width//4, settings.height//2)
        self.image_wall.scale = self.scale

    def update_render_floor(self, pos=None):
        if pos == None:
            temp_image_floor = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
            print("UPDATE FLOOR")
            for y in range(self.world_size[1]):
                for x in range(self.world_size[0]):
                    block = self.map_floor[self.get_block_num(x, y)].split('.')
                    if block[0] != 'none':
                        temp_image_floor.paste(self.floor_blocks_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

        else:
            temp_image_floor = self.temp_image_floor
            block = self.get_floor(pos[0], pos[1]).split('.')
            if block[0] != 'none':
                temp_image_floor.paste(self.floor_blocks_img[block[0]].rotate(int(block[1])), (pos[0] * self.size, pos[1] * self.size))

        self.temp_image_floor = temp_image_floor
        raw_image = temp_image_floor.tobytes()
        self.image_floor = pyglet.image.ImageData(temp_image_floor.width, temp_image_floor.height, 'RGBA', raw_image, pitch=-temp_image_floor.width * 4)
        self.image_floor = pyglet.sprite.Sprite(self.image_floor, settings.width//4, settings.height//2)
        self.image_floor.scale = self.scale

    def update_render_ceiling(self, pos=None):
        if pos == None:
            temp_image_ceiling = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
            print("UPDATE CEILING")
            for y in range(self.world_size[1]):
                for x in range(self.world_size[0]):
                    block = self.map_ceiling[self.get_block_num(x, y)].split('.')
                    if block[0] != 'none':
                        #temp_image_ceiling.paste(self.ceiling_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))
                        temp_image_ceiling.paste(self.ceiling_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

        else:
            temp_image_ceiling = self.temp_image_ceiling
            block = self.map_ceiling[self.get_block_num(pos[0], pos[1])].split('.')
            if block[0] != 'none':
                temp_image_ceiling.paste(self.ceiling_block_img[block[0]].rotate(int(block[1])), (pos[0] * self.size, pos[1] * self.size))

        self.temp_image_ceiling = temp_image_ceiling
        raw_image = temp_image_ceiling.tobytes()
        self.image_ceiling = pyglet.image.ImageData(temp_image_ceiling.width, temp_image_ceiling.height, 'RGBA', raw_image, pitch=-temp_image_ceiling.width * 4)
        self.image_ceiling = pyglet.sprite.Sprite(self.image_ceiling, settings.width//4, settings.height//2)
        self.image_ceiling.scale = self.scale

    def update_render_water(self, pos=None):
        if pos == None:
            temp_image_water = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
            print("UPDATE WATER")
            for y in range(self.world_size[1]):
                for x in range(self.world_size[0]):
                    block = self.map_water[self.get_block_num(x, y)].split('.')
                    if block[0] != 'none':
                        temp_image_water.paste(self.water_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

        else:
            temp_image_water = self.temp_image_water
            block = self.map_water[self.get_block_num(pos[0], pos[1])].split('.')
            if block[0] != 'none':
                temp_image_water.paste(self.water_block_img[block[0]].rotate(int(block[1])), (pos[0] * self.size, pos[1] * self.size))

        self.temp_image_water = temp_image_water
        raw_image = temp_image_water.tobytes()
        self.image_water = pyglet.image.ImageData(temp_image_water.width, temp_image_water.height, 'RGBA', raw_image, pitch=-temp_image_water.width * 4)
        self.image_water = pyglet.sprite.Sprite(self.image_water, settings.width//4, settings.height//2)
        self.image_water.scale = self.scale

    def update_render_vegetation(self, pos=None):
        if pos == None:
            temp_image_vegetation = Image.new('RGBA', (self.world_size[0] * self.size, self.world_size[1] * self.size))
            print("UPDATE VEGETATION")
            for y in range(self.world_size[1]):
                for x in range(self.world_size[0]):
                    block = self.map_vegetation[self.get_block_num(x, y)].split('.')
                    if block[0] != 'none':
                        temp_image_vegetation.paste(self.vegetation_block_img[block[0]].rotate(int(block[1])), (x * self.size, y * self.size))

        else:
            temp_image_vegetation = self.temp_image_vegetation
            block = self.map_vegetation[self.get_block_num(pos[0], pos[1])].split('.')
            if block[0] != 'none':
                temp_image_vegetation.paste(self.vegetation_block_img[block[0]].rotate(int(block[1])), (pos[0] * self.size, pos[1] * self.size))

        self.temp_image_vegetation = temp_image_vegetation
        raw_image = temp_image_vegetation.tobytes()
        self.image_vegetation = pyglet.image.ImageData(temp_image_vegetation.width, temp_image_vegetation.height, 'RGBA', raw_image, pitch=-temp_image_vegetation.width * 4)
        self.image_vegetation = pyglet.sprite.Sprite(self.image_vegetation, settings.width//4, settings.height//2)
        self.image_vegetation.scale = self.scale
        #image_ceiling

    def set_spawn(self, pos):
        print("SET SPAWN")
        self.spawn.append([pos[0], pos[1], 0, 0])

    def del_spawn(self, pos):
        print(pos)
        print("DEL SPAWN")
        for i in range(len(self.spawn)):
            if self.spawn[i][0] == pos[0] and self.spawn[i][1] == pos[1]:
                self.spawn.pop(i)

    def update_poligons():
        print("GENERATE WALL POLIGONS")
        for y in range(self.world_size[1]):
            for x in range(self.world_size[0]):
                if self.get_wall(x, self.world_size[1]-1 - y) != 'none':
                    poligon_block = collision.Poly(v(x * self.size_poligon, y * self.size_poligon),
                    [
                        v(0, 0),
                        v(self.size_poligon, 0),
                        v(self.size_poligon, self.size_poligon),
                        v(0, self.size_poligon)
                    ])
                    self.poligons_wall.append(poligon_block)
                else:
                    self.poligons_wall.append('none')

    def update(self):
        if not self.inventory_bool:
            if keyboard[key.W]:
                self.pos[1] -= self.speed
            elif keyboard[key.S]:
                self.pos[1] += self.speed
            if keyboard[key.A]:
                self.pos[0] += self.speed
            elif keyboard[key.D]:
                self.pos[0] -= self.speed

        #if keyboard[key.Q]:
        #    self.map_floor[0] = self.floor_blocks_img['grass']
        #    self.update_render_floor()
        self.image_floor.x = self.pos[0]
        self.image_floor.y = self.pos[1]

        self.image_wall.x = self.pos[0]
        self.image_wall.y = self.pos[1]

        self.image_water.x = self.pos[0]
        self.image_water.y = self.pos[1]

        self.image_vegetation.x = self.pos[0]
        self.image_vegetation.y = self.pos[1]

        self.image_ceiling.x = self.pos[0]
        self.image_ceiling.y = self.pos[1]

        ##

        self.image_other_up.x = self.pos[0]
        self.image_other_up.y = self.pos[1]

        self.image_other_down.x = self.pos[0]
        self.image_other_down.y = self.pos[1]

        self.image_effect_up.x = self.pos[0]
        self.image_effect_up.y = self.pos[1]

        ##

        self.image_grid.x = self.pos[0]
        self.image_grid.y = self.pos[1]


    def on_key_press(self, symbol, modifiers):
        if symbol == key.P:
            print("SAVE WORLD")
            objects_display[0].save_file(self.world_file_name)
        elif symbol == key.E:
            if self.inventory_bool:
                self.inventory_bool = False
            else:
                self.inventory_bool = True

        elif symbol == key.C:
            if self.show_celling:
                self.show_celling = False
            else:
                self.show_celling = True
        elif symbol == key.V:
            if self.show_vegetation:
                self.show_vegetation = False
            else:
                self.show_vegetation = True

        elif symbol == key.B:
            if self.show_other_up:
                self.show_other_up = False
            else:
                self.show_other_up = True

        elif symbol == key.L:
            if self.show_effect_up:
                self.show_effect_up = False
            else:
                self.show_effect_up = True

        elif symbol == key.N:
            if self.show_other_down:
                self.show_other_down = False
            else:
                self.show_other_down = True

        elif symbol == key.Q:
            if self.show_grid:
                self.show_grid = False
            else:
                self.show_grid = True

        elif symbol == key.X:
            if self.cut:
                self.cut = False
            else:
                self.cut = True

        elif symbol == key.T:
            if self.press_or_line:
                self.press_or_line = False
            else:
                self.press_or_line = True

        elif symbol == key.J:
            self.scale_map(1)

        elif symbol == key.K:
            self.scale_map(-1)

        elif symbol == key.F:
            objects_display[2].selected_type = -1

        elif symbol == key.R:
            objects_display[2].current_rot += 90
            if objects_display[2].current_rot > 270:
                objects_display[2].current_rot = 0
            objects_display[2].update_rot_change_block()

        objects_display[2].text.label.text = ((objects_display[2].selected_block + '.' +  str(objects_display[2].current_rot)) if not self.cut else 'cut') + '\n' + ('press' if self.press_or_line else 'line')

        if symbol == pyglet.window.key.ESCAPE:
            print("SAVE WORLD")
            objects_display[0].save_file(self.world_file_name)
            menu()
            return pyglet.event.EVENT_HANDLED

    def on_mouse_press(self, x, y, button, modifiers):
        if self.press_or_line:
            self.set_or_cut_block(x, y, button)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.press_or_line:
            button = buttons
            self.set_or_cut_block(x, y, button)

    def set_or_cut_block(self, x, y, button):
        if not self.inventory_bool:
            if button == 1 and not self.cut:
                x_ = int( ( ( (self.pos[0] - x)/self.scale )//self.size) ) + 1
                y_ = int( ( ( (self.pos[1] - y)/self.scale )//self.size) )

                _x_ = int(math.sqrt(x_ ** 2))
                _y_ = self.world_size[1] - int(math.sqrt(y_ ** 2))

                print(_x_, _y_)
                print(self.get_block_num(_x_, _y_))
                # [_x_, _y_]
                if objects_display[2].selected_type == 0:
                    self.map_floor[self.get_block_num(_x_, _y_)] = objects_display[2].selected_block + '.' + str(objects_display[2].current_rot)
                    self.update_render_floor()

                elif objects_display[2].selected_type == 1:
                    self.map_wall[self.get_block_num(_x_, _y_)] = objects_display[2].selected_block + '.' + str(objects_display[2].current_rot)
                    self.update_render_wall()

                elif objects_display[2].selected_type == 2:
                    self.map_water[self.get_block_num(_x_, _y_)] = objects_display[2].selected_block + '.' + str(objects_display[2].current_rot)
                    self.update_render_water()

                elif objects_display[2].selected_type == 3:
                    self.map_vegetation[self.get_block_num(_x_, _y_)] = objects_display[2].selected_block + '.' + str(objects_display[2].current_rot)
                    self.update_render_vegetation()

                elif objects_display[2].selected_type == 4:
                    self.map_ceiling[self.get_block_num(_x_, _y_)] = objects_display[2].selected_block + '.' + str(objects_display[2].current_rot)
                    self.update_render_ceiling()
                #####
                elif objects_display[2].selected_type == 5:
                    self.map_other_up[self.get_block_num(_x_, _y_)] = objects_display[2].selected_block + '.' + str(objects_display[2].current_rot)
                    self.update_render_other_up()

                elif objects_display[2].selected_type == 6:
                    self.map_other_down[self.get_block_num(_x_, _y_)] = objects_display[2].selected_block + '.' + str(objects_display[2].current_rot)
                    self.update_render_other_down()

                elif objects_display[2].selected_type == 7:
                    self.map_effect_up[self.get_block_num(_x_, _y_)] = objects_display[2].selected_block + '.' + str(objects_display[2].current_rot)
                    self.update_render_effect_up()

                elif objects_display[2].selected_type == -1:
                    #self.map_other_down[self.get_block_num(_x_, _y_)] = objects_display[2].selected_block + '.' + str(objects_display[2].current_rot)
                    self.set_spawn([_x_, _y_])

            if button == 4 or self.cut:
                x_ = int( ( ( (self.pos[0] - x)/self.scale )//self.size) ) + 1
                y_ = int( ( ( (self.pos[1] - y)/self.scale )//self.size) )

                _x_ = int(math.sqrt(x_ ** 2))
                _y_ = self.world_size[1] - int(math.sqrt(y_ ** 2))

                print(_x_, _y_)

                if objects_display[2].selected_type == 0:
                    self.map_floor[self.get_block_num(_x_, _y_)] = 'none'
                    self.update_render_floor()

                elif objects_display[2].selected_type == 1:
                    self.map_wall[self.get_block_num(_x_, _y_)] = 'none'
                    self.update_render_wall()

                elif objects_display[2].selected_type == 2:
                    self.map_water[self.get_block_num(_x_, _y_)] = 'none'
                    self.update_render_water()

                elif objects_display[2].selected_type == 3:
                    self.map_vegetation[self.get_block_num(_x_, _y_)] = 'none'
                    self.update_render_vegetation()

                elif objects_display[2].selected_type == 4:
                    self.map_ceiling[self.get_block_num(_x_, _y_)] = 'none'
                    self.update_render_ceiling()
                #######
                elif objects_display[2].selected_type == 5:
                    self.map_other_up[self.get_block_num(_x_, _y_)] = 'none'
                    self.update_render_other_up()

                elif objects_display[2].selected_type == 6:
                    self.map_other_down[self.get_block_num(_x_, _y_)] = 'none'
                    self.update_render_other_down()

                elif objects_display[2].selected_type == 7:
                    self.map_effect_up[self.get_block_num(_x_, _y_)] = 'none'
                    self.update_render_effect_up()

                elif objects_display[2].selected_type == -1:
                    self.del_spawn([_x_, _y_])

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.scale_map(scroll_y)

    def scale_map(self, scroll_y):
        if not self.inventory_bool:
            self.scale += self.tick_scale * scroll_y
            self.image_wall.scale = self.scale
            self.image_floor.scale = self.scale
            self.image_water.scale = self.scale
            self.image_vegetation.scale = self.scale
            self.image_ceiling.scale = self.scale

            self.image_other_up.scale = self.scale
            self.image_other_down.scale = self.scale

            self.image_effect_up.scale = self.scale

            self.image_grid.scale = self.scale


    def draw(self):
        drawp(self.image_floor)

        drawp(self.image_wall)

        if self.show_other_down:
            drawp(self.image_other_down)

        drawp(self.image_water)

        if self.show_vegetation:
            drawp(self.image_vegetation)

        if self.show_other_up:
            drawp(self.image_other_up)

        if self.show_celling:
            drawp(self.image_ceiling)

        if self.show_effect_up:
            drawp(self.image_effect_up)



        for s in self.spawn:
            self.image_spawn.sprite.x = int((s[0]) * (self.size))*self.scale + self.pos[0]
            self.image_spawn.sprite.y = int((self.world_size[1] - s[1] -1) * (self.size))*self.scale + self.pos[1]
            self.image_spawn.sprite.scale = self.scale

            drawp(self.image_spawn)
            #self.circle_spawn.edit(360, ((s[0] * self.size_poligon) * self.scale + self.pos[0]), (((self.world_size[1] - s[1]) * self.size_poligon) * self.scale + self.pos[1]))
            #self.circle_spawn.draw()

        if self.show_grid:
            drawp(self.image_grid)
            drawp(self.image_grid)
