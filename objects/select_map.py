class select_map_buttons():

    def mapList(self):
        maps_names = []
        maps_logos = []
        files = os.listdir('maps')

        for file in files:
            try:
                if file.split('.')[1] == 'map':
                    maps_names.append(file.split('.')[0])
                    if os.path.exists('maps/' + file + '/logo.png'):
                        maps_logos.append('maps/' + file + '/logo.png')
                    else:
                        maps_logos.append('img/file_not_found.png')
            except:
                pass
        return maps_names, maps_logos

    def __init__(self):
        self.buttons = []
        self.image_maps = []
        self.text_maps = []

        self.maps_in_page = 3 * 2
        self.page = 1
        self.map_names, self.map_logos = self.mapList()

        i = -1
        for y in range(3):
            for x in range(2):
                i += 1
                if i >= len(self.map_names) or (i >= self.page * self.maps_in_page):
                    break
                self.buttons.append(
                    image_button((x * settings.width/2.8) + settings.width/50 + settings.width/3.8,
                        (settings.height - settings.height/3.5) - (y * settings.height/4.5),
                        'buttons/button_map.png', scale=settings.height/160,
                        center=False, arg='play(\'' + self.map_names[i] + '\')',
                        image_selected='buttons/button_map_selected.png'
                        #text='settings',
                        #text_indent= settings.height//100)
                    )
                )

                self.image_maps.append(
                    image_label(self.map_logos[i],
                        (x * settings.width/2.8) + settings.width/50 + settings.width/3.8 + settings.width/300,
                        (settings.height - settings.height/3.5) - (y * settings.height/4.5) + settings.height/200,
                        scale=settings.height/170, pixel=True, no_image=True
                    )
                )

                self.text_maps.append(
                    text_label(
                        (x * settings.width/2.8) + settings.width/50 + settings.width/3.8 + settings.width/8,
                        (settings.height - settings.height/3.5) - (y * settings.height/4.5) + settings.height/6,
                        self.map_names[i],
                        load_font=True, font='pixel.ttf',
                        size=settings.height//48, anchor_x='left',
                        color = (150, 150, 150, 255)
                    )
                )

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
