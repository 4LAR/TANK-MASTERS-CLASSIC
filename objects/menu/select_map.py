class map_list_class():
    def __init__(self):
        self.map_names, self.map_logos, self.map_dir = self.search()

    def search(self, type_maps='arcade'):
        print('READ MAPS')
        maps_names = []
        maps_logos = []
        map_dir   = []

        files = os.listdir('maps/'+type_maps)

        for file in files:
            try:
                if file.split('.')[1] == 'map':
                    map_dir.append(type_maps + '/' + file.split('.')[0])
                    maps_names.append(file.split('.')[0])
                    if os.path.exists('maps/' + type_maps + '/' + file + '/logo.png'):
                        maps_logos.append('maps/' + type_maps + '/' + file + '/logo.png')
                    else:
                        maps_logos.append('img/file_not_found.png')
            except:
                pass
        return maps_names, maps_logos, map_dir

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

        self.world_size = []
        self.game_mode = []

        for i in range(len(self.map_names)-1, -1, -1):
            read_bool = self.os_world.read_file(self.map_dir[i])
            #print(self.map_names[i], read_bool, i)
            if read_bool:
                self.world_size.append(self.os_world.world_size)
                self.game_mode.append('death match')
            else:
                self.map_names.pop(i)
                self.map_logos.pop(i)
                self.map_dir.pop(i)

        self.num = ((self.page - 1) * self.maps_in_page) - 1
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


        maps = zip(map_list.map_names, map_list.map_logos, self.map_dir)
        xs = sorted(maps, key=lambda tup: tup[0])

        self.map_names = [x[0] for x in xs]
        self.map_logos = [x[1] for x in xs]
        self.map_dir = [x[2] for x in xs]

    def __init__(self, editor=False):
        map_list.search()

        self.editor = editor

        self.buttons = []
        self.image_maps = []
        self.text_maps = []

        self.os_world = os_world()

        self.text_page = text_label(settings.width/2.3, settings.height/6, 'page: 1/1', load_font=True, font='pixel.ttf', size=settings.height//24, anchor_x='left', color = (150, 150, 150, 255))

        self.maps_in_page = 3 * 2

        self.x = 0
        self.y = 0
        self.num = 0
        self.end_load = True

        self.update_map_list()
        self.update_page()
        self.update_page_text()

    def on_mouse_press(self, x, y, button, modifiers):
        for b in self.buttons:
            b.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for b in self.buttons:
            b.on_mouse_motion(x, y, dx, dy)

    def draw(self):
        for b in self.image_maps:
            drawp(b)
        for b in self.buttons:
            drawp(b)
        for b in self.text_maps:
            b.draw()

        self.text_page.draw()
