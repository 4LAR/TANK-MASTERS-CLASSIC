class smoke():
    def __init__(self):
        self.smoke_list = []

        self.smoke_delay = 0.1

        self.smoke_images = []
        self.max_current_smoke = 11
        for i in range(self.max_current_smoke):
            self.smoke_images.append(
                image_label(
                'world/smoke/big_smoke_' + str(i) + '.png',
                settings.width//2, settings.height//2, scale=get_obj_display('world').scale,
                pixel=False, center=True, rotation=0
            )
        )

    def add_smoke(self, x, y, current=0):
        self.smoke_list.append([x, y, current, time.perf_counter() + self.smoke_delay])

    def update(self):
        if not get_obj_display('game_settings').pause and get_obj_display('graphics_settings').draw_smoke:
            for i in range(len(self.smoke_list)-1, -1, -1):

                if self.smoke_list[i][3] <= time.perf_counter():
                    self.smoke_list[i][2] += 1
                    self.smoke_list[i][3] = time.perf_counter() + self.smoke_delay

                if self.smoke_list[i][2] >= self.max_current_smoke:
                    self.smoke_list.pop(i)

    def draw(self):
        if get_obj_display('graphics_settings').draw_smoke:
            for i in range(len(self.smoke_list)):
                self.smoke_images[self.smoke_list[i][2]].sprite.x = self.smoke_list[i][0] + get_obj_display('world').map_offs[0]
                self.smoke_images[self.smoke_list[i][2]].sprite.y = self.smoke_list[i][1] + get_obj_display('world').map_offs[1]
                drawp(self.smoke_images[self.smoke_list[i][2]])
