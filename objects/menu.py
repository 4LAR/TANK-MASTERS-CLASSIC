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
        drawp(self.image_background)

class main_menu_buttons():
    pass

def menu():
    clear_display()
    add_display(background_menu())
    add_display(image_button(0, settings.height - settings.height/3, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=play, image_selected='buttons/button_clear_selected.png', text='play', text_indent= settings.height//100))
    add_display(image_button(0, settings.height - settings.height/2, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=exit, image_selected='buttons/button_clear_selected.png', text='editor', text_indent= settings.height//100))
    add_display(image_button(0, settings.height - settings.height/1.5, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=exit, image_selected='buttons/button_clear_selected.png', text='settings', text_indent= settings.height//100))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=exit, image_selected='buttons/button_clear_selected.png', text='exit', text_indent= settings.height//100))
    add_display(text_label(settings.width/100, settings.height/20, version_engine + ' | TANK MASTERS: CLASSIC (0.0.1)', load_font=True, font='pixel.ttf', size=settings.height//48, anchor_x='left', color = (20, 20, 20, 255)))
    add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.01, for_from=255, for_before=0, tick=-5))
