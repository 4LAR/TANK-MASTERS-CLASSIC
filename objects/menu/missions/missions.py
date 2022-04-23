class maps_missions_list():
    def __init__(self):
        self.search()

    def search(self):
        print('READ MISSIONS')

        self.missions_names = []
        self.missions_logos = []
        self.missions_dir = []

        files = os.listdir('maps/missions')

        for file in files:
            try:
                if file.split('.')[1] == 'maps':
                    self.missions_dir.append('missions/' + file.split('.')[0])
                    self.missions_names.append(file.split('.')[0])
                    if os.path.exists('maps/missions/' + file + '/logo.png'):
                        self.missions_logos.append('maps/missions/' + file + '/logo.png')
                    else:
                        self.missions_logos.append('img/file_not_found.png')
            except:
                pass
        
        return self.missions_names, self.missions_logos, self.missions_dir

maps_missions_list = maps_missions_list()

class missions():
    def __init__(self):
        
        maps_missions_list.search()

        self.maps_in_page = 3 * 1

        self.x = 0
        self.y = 0
        self.num = 0
        self.end_load = True

        self.update_map_list()
        self.update_page()

    def update_page(self):
        self.buttons = []
        self.image_maps = []
        self.text_maps = []

        self.num = ((self.page - 1) * self.maps_in_page)
        self.x = 1
        self.y = 0

        self.end_load = False

    def update_map_list(self):

        self.page = 1
        self.map_names = maps_missions_list.missions_names
        self.map_logos = maps_missions_list.missions_logos
        self.map_dir = maps_missions_list.missions_dir

        maps = zip(self.map_names, self.map_logos, self.map_dir)
        xs = sorted(maps, key=lambda tup: tup[0])

        self.map_names = [x[0] for x in xs]
        self.map_logos = [x[1] for x in xs]
        self.map_dir = [x[2] for x in xs]

    def append_map(self, i, x, y):
        self.buttons.append(
            image_button((x * settings.width/2.8) + settings.width/50 + settings.width/3.8,
                (settings.height - settings.height/3.5) - (y * settings.height/4.5),
                'buttons/button_map.png', scale=settings.height/160,
                center=False, arg="print('hello world')",
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

    def update(self):
        if not self.end_load:

                self.append_map(self.num, self.x, self.y)

                self.x = 1
                self.y += 1

                self.num += 1

                if self.num >= len(self.map_names) or (self.num >= self.page * self.maps_in_page) or (self.y >= 3):
                    self.end_load = True

    def draw(self):
        for b in self.image_maps:
            drawp(b)
        for b in self.buttons:
            drawp(b)
        for b in self.text_maps:
            b.draw()