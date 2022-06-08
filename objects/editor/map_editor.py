class map(object):
    def get_block_num(self, x, y):
        return y * self.world_size[0] + x

    def __init__(self, name, new=False):

        self.mouse_pos = [0, 0]

        self.inventory_bool = False

        self.show_floor = True
        self.show_wall = True
        self.show_other_down = True
        self.show_water = True
        self.show_vegetation = True
        self.show_other_up = True
        self.show_celling = False # for TANK MASTERS (no TANK MASTERS CLASSIC)
        self.show_effect_up = True

        self.show_cursor = True

        self.show_grid = True

        self.cut = False
        self.press_or_line = True

        self.press_space = False

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
        self.image_spawn = image_label('editor/spawn.png', 0, 0, pixel=False, center=False)

        self.select_block_grid_image = image_label('buttons/frame/frame_selected.png', 0, 0, pixel=False, center=False)

        self.image_floor = None
        self.image_wall = None

        self.image_water = None

        self.image_vegetation = None

        self.image_ceiling = None

        self.image_grid = None

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

        self.select_block_grid_image.sprite.scale = self.scale/2

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
        temp_image_grid = Image.new('RGBA', (self.world_size[0] * self.size * 2, self.world_size[1] * self.size * 2))
        print("UPDATE GRID")
        resize = (16, 16)
        grid_image = Image.open('assets/img/editor/grid.png').resize(resize, Image.NEAREST).convert("RGBA")
        for y in range(self.world_size[1]):
            for x in range(self.world_size[0]):
                temp_image_grid.paste(grid_image, (x * (self.size*2), y * (self.size*2)))

        self.temp_image_grid = temp_image_grid
        raw_image = temp_image_grid.tobytes()
        self.image_grid = pyglet.image.ImageData(temp_image_grid.width, temp_image_grid.height, 'RGBA', raw_image, pitch=-temp_image_grid.width * 4)
        self.image_grid = pyglet.sprite.Sprite(self.image_grid, settings.width//4, settings.height//2)
        self.image_grid.scale = self.scale/2

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

    def update_camera_pos(self, x=0, y=0):
        self.pos = [self.pos[0] + x, self.pos[1] + y]
        self.update_pos_cursor()

    def save(self):
        print("SAVE WORLD")
        objects_display[0].save_file(self.world_file_name)

        get_obj_display('editor_gui').last_save_text.label.text = "last save: " + time.strftime("%H:%M", time.localtime())

    def exit(self):
        self.save()
        menu()
        background_sound.play('assets/sound/background/forest waterfall.wav')
        return pyglet.event.EVENT_HANDLED

    def update(self):
        if not self.inventory_bool:
            speed = self.speed * 2 if keyboard[key.LSHIFT] else self.speed
            if not keyboard[key.LCTRL]:
                if keyboard[key.W]:
                    self.update_camera_pos(y=-speed)
                elif keyboard[key.S]:
                    self.update_camera_pos(y=speed)
                if keyboard[key.A]:
                    self.update_camera_pos(x=speed)
                elif keyboard[key.D]:
                    self.update_camera_pos(x=-speed)

            self.press_space = keyboard[key.SPACE]

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

        self.image_other_up.x = self.pos[0]
        self.image_other_up.y = self.pos[1]

        self.image_other_down.x = self.pos[0]
        self.image_other_down.y = self.pos[1]

        self.image_effect_up.x = self.pos[0]
        self.image_effect_up.y = self.pos[1]

        self.image_grid.x = self.pos[0]
        self.image_grid.y = self.pos[1]


    def rotate_block(self, deg=90):
        get_obj_display('map_inventory').current_rot += deg
        if get_obj_display('map_inventory').current_rot > 270:
            get_obj_display('map_inventory').current_rot = 0
        elif get_obj_display('map_inventory').current_rot < 0:
            get_obj_display('map_inventory').current_rot = 270

        get_obj_display('map_inventory').update_rot_change_block()

    def on_key_press(self, symbol, modifiers):
        if modifiers & key.MOD_SHIFT:
            if symbol == key.R:
                self.rotate_block(90)

        elif modifiers & key.MOD_CTRL:
            if symbol == key.S:
                self.save()

        elif symbol == key.EQUAL:
            self.scale_map(1)

        elif symbol == key.MINUS:
            self.scale_map(-1)

        elif symbol == key.F:
            get_obj_display('map_inventory').selected_type = -1

        elif symbol == key.R:
            self.rotate_block(-90)

        elif symbol == key.E:
            self.open_inventory()

        # hotbar
        # cursor_type
        elif symbol == key._1:
            get_obj_display('editor_gui').change_cursor_type(0)

        elif symbol == key._2:
            get_obj_display('editor_gui').change_cursor_type(1)

        elif symbol == key._3:
            get_obj_display('editor_gui').change_cursor_type(2)

        #draw_type
        elif symbol == key.X:
            get_obj_display('editor_gui').change_draw_type(
                (1 if get_obj_display('editor_gui').draw_type[0].flag else 0)
            )

        get_obj_display('map_inventory').text.label.text = (get_obj_display('map_inventory').selected_block + '.' +  str(get_obj_display('map_inventory').current_rot))

        if symbol == pyglet.window.key.ESCAPE:
           return self.exit()

    def open_inventory(self):
        self.inventory_bool = not self.inventory_bool

    def on_mouse_press(self, x, y, button, modifiers):
        if get_obj_display('editor_gui').cursor_type[1].flag:
            if not (self.press_space or get_obj_display('editor_gui').cursor_type[0].flag):
                self.set_or_cut_block(x, y, button)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if get_obj_display('editor_gui').cursor_type[2].flag and not (self.press_space or get_obj_display('editor_gui').cursor_type[0].flag):
            button = buttons
            self.set_or_cut_block(x, y, button)

        if self.press_space or get_obj_display('editor_gui').cursor_type[0].flag:
            self.update_camera_pos(x=dx, y=dy)

    def set_or_cut_block(self, x, y, button):
        ok = True
        for b in get_obj_display('map_inventory').hotbar_buttons:
            if b.selected:
                ok = False
                break

        if not self.inventory_bool and ok and not get_obj_display('editor_gui').hover:
            x_ = int( ( ( (self.pos[0] - x)/self.scale )//self.size) ) + 1
            y_ = int( ( ( (self.pos[1] - y)/self.scale )//self.size) )

            _x_ = int(math.sqrt(x_ ** 2))
            _y_ = self.world_size[1] - int(math.sqrt(y_ ** 2))

            if ((0 <= -x_) and (-x_ < self.world_size[0])) and ((0 < -y_) and (-y_ <= self.world_size[1])):
                if button == 1 and not get_obj_display('editor_gui').draw_type[1].flag:

                    if get_obj_display('map_inventory').selected_type == 0:
                        self.map_floor[self.get_block_num(_x_, _y_)] = get_obj_display('map_inventory').selected_block + '.' + str(get_obj_display('map_inventory').current_rot)
                        self.update_render_floor()

                    elif get_obj_display('map_inventory').selected_type == 1:
                        self.map_wall[self.get_block_num(_x_, _y_)] = get_obj_display('map_inventory').selected_block + '.' + str(get_obj_display('map_inventory').current_rot)
                        self.update_render_wall()

                    elif get_obj_display('map_inventory').selected_type == 2:
                        self.map_water[self.get_block_num(_x_, _y_)] = get_obj_display('map_inventory').selected_block + '.' + str(get_obj_display('map_inventory').current_rot)
                        self.update_render_water()

                    elif get_obj_display('map_inventory').selected_type == 3:
                        self.map_vegetation[self.get_block_num(_x_, _y_)] = get_obj_display('map_inventory').selected_block + '.' + str(get_obj_display('map_inventory').current_rot)
                        self.update_render_vegetation()

                    elif get_obj_display('map_inventory').selected_type == 4:
                        self.map_ceiling[self.get_block_num(_x_, _y_)] = get_obj_display('map_inventory').selected_block + '.' + str(get_obj_display('map_inventory').current_rot)
                        self.update_render_ceiling()
                    #####
                    elif get_obj_display('map_inventory').selected_type == 5:
                        self.map_other_up[self.get_block_num(_x_, _y_)] = get_obj_display('map_inventory').selected_block + '.' + str(get_obj_display('map_inventory').current_rot)
                        self.update_render_other_up()

                    elif get_obj_display('map_inventory').selected_type == 6:
                        self.map_other_down[self.get_block_num(_x_, _y_)] = get_obj_display('map_inventory').selected_block + '.' + str(get_obj_display('map_inventory').current_rot)
                        self.update_render_other_down()

                    elif get_obj_display('map_inventory').selected_type == 7:
                        self.map_effect_up[self.get_block_num(_x_, _y_)] = get_obj_display('map_inventory').selected_block + '.' + str(get_obj_display('map_inventory').current_rot)
                        self.update_render_effect_up()

                    elif get_obj_display('map_inventory').selected_type == -1:
                        self.set_spawn([_x_, _y_])

                if button == 4 or get_obj_display('editor_gui').draw_type[1].flag:

                    if get_obj_display('map_inventory').selected_type == 0:
                        self.map_floor[self.get_block_num(_x_, _y_)] = 'none'
                        self.update_render_floor()

                    elif get_obj_display('map_inventory').selected_type == 1:
                        self.map_wall[self.get_block_num(_x_, _y_)] = 'none'
                        self.update_render_wall()

                    elif get_obj_display('map_inventory').selected_type == 2:
                        self.map_water[self.get_block_num(_x_, _y_)] = 'none'
                        self.update_render_water()

                    elif get_obj_display('map_inventory').selected_type == 3:
                        self.map_vegetation[self.get_block_num(_x_, _y_)] = 'none'
                        self.update_render_vegetation()

                    elif get_obj_display('map_inventory').selected_type == 4:
                        self.map_ceiling[self.get_block_num(_x_, _y_)] = 'none'
                        self.update_render_ceiling()
                    #######
                    elif get_obj_display('map_inventory').selected_type == 5:
                        self.map_other_up[self.get_block_num(_x_, _y_)] = 'none'
                        self.update_render_other_up()

                    elif get_obj_display('map_inventory').selected_type == 6:
                        self.map_other_down[self.get_block_num(_x_, _y_)] = 'none'
                        self.update_render_other_down()

                    elif get_obj_display('map_inventory').selected_type == 7:
                        self.map_effect_up[self.get_block_num(_x_, _y_)] = 'none'
                        self.update_render_effect_up()

                    elif get_obj_display('map_inventory').selected_type == -1:
                        self.del_spawn([_x_, _y_])

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        #if keyboard[key.LCTRL]:
        self.scale_map(scroll_y)

    def update_pos_cursor(self):
        if self.show_cursor:
            x_ = int( ( ( (self.pos[0] - self.mouse_pos[0])/self.scale )//self.size) ) + 1
            y_ = int( ( ( (self.pos[1] - self.mouse_pos[1])/self.scale )//self.size) ) + 1

            self.select_block_grid_image.sprite.x = self.pos[0] - (x_ * 8 * self.scale)
            self.select_block_grid_image.sprite.y = self.pos[1] - (y_ * 8 * self.scale)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = [x, y]
        self.update_pos_cursor()

    def scale_map(self, scroll_y):
        if not self.inventory_bool:
            self.pos = [self.pos[0] - (self.mouse_pos[0]*scroll_y) / 10, self.pos[1] - (self.mouse_pos[1] * scroll_y) / 10]

            self.scale += self.tick_scale * (scroll_y * 10)
            self.image_wall.scale = self.scale
            self.image_floor.scale = self.scale
            self.image_water.scale = self.scale
            self.image_vegetation.scale = self.scale
            self.image_ceiling.scale = self.scale

            self.image_other_up.scale = self.scale
            self.image_other_down.scale = self.scale

            self.image_effect_up.scale = self.scale

            self.image_grid.scale = self.scale/2

            self.select_block_grid_image.sprite.scale = self.scale/2
            self.update_pos_cursor()

    def draw(self):
        if get_obj_display('editor_gui').layers_buttons[0].flag:
            drawp(self.image_floor)

        if get_obj_display('editor_gui').layers_buttons[3].flag:
            drawp(self.image_water)

        if get_obj_display('editor_gui').layers_buttons[1].flag:
            drawp(self.image_wall)

        if get_obj_display('editor_gui').layers_buttons[2].flag:
            drawp(self.image_other_down)

        if get_obj_display('editor_gui').layers_buttons[4].flag:
            drawp(self.image_vegetation)

        if get_obj_display('editor_gui').layers_buttons[5].flag:
            drawp(self.image_other_up)

        #if get_obj_display('gui').layers_buttons[6]:
        #    drawp(self.image_ceiling)

        #if get_obj_display('editor_gui').layers_buttons[6].flag:
        #    drawp(self.image_effect_up)

        for s in self.spawn:
            self.image_spawn.sprite.x = int((s[0]) * (self.size))*self.scale + self.pos[0]
            self.image_spawn.sprite.y = int((self.world_size[1] - s[1] -1) * (self.size))*self.scale + self.pos[1]
            self.image_spawn.sprite.scale = self.scale

            drawp(self.image_spawn)

        if get_obj_display('editor_gui').layers_buttons[6].flag:
            drawp(self.image_grid)
            drawp(self.image_grid)

        if self.show_cursor and not(self.press_space or get_obj_display('editor_gui').cursor_type[0].flag):
            drawp(self.select_block_grid_image)
