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


        self.font_scale = settings.height//36
        self.text = text_label(settings.height/20, settings.height/30, self.selected_block, load_font=True, font='pixel.ttf', size=self.font_scale, anchor_x='left', color = (180, 180, 180, 255))

        self.backgraund = label(0, settings.height - settings.height/6 - (settings.height/10)*6, settings.width, (settings.height/10)*7, (0, 0, 0), alpha=200)

        self.image_scale = settings.height//100
        self.image_width = image_label('world/floor/grass.png', settings.width//2.5, settings.height//3, scale=self.image_scale, pixel=False).sprite.width
        self.image_height = image_label('world/floor/grass.png', settings.width//2.5, settings.height//3, scale=self.image_scale, pixel=False).sprite.height

        self.buttons = []
        self.scroll_tick = settings.height/50
        self.scroll = 0

        self.current_rot = 0
        self.brightness = 1.0

        self.block_path = 'world/floor/grass.png'

        # inventory select type
        types = [
            'floor',
            'wall',
            'liquid',
            'vegetation',
            'other up',
            'other down',
            'other'
        ]
        self.inventory_buttons_select_type = []
        self.inventory_buttons_select_num = 0
        for i in range(len(types)):
            self.inventory_buttons_select_type.append(
                image_flag(
                    0,
                    settings.height - settings.height/6 - (settings.height/10)*i,
                    image='buttons/button_clear_full_kv.png',
                    image_flag='buttons/button_clear_full_kv_flag.png',
                    image_selected_flag='buttons/button_clear_full_kv_flag_selected.png',
                    image_selected='buttons/button_clear_full_kv_selected.png',
                    scale=settings.height/160,
                    function_bool = True,
                    arg='get_obj_display(\'map_inventory\').inventory_buttons_select(' + str(i) + ')',

                    text=types[i],
                    text_color = (150, 150, 150, 255),
                    font='pixel.ttf',
                    text_indent=settings.height/40#,

                    #shadow=graphics_settings.shadows_buttons

                )
            )

        self.inventory_buttons_select(0)

        self.hotbar_buttons = []

        self.selected_block_img = None
        self.hotbar_buttons.append(
            image_button(
                settings.width/18, settings.height/12,
                'buttons/ramka.png', scale=settings.height/240,
                center=True, arg='get_obj_display("map").open_inventory()',
                image_selected='buttons/ramka_selected.png',
                shadow=graphics_settings.shadows_buttons
            )
        )

        self.update_inventory()
        self.change_block(0, 'grass')

    def update_image_block(self):
        path = [
            'world/floor/',
            'world/wall/',
            'world/liquid/',
            'world/vegetation/',
            'world/other_up/',
            'world/other_down/'
        ]
        self.selected_block_img = image_label(
            path[self.selected_type] + self.selected_block + '.png',
            settings.width/18, settings.height/12,
            scale=settings.height/65,
            pixel=False,
            center=True,
            rotation=self.current_rot,
        )


    def inventory_buttons_select(self, num):
        self.inventory_buttons_select_type[num].flag = True
        self.inventory_buttons_select_num = num
        for i in range(len(self.inventory_buttons_select_type)):
            if i != num:
                self.inventory_buttons_select_type[i].flag = False

    def update_inventory(self):
        self.buttons = []

        self.x = -self.image_width*1.2
        self.y = settings.height/10
        self.buttons.append([])
        for i in range(len(self.floor_blocks_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*3 - self.image_width*1.2:
                self.x = 0
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(0, "'+self.floor_blocks_name[i]+'")'
            self.buttons[0].append(image_button(settings.width/4 + self.x, settings.height - self.image_height - self.y, 'world/floor/' + self.floor_blocks_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.x = -self.image_width*1.2
        self.y = settings.height/10
        self.buttons.append([])
        for i in range(len(self.wall_block_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*3 - self.image_width*1.2:
                self.x = 0
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(1, "'+self.wall_block_name[i]+'")'
            self.buttons[1].append(image_button(settings.width/4 + self.x, settings.height - self.image_height - self.y, 'world/wall/' + self.wall_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.x = -self.image_width*1.2
        self.y = settings.height/10
        self.buttons.append([])
        for i in range(len(self.water_block_name)):
            if self.water_block_name[i].split('_')[1] == '0':
                self.x += self.image_width*1.2
                if self.x >= settings.width - (settings.width//10)*3 - self.image_width*1.2:
                    self.x = 0
                    self.y += self.image_height*1.2
                arg = 'objects_display[2].change_block(2, "'+self.water_block_name[i]+'")'
                self.buttons[2].append(image_button(settings.width/4 + self.x, settings.height - self.image_height - self.y, 'world/liquid/' + self.water_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))


        self.x = -self.image_width*1.2
        self.y = settings.height/10
        self.buttons.append([])
        for i in range(len(self.vegetation_block_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*3 - self.image_width*1.2:
                self.x = 0
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(3, "'+self.vegetation_block_name[i]+'")'
            self.buttons[3].append(image_button(settings.width/4 + self.x, settings.height - self.image_height - self.y, 'world/vegetation/' + self.vegetation_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.x = -self.image_width*1.2
        self.y = settings.height/10
        self.buttons.append([])
        for i in range(len(self.other_up_block_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*3 - self.image_width*1.2:
                self.x = 0
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(5, "'+self.other_up_block_name[i]+'")'
            self.buttons[4].append(image_button(settings.width/4 + self.x, settings.height - self.image_height - self.y, 'world/other_up/' + self.other_up_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.x = -self.image_width*1.2
        self.y = settings.height/10
        self.buttons.append([])
        for i in range(len(self.other_down_block_name)):
            self.x += self.image_width*1.2
            if self.x >= settings.width - (settings.width//10)*3 - self.image_width*1.2:
                self.x = 0
                self.y += self.image_height*1.2
            arg = 'objects_display[2].change_block(6, "'+self.other_down_block_name[i]+'")'
            self.buttons[5].append(image_button(settings.width/4 + self.x, settings.height - self.image_height - self.y, 'world/other_down/' + self.other_down_block_name[i] + '.png', scale=self.image_scale, center=False, arg=arg))

        self.buttons.append([])

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass
        #if objects_display[1].inventory_bool:
        #    self.scroll += self.scroll_tick * scroll_y
        #    if self.scroll > 0:
        #        self.scroll = 0
        #    self.update_inventory()

        #else:
        #    if not keyboard[key.LCTRL]:
        #        self.hotbar_num -= int(scroll_y)
        #        if self.hotbar_num < 0:
        #            self.hotbar_num = 9
        #        elif self.hotbar_num > 9:
        #            self.hotbar_num = 0
        #        self.hotbar_change_num(self.hotbar_num)

    def change_block(self, block_type, block_name):
        self.selected_block = block_name
        self.selected_type = block_type
        self.text.label.text = ((block_name + '.' +  str(self.current_rot)) if not objects_display[1].cut else 'cut') + '\n' + ('press' if objects_display[1].press_or_line else 'line')
        self.update_image_block()

    def update_rot_change_block(self):
        self.text.label.text = ((self.selected_block + '.' +  str(self.current_rot)) if not objects_display[1].cut else 'cut') + '\n' + ('press' if objects_display[1].press_or_line else 'line')#self.selected_block + '.' +  str(self.current_rot)
        self.update_image_block()

    def on_mouse_motion(self, x, y, dx, dy):
        if objects_display[1].inventory_bool:
            for b in self.inventory_buttons_select_type:
                b.on_mouse_motion(x, y, dx, dy)

        else:
            pass

        for b in self.hotbar_buttons:
            b.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if objects_display[1].inventory_bool:
            for b in self.inventory_buttons_select_type:
                if b.on_mouse_press(x, y, button, modifiers):
                    return True

            for button in self.buttons[self.inventory_buttons_select_num]:
                button.on_mouse_press(x, y, button, modifiers)

        else:
            pass

        for b in self.hotbar_buttons:
            b.on_mouse_press(x, y, button, modifiers)

    def draw(self):
        drawp(self.selected_block_img)
        for b in self.hotbar_buttons:
            drawp(b)

        if objects_display[1].inventory_bool:
            self.backgraund.draw()
            for button in self.buttons[self.inventory_buttons_select_num]:
                button.draw()

            for img in self.inventory_buttons_select_type:
                drawp(img)

        self.text.draw()
