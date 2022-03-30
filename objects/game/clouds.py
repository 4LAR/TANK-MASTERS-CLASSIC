class clouds():

    def get_speed_by_deg_sp(self, deg, speed):
        #deg += 90
        if deg < 0:
            deg = 180 + (180 + deg)
        if deg >= 360:
            deg = 0
        a = speed/math.sin(math.radians(90))
        x = a * math.sin(math.radians(deg))
        y = a * math.sin(math.radians(180 - 90 - deg))
        return x, y

    def __init__(self):
        try:

            self.deg = 45

            self.image_cloud = Image.new('RGBA', (settings.width*2, settings.height*2))

            self.speed = settings.height/800
            self.speed_x, self.speed_y = self.get_speed_by_deg_sp(self.deg, self.speed)

            self.delay = 1/(settings.fps/1.6)
            self.time = time.perf_counter() + self.delay

            self.max_cloud = 20

            for _ in range(self.max_cloud):
                x = random.randrange(0, settings.width*2)
                y = random.randrange(0, settings.height*2)
                image = Image.new('RGBA', (random.randrange(settings.width//12, settings.width//6), random.randrange(settings.height//12, settings.height//6)))
                image.putalpha(48)
                self.image_cloud.paste(image,
                    (x, y)
                )

            raw_image = self.image_cloud.tobytes()

            self.cloud_arr = []
            for i in range(3):
                image_cloud = pyglet.image.ImageData(self.image_cloud.width, self.image_cloud.height, 'RGBA', raw_image, pitch=-self.image_cloud.width * 4)
                image_cloud.anchor_x = image_cloud.width // 2
                image_cloud.anchor_y = image_cloud.height // 2
                self.cloud_arr.append([pyglet.sprite.Sprite(image_cloud, settings.width//4, settings.height//2), (i * settings.width),( i * settings.height)])
                #self.cloud_arr[i][0].rotation = self.deg
                self.cloud_arr[i][0].x = self.cloud_arr[i][1]
                self.cloud_arr[i][0].y = self.cloud_arr[i][2]

        except:
            print("FATAL ERROR: " + str(traceback.format_exc()))

    def update(self):
        if graphics_settings.draw_clouds and not get_obj_display('game_settings').pause:
            if self.time <= time.perf_counter():
                for i in range(len(self.cloud_arr)):
                    self.cloud_arr[i][1] -= self.speed_x
                    self.cloud_arr[i][2] -= self.speed_y
                    if (self.cloud_arr[i][1]) < -(settings.width) or (self.cloud_arr[i][2]) < -(settings.height):
                        self.cloud_arr[i][1] = int(settings.width*1.2)
                        self.cloud_arr[i][2] = int(settings.width*1.2)

                    self.cloud_arr[i][0].x = self.cloud_arr[i][1]
                    self.cloud_arr[i][0].y = self.cloud_arr[i][2]

                self.time = time.perf_counter() + self.delay

    def draw(self):
        if graphics_settings.draw_clouds:
            for cloud in self.cloud_arr:
                cloud[0].x += get_obj_display('world').map_offs[0]
                cloud[0].y += get_obj_display('world').map_offs[1]
                drawp(cloud[0])
                cloud[0].x -= get_obj_display('world').map_offs[0]
                cloud[0].y -= get_obj_display('world').map_offs[1]
