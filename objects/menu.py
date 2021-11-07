class background_menu():
    def __init__(self):
        size = 16
        resize = (size, size)
        width = 16
        height = 9

        background_image = Image.open('img/background.png').resize(resize, Image.NEAREST).convert("RGBA")
        self.temp_image_background = Image.new('RGBA', (width * size, height * size))
        for y in range(height):
            for x in range(width):
                self.temp_image_background.paste(background_image, (x * size, y * size))

        raw_image = self.temp_image_background.tobytes()
        self.image_background = pyglet.image.ImageData(self.temp_image_background.width, self.temp_image_background.height, 'RGBA', raw_image, pitch=-self.temp_image_background.width * 4)
        self.image_background = pyglet.sprite.Sprite(self.image_background, 0, 0)
        self.image_background.scale = settings.height / 64

    def draw(self):
        drawp(self.image_background)

class main_menu_buttons():
    pass

def menu():
    clear_display()
    add_display(background_menu())
