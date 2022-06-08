class weather():

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

            self.image_rain = Image.new('RGBA', (settings.width*2, settings.height*2))
            image = Image.open('assets/img/world/rain/' +
                ('rain' if not get_obj_display('game_settings').snow else 'snow')
             + '.png').resize(((settings.height//50)//8, (settings.height//50)), Image.NEAREST).convert("RGBA")

            self.speed = settings.height/80 if not get_obj_display('game_settings').snow else settings.height/200
            self.speed_x, self.speed_y = self.get_speed_by_deg_sp(self.deg, self.speed)

            self.delay = 1/(settings.fps/1.6)
            self.time = time.perf_counter() + self.delay

            self.max_rain = 1000 if not get_obj_display('game_settings').snow else 10000

            for _ in range(self.max_rain):
                x = random.randrange(0, settings.width*2)
                y = random.randrange(0, settings.height*2)
                self.image_rain.paste(image,
                    (x, y)
                )

            raw_image = self.image_rain.tobytes()

            self.rain_arr = []
            for i in range(3):
                image_rain = pyglet.image.ImageData(self.image_rain.width, self.image_rain.height, 'RGBA', raw_image, pitch=-self.image_rain.width * 4)
                image_rain.anchor_x = image_rain.width // 2
                image_rain.anchor_y = image_rain.height // 2
                self.rain_arr.append([pyglet.sprite.Sprite(image_rain, settings.width//4, settings.height//2), (i * settings.width),( i * settings.height)])
                self.rain_arr[i][0].rotation = self.deg
                self.rain_arr[i][0].x = self.rain_arr[i][1]
                self.rain_arr[i][0].y = self.rain_arr[i][2]

        except:
            print("FATAL ERROR: " + str(traceback.format_exc()))

    def update(self):
        if get_obj_display('game_settings').rain and not get_obj_display('game_settings').pause:
            if self.time <= time.perf_counter():
                for i in range(len(self.rain_arr)):
                    self.rain_arr[i][1] -= self.speed_x
                    self.rain_arr[i][2] -= self.speed_y
                    if (self.rain_arr[i][1]) < -(settings.width) or (self.rain_arr[i][2]) < -(settings.height):
                        self.rain_arr[i][1] = int(settings.width*1.2)
                        self.rain_arr[i][2] = int(settings.width*1.2)

                    self.rain_arr[i][0].x = self.rain_arr[i][1]
                    self.rain_arr[i][0].y = self.rain_arr[i][2]

                self.time = time.perf_counter() + self.delay

    def draw(self):
        if get_obj_display('game_settings').rain:
            for rain in self.rain_arr:
                drawp(rain[0])
