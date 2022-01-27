class map_inventory():
    def __init__(self):

        self.selected_block = 'grass'
        self.selected_type = 0
        #0 - floor
        #1 - wall
        #2 - water
        #3 - vegetation
        #4 - ceiling
        #*5 - other up
        #*6 - other down
        #*7 - effect up
        #*8 - effect down

        self.floor_blocks_name = objects_display[0].floor_blocks_name

        self.wall_block_name = objects_display[0].wall_block_name

        self.water_block_name = objects_display[0].water_block_name

        self.vegetation_block_name = objects_display[0].vegetation_block_name

        self.ceiling_block_name = objects_display[0].ceiling_block_name
        #
        self.other_up_block_name = objects_display[0].other_up_block_name

        self.other_down_block_name = objects_display[0].other_down_block_name
        #
        self.effect_up_name = objects_display[0].effect_up_name


        self.font_scale = settings.height//80
        self.text = text_label(0, settings.height//2, self.selected_block, load_font=True, font='default.ttf', size=self.font_scale, anchor_x='left', color = (180, 180, 180, 255))

        self.backgraund = label(settings.width//10, 0, settings.width - (settings.width//10)*2, settings.height, (0, 0, 0), alpha=120)

        self.image_scale = settings.height//100
        self.image_width = image_label('world/floor/grass.png', settings.width//2.5, settings.height//3, scale=self.image_scale, pixel=False).sprite.width
        self.image_height = image_label('world/floor/grass.png', settings.width//2.5, settings.height//3, scale=self.image_scale, pixel=False).sprite.height

        self.selected_block_img = None

        self.buttons = []
        self.scroll_tick = settings.height/50
        self.scroll = 0

        self.current_rot = 0
        self.brightness = 1.0

        self.block_path = 'world/floor/grass.png'

        # hotbar
        self.hotbar_num = 0
        self.hotbar_blocks = []
        for _ in range(10):
            self.hotbar_blocks.append('')

        self.hotbar_images = []
        for i in range(10):
            self.hotbar_images.append(
                image_label('world/floor/grass.png', settings.width/5 + (settings.width/20) * i, 0, scale=settings.height/100, pixel=False)
            )

        self.hotbar_buttons = []
        for i in range(10):
            self.hotbar_buttons.append(
                image_flag(
                    settings.width/5 + (settings.width/20) * i,
                    0,
                    image='buttons/ramka.png',
                    image_flag='buttons/ramka_selected.png',
                    image_selected_flag='buttons/ramka_selected.png',
                    image_selected='buttons/ramka.png',
                    scale=settings.height/384,
                    function_bool = True,
                    arg='get_obj_display(\'map_inventory\').hotbar_change_num(' + str(i) + ')',

                    shadow=graphics_settings.shadows_buttons

                )
                #image_button(
                #    settings.width/5 + (settings.width/20) * i,
                #    0,
                #    'buttons/ramka.png', scale=settings.height/384,
                #    center=False, arg='exit()', image_selected='buttons/ramka_selected.png',
                #    shadow=graphics_settings.shadows_buttons
                #)
            )
        self.hotbar_change_num(0)

        self.update_inventory()
        self.change_block(0, 'grass')

    def hotbar_change_num(self, num):
        self.hotbar_buttons[num].flag = True
        self.hotbar_num = num
        for i in range(len(self.hotbar_buttons)):
            if i != num:
                self.hotbar_buttons[i].flag = False

    def update_inventory(self):
        self.buttons = []
        self.x = 0
        self.y = self.scroll
        for i in range(len(self.floor_blocks_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*2 - self.image_width*1.2:
                self.x = self.image_width*1.2
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(0, "'+self.floor_blocks_name[i]+'")'
            self.buttons.append(image_button(settings.width//10 + self.x, settings.height - settings.height//10 - self.image_height - self.y, 'world/floor/' + self.floor_blocks_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.y += (self.image_height*1.2)*2
        self.x = 0
        for i in range(len(self.wall_block_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*2 - self.image_width*1.2:
                self.x = self.image_width*1.2
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(1, "'+self.wall_block_name[i]+'")'
            self.buttons.append(image_button(settings.width//10 + self.x, settings.height - settings.height//10 - self.image_height - self.y, 'world/wall/' + self.wall_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.y += (self.image_height*1.2)*2
        self.x = 0
        for i in range(len(self.ceiling_block_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*2 - self.image_width*1.2:
                self.x = self.image_width*1.2
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(4, "'+self.ceiling_block_name[i]+'")'
            self.buttons.append(image_button(settings.width//10 + self.x, settings.height - settings.height//10 - self.image_height - self.y, 'world/ceiling/' + self.ceiling_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.y += (self.image_height*1.2)*2
        self.x = 0
        for i in range(len(self.vegetation_block_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*2 - self.image_width*1.2:
                self.x = self.image_width*1.2
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(3, "'+self.vegetation_block_name[i]+'")'
            self.buttons.append(image_button(settings.width//10 + self.x, settings.height - settings.height//10 - self.image_height - self.y, 'world/vegetation/' + self.vegetation_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))


        self.y += (self.image_height*1.2)*2
        self.x = 0
        for i in range(len(self.water_block_name)):
            if self.water_block_name[i].split('_')[1] == '0':
                self.x += self.image_width*1.2
                if self.x >= settings.width - (settings.width//10)*2 - self.image_width*1.2:
                    self.x = self.image_width*1.2
                    self.y += self.image_height*1.2
                arg = 'objects_display[2].change_block(2, "'+self.water_block_name[i]+'")'
                self.buttons.append(image_button(settings.width//10 + self.x, settings.height - settings.height//10 - self.image_height - self.y, 'world/liquid/' + self.water_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))
                print('world/liquid/' + self.water_block_name[i] + '.png')
        ###########
        self.y += (self.image_height*1.2)*2
        self.x = 0
        for i in range(len(self.other_up_block_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*2 - self.image_width*1.2:
                self.x = self.image_width*1.2
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(5, "'+self.other_up_block_name[i]+'")'
            self.buttons.append(image_button(settings.width//10 + self.x, settings.height - settings.height//10 - self.image_height - self.y, 'world/other_up/' + self.other_up_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.y += (self.image_height*1.2)*2
        self.x = 0
        for i in range(len(self.other_down_block_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*2 - self.image_width*1.2:
                self.x = self.image_width*1.2
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(6, "'+self.other_down_block_name[i]+'")'
            self.buttons.append(image_button(settings.width//10 + self.x, settings.height - settings.height//10 - self.image_height - self.y, 'world/other_down/' + self.other_down_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.y += (self.image_height*1.2)*2
        self.x = 0
        for i in range(len(self.effect_up_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*2 - self.image_width*1.2:
                self.x = self.image_width*1.2
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(7, "'+self.effect_up_name[i]+'")'
            self.buttons.append(image_button(settings.width//10 + self.x, settings.height - settings.height//10 - self.image_height - self.y, 'world/effect_up/' + self.effect_up_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))



    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if objects_display[1].inventory_bool:
            self.scroll += self.scroll_tick * scroll_y
            if self.scroll > 0:
                self.scroll = 0
            self.update_inventory()

        else:
            if not keyboard[key.LCTRL]:
                self.hotbar_num -= int(scroll_y)
                if self.hotbar_num < 0:
                    self.hotbar_num = 9
                elif self.hotbar_num > 9:
                    self.hotbar_num = 0

                self.hotbar_change_num(self.hotbar_num)

    def change_block(self, block_type, block_name):
        self.selected_block = block_name
        self.selected_type = block_type
        self.text.label.text = ((block_name + '.' +  str(self.current_rot)) if not objects_display[1].cut else 'cut') + '\n' + ('press' if objects_display[1].press_or_line else 'line')
        self.selected_block_img = image_label('world/floor/grass.png', settings.width//20, settings.height - settings.height//10, 0, scale=self.image_scale, pixel=False, rotation=self.current_rot, center=True)
        print(self.text.label.text)

    def update_rot_change_block(self):
        self.selected_block_img = image_label('world/floor/grass.png', settings.width//20, settings.height - settings.height//10, scale=self.image_scale, pixel=False, rotation=self.current_rot, center=True)
        self.text.label.text = ((self.selected_block + '.' +  str(self.current_rot)) if not objects_display[1].cut else 'cut') + '\n' + ('press' if objects_display[1].press_or_line else 'line')#self.selected_block + '.' +  str(self.current_rot)
        print(self.text.label.text)

    def on_mouse_motion(self, x, y, dx, dy):
        for b in self.hotbar_buttons:
            b.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        for b in self.hotbar_buttons:
            if b.on_mouse_press(x, y, button, modifiers):
                return True

        if objects_display[1].inventory_bool:
            for button in self.buttons:
                button.on_mouse_press(x, y, button, modifiers)

    def draw(self):
        if objects_display[1].inventory_bool:
            self.backgraund.draw()
            for button in self.buttons:
                button.draw()
        self.text.draw()

        for img in self.hotbar_images:
            drawp(img)

        for b in self.hotbar_buttons:
            drawp(b)

        #self.selected_block_img.draw()
