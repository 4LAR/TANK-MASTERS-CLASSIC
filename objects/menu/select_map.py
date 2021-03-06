class map_list_class():
    def __init__(self):
        self.os_world = os_world()

        #self.map_names, self.map_logos, self.map_dir, self.world_size, self.game_mode = self.search()
        self.search()

    def search(self, type_maps='arcade'):
        filters = []

        if map_filter.death_match_filter: filters.append('death match')
        if map_filter.capture_flag_filter: filters.append('capture flag')
        if map_filter.resource_capture_filter: filters.append('resource capture')

        print('READ MAPS (', filters, ')')
        self.map_names = []
        self.map_logos = []
        self.map_dir    = []
        self.world_size = []
        self.game_mode  = []

        files = os.listdir('maps/'+type_maps)

        for file in files:
            try:
                if file.split('.')[1] == 'map':
                    read_bool = self.os_world.read_file(type_maps + '/' + file.split('.')[0])
                    if read_bool and self.os_world.game_mode in filters:
                        self.world_size.append(self.os_world.world_size)
                        self.game_mode.append(self.os_world.game_mode)
                        self.map_dir.append(type_maps + '/' + file.split('.')[0])
                        self.map_names.append(file.split('.')[0])
                        if os.path.exists('maps/' + type_maps + '/' + file + '/logo.png'):
                            self.map_logos.append('maps/' + type_maps + '/' + file + '/logo.png')
                        else:
                            self.map_logos.append('assets/img/file_not_found.png')
            except:
                pass

        return self.map_names, self.map_logos, self.map_dir, self.world_size, self.game_mode

map_list = map_list_class()

class select_map_buttons():

    def update_page_text(self):
        self.text_page.label.text = 'page: ' + str(self.page) + '/' + str(math.ceil(len(self.map_names) / self.maps_in_page))
        self.update_page()

    def page_up(self):
        if self.page < math.ceil(len(self.map_names) / self.maps_in_page):
            self.page += 1
            self.update_page_text()


    def page_down(self):
        if self.page > 1:
            self.page -= 1
            self.update_page_text()

    def append_map(self, i, x, y):
        self.buttons.append(
            image_button((x * settings.width/2.8) + settings.width/50 + settings.width/3.8,
                (settings.height - settings.height/3.5) - (y * settings.height/4.5),
                'buttons/button_map.png', scale=settings.height/160,
                center=False, arg=('editor(\'' + self.map_dir[i] + '\')') if self.editor else ('select_tank(\'' + self.map_dir[i] + '\')'), #('play(\'' + self.map_names[i] + '\')'),
                image_selected='buttons/button_map_selected.png', shadow=graphics_settings.shadows_buttons
            )
        )

        # image
        self.image_maps.append(
            image_label(self.map_logos[i],
                (x * settings.width/2.8) + settings.width/50 + settings.width/3.8 + settings.width/300,
                (settings.height - settings.height/3.5) - (y * settings.height/4.5) + settings.height/200,
                scale=settings.height/170, pixel=True, no_image=True
            )
        )

        # text
        self.text_maps.append(
            text_label(
                (x * settings.width/2.8) + settings.width/50 + settings.width/3.8 + settings.width/8,
                (settings.height - settings.height/3.5) - (y * settings.height/4.5) + settings.height/6,
                'name: ' + self.map_names[i],
                load_font=True, font='pixel.ttf',
                size=settings.height//48, anchor_x='left',
                color = (150, 150, 150, 255)
            )
        )

        self.text_maps.append(
            text_label(
                (x * settings.width/2.8) + settings.width/50 + settings.width/3.8 + settings.width/8,
                (settings.height - settings.height/3.5) - (y * settings.height/4.5) + settings.height/6 - settings.height/40 - settings.height/40,
                'size: ' + str(self.world_size[i][0]) + '/' + str(self.world_size[i][1]),
                load_font=True, font='pixel.ttf',
                size=settings.height//48, anchor_x='left',
                color = (150, 150, 150, 255)
            )
        )
        self.text_maps.append(
            text_label(
                (x * settings.width/2.8) + settings.width/50 + settings.width/3.8 + settings.width/8,
                (settings.height - settings.height/3.5) - (y * settings.height/4.5) + settings.height/6 - settings.height/40 - settings.height/40 - settings.height/40,
                'game mode: ' + self.game_mode[i],
                load_font=True, font='pixel.ttf',
                size=settings.height//48, anchor_x='left',
                color = (150, 150, 150, 255)
            )
        )

    def update(self):
        if len(self.map_names) > 0:
            if not self.end_load:

                self.append_map(self.num, self.x, self.y)

                if self.x < 1:
                    self.x += 1
                else:
                    self.y += 1
                    self.x = 0

                self.num += 1

                if self.num >= len(self.map_names) or (self.num >= self.page * self.maps_in_page) or (self.y >= 3):
                    self.end_load = True

    def update_page(self):
        self.buttons = []
        self.image_maps = []
        self.text_maps = []

        self.num = ((self.page - 1) * self.maps_in_page)
        self.x = 0
        self.y = 0

        self.end_load = False

        # old load
        '''i = ((self.page - 1) * self.maps_in_page) - 1
        for y in range(3):
            for x in range(2):
                try:
                    i += 1
                    if i >= len(self.map_names) or (i >= self.page * self.maps_in_page):
                        break

                    # button
                    self.append_map(i, x, y)

                except:
                    break'''

    def update_map_list(self):

        self.page = 1
        self.map_names = map_list.map_names
        self.map_logos = map_list.map_logos
        self.map_dir = map_list.map_dir
        self.world_size = map_list.world_size
        self.game_mode = map_list.game_mode


        maps = zip(map_list.map_names, map_list.map_logos, self.map_dir, self.world_size, self.game_mode)
        xs = sorted(maps, key=lambda tup: tup[0])

        self.map_names = [x[0] for x in xs]
        self.map_logos = [x[1] for x in xs]
        self.map_dir = [x[2] for x in xs]
        self.world_size = [x[3] for x in xs]
        self.game_mode = [x[4] for x in xs]

    def reset(self):

        self.buttons = []
        self.image_maps = []
        self.text_maps = []

        self.x = 0
        self.y = 0
        self.num = 0
        self.end_load = True

        self.update_map_list()
        self.update_page()
        self.update_page_text()

    def __init__(self, editor=False):
        map_list.search()

        self.editor = editor

        self.buttons = []
        self.image_maps = []
        self.text_maps = []

        self.text_page = text_label(settings.width/2.3, settings.height/6, 'page: 1/1', load_font=True, font='pixel.ttf', size=settings.height//24, anchor_x='left', color = (150, 150, 150, 255))

        self.text_page_background = image_label('buttons/page_indicator.png', settings.width/2.5, settings.height/10, scale=settings.height/120, pixel=True, shadow=graphics_settings.shadows_buttons)

        self.page_up_button = image_button(settings.width/3 + settings.width/3.55, settings.height/10, 'buttons/button_right_page.png', image_selected='buttons/button_right_page_selected.png', scale=settings.height/120, center=False, arg='get_obj_display(\'select_map_buttons\').page_up()', shadow=graphics_settings.shadows_buttons)
        self.page_down_button = image_button(settings.width/3, settings.height/10, 'buttons/button_left_page.png', image_selected='buttons/button_left_page_selected.png', scale=settings.height/120, center=False, arg='get_obj_display(\'select_map_buttons\').page_down()', shadow=graphics_settings.shadows_buttons)

        self.maps_in_page = 3 * 2

        self.x = 0
        self.y = 0
        self.num = 0
        self.end_load = True

        self.text_no_maps = text_label(settings.width/1.7, settings.height/1.2, 'maps not found', load_font=True, font='pixel.ttf', size=settings.height//18, anchor_x='center', color = (150, 150, 150, 255))
        self.no_maps_background = label(
            settings.width/2.5,
            settings.height - settings.height/4.5,
            (settings.width / 2.7),
            settings.height/10,
            (0, 0, 0), alpha=120
        )

        self.update_map_list()
        self.update_page()
        self.update_page_text()

    def on_mouse_press(self, x, y, button, modifiers):
        for b in self.buttons:
            if b.on_mouse_press(x, y, button, modifiers):
                return True

        if len(self.map_names) > 6:
            self.page_up_button.on_mouse_press(x, y, button, modifiers)
            self.page_down_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for b in self.buttons:
            b.on_mouse_motion(x, y, dx, dy)

        if len(self.map_names) > 6:
            self.page_up_button.on_mouse_motion(x, y, dx, dy)
            self.page_down_button.on_mouse_motion(x, y, dx, dy)

    def draw(self):
        for b in self.image_maps:
            drawp(b)
        for b in self.buttons:
            drawp(b)
        for b in self.text_maps:
            b.draw()

        if len(self.map_names) > 6:
            self.page_up_button.draw()
            self.text_page_background.draw()
            self.page_down_button.draw()
            self.text_page.draw()

        if not len(self.map_names) > 0:
            self.no_maps_background.draw()
            self.text_no_maps.draw()
