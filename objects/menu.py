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

class head_menu():
    def __init__(self, text):

        self.text = text_label(settings.width/2, settings.height - settings.height/35, text, load_font=True, font='pixel.ttf', size=settings.height//24, anchor_x='center', color = (150, 150, 150, 255))

        image = PIL_resize_image('img/buttons/button_clear.png', (settings.width//2, 16))
        raw_image = image.tobytes()
        self.image = pyglet.image.ImageData(image.width, image.height, 'RGBA', raw_image, pitch=-image.width * 4)
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x = 0, y = settings.height - settings.height/15
        )
        self.sprite.scale = settings.height/130

    def draw(self):
        drawp(self.sprite)
        self.text.draw()

first_breath_menu = True

def menu():
    global first_breath_menu
    clear_display()
    add_display(background_menu())
    add_display(image_button(0, settings.height - settings.height/3, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='select_map(editor=True)', function=play_menu, image_selected='buttons/button_clear_selected.png', text='play', text_indent= settings.height//100))
    add_display(image_button(0, settings.height - settings.height/2, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='select_map(editor=True)', image_selected='buttons/button_clear_selected.png', text='editor', text_indent= settings.height//100))
    add_display(image_button(0, settings.height - settings.height/1.5, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=settings_menu, image_selected='buttons/button_clear_selected.png', text='settings', text_indent= settings.height//100))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=exit, image_selected='buttons/button_clear_selected.png', text='exit', text_indent= settings.height//100))
    add_display(text_label(settings.width/100, settings.height/20, version_engine + ' | ' + version, load_font=True, font='pixel.ttf', size=settings.height//48, anchor_x='left', color = (20, 20, 20, 255)))
    if first_breath_menu:
        add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.01, for_from=255, for_before=0, tick=-5))
        first_breath_menu = False

def select_map(editor=False):
    clear_display()
    add_display(background_menu())
    add_display(head_menu('select map'))

    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=menu, image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100))
    add_display(select_map_buttons())
    add_display(image_label('buttons/page_indicator.png',
        settings.width/2.5, settings.height/10,
        scale=settings.height/120, pixel=True
    ))
    add_display(text_label(settings.width/2.3, settings.height/6, 'page: 1/2', load_font=True, font='pixel.ttf', size=settings.height//24, anchor_x='left', color = (150, 150, 150, 255)))
    add_display(image_button(settings.width/3, settings.height/10, 'buttons/button_left_page.png', image_selected='buttons/button_left_page_selected.png', scale=settings.height/120, center=False, function=menu))
    add_display(image_button(settings.width/3 + settings.width/3.5, settings.height/10, 'buttons/button_right_page.png', image_selected='buttons/button_right_page_selected.png', scale=settings.height/120, center=False, function=menu))


def play_menu():
    clear_display()
    add_display(background_menu())
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=menu, image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100))

def settings_menu():
    clear_display()
    add_display(background_menu())
    add_display(head_menu('settings'))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=menu, image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100))
