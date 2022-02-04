
BUFFERSIZE = 512

def save_dict(dict, name):
    json.dump(dict, open(str(name) + '.json','w'))

def read_dict(name):
    return json.load(open(str(name) + '.json'))

def norm_deg(deg):
    #while True:
    if deg <= 180:
        deg = 180 - (180 + deg)
    elif deg > 180:
        deg = -180 + (deg - 180)
        #else:
        #    break

    return deg

def draw_text_cursor(pos_cursor_x, pos_cursor_y, align='left', text='test', length=settings.width//15):
    if align == 'left':
        draw_line(
            (pos_cursor_x, pos_cursor_y),
            (pos_cursor_x - settings.width//15, pos_cursor_y + settings.height//15)
        )
        draw_line(
            (pos_cursor_x - settings.width//15, pos_cursor_y + settings.height//15),
            (pos_cursor_x - settings.width//15 - length, pos_cursor_y + settings.height//15)
        )

def get_font_size(font, size=14):
    selected_font = pyglet.font.load('font/' + font, size)
    return (selected_font.ascent - selected_font.descent, size)

def PIL_to_pyglet(image_pil, scale=1, anchor_bool = False):
    raw_image = image_pil.tobytes()
    image_pyglet = pyglet.image.ImageData(image_pil.width, image_pil.height, 'RGBA', raw_image, pitch=-image_pil.width * 4)
    if anchor_bool:
        image_pyglet.anchor_x = image_pyglet.width // 2
        image_pyglet.anchor_y = image_pyglet.height // 2
    image_pyglet = pyglet.sprite.Sprite(image_pyglet, settings.width//4, settings.height//2)
    image_pyglet.scale = scale
    return image_pyglet

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def lerp(start, end, a):
    return (1-a) * start + a * end

def draw_line(pos_from, pos_before):
    points = [pos_from[0], pos_from[1], pos_before[0], pos_before[1]]
    pyglet.graphics.draw(2, pyglet.gl.GL_LINE_LOOP,
        ('v2i', points)
    )

def draw_poly(poligon):
    points = []
    for p in poligon.points:
        points.append(int(p[0]))
        points.append(int(p[1]))
    pyglet.graphics.draw(len(poligon.points), pyglet.gl.GL_LINE_LOOP,
        ('v2i', points)
    )

def draw_box_poly(poly):
    points = (
        int(poly.points[0][0]), int(poly.points[0][1]),
        int(poly.points[1][0]), int(poly.points[1][1]),
        int(poly.points[2][0]), int(poly.points[2][1]),
        int(poly.points[3][0]), int(poly.points[3][1])
    )
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
        ('v2i', points)
    )

def drawp(image):
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    image.draw()

#@numba.njit(fastmath = True)
def get_pil_color_mask(image, color=(0, 0, 0, 0)):
    ibw, ibh = image.size
    for y in range(ibh):
        for x in range(ibw):
            if image.getpixel((x, y)) != (0, 0, 0, 0):
                image.putpixel((x, y), color)
    return image

#@numba.njit(fastmath = True)
def get_pil_black_mask(image, alpha=255):
    ibw, ibh = image.size
    for y in range(ibh):
        for x in range(ibw):
            if image.getpixel((x, y)) != (0, 0, 0, 0):
                image.putpixel((x, y), (0, 0, 0, alpha))
    return image

#@numba.njit(fastmath = True)
def del_black_mask(image, image_mask):
    ibw, ibh = image.size
    for y in range(ibh):
        print(y)
        for x in range(ibw):
            if image_mask.getpixel((x, y)) == (0, 0, 0, 0):
                image.putpixel((x, y), (0, 0, 0, 0))
    return image

def PIL_resize_image(input_image_path,
                 size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    resized_image = original_image.resize(size)
    width, height = resized_image.size
    return resized_image

pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
class Sound():
    def __init__(self, loop=False, no_sound=False):
        self.sound_name = ''

        self.no_sound = no_sound

        self.sound = pyglet.media.Player()
        self.sound.volume = settings.sound_volume
        self.sound.loop = loop

    def sound_volume(self, vol):
        self.sound.volume = vol

    def pause(self):
        self.sound.pause()

    def update(self):
        self.sound.volume = settings.sound_volume

    def play(self, music):
        self.sound.next_source()
        self.sound.queue( pyglet.media.load(('' if self.no_sound else 'sound/') + music) )
        self.sound.play()
        self.sound_name = music

sound = Sound()

class timer():
    def __init__(self, delay, func, arg=None):
        self.time = time.perf_counter() + delay
        self.func = func
        self.arg = arg
        self.stop = False

    def update(self):
        if self.time <= time.perf_counter() and not self.stop:
            if self.arg == None:
                self.function()
            else:
                exec(self.arg)
            self.stop = True

class read_key_image():
    def __init__(self, x, y, image, image_selected='', scale=1, font='default.ttf', color_text=(255, 255, 255, 255), text='', text_indent=0, text_input_indent=20, shadow=False, color_shadow=(0, 0, 0, 128)):
        self.x = x
        self.y = y

        self.image = image
        self.image_selected = image_selected
        self.scale = scale

        self.shadow = shadow
        self.color_shadow = color_shadow

        self.image_shadow_obj = PIL_to_pyglet(get_pil_color_mask(Image.open('img/' + self.image).convert("RGBA"), self.color_shadow), scale, False)
        self.image_shadow_obj.x = x - scale
        self.image_shadow_obj.y = y + scale

        self.image_obj = image_label(self.image, x, y, scale=scale, center=False)
        self.image_selected_obj = image_label(self.image_selected, x, y, scale=scale, center=False)

        self.image_shadow_obj = PIL_to_pyglet(get_pil_color_mask(Image.open('img/' + self.image).convert("RGBA"), self.color_shadow), scale, False)
        self.image_shadow_obj.x = x - scale
        self.image_shadow_obj.y = y + scale

        self.key = ''

        self.font = font
        self.color_text = color_text

        self.text = text
        size = self.scale * 5.5
        self.text_button = text_label(self.x + text_indent, self.y + size*1.6, self.text, load_font=True, font=font, size=int(size), anchor_x='left', color=color_text)
        self.text_obj = text_label(x + text_indent + self.text_button.label.content_width + text_input_indent, self.y + size*1.6, self.key, load_font=True, font=font, size=int(size), anchor_x='left', color=color_text)

        self.hover = False
        self.selected = False

        self.image_poligon = collision.Poly(v(x, y),
        [
            v(0, self.image_obj.sprite.height),
            v(self.image_obj.sprite.width, self.image_obj.sprite.height),
            v(self.image_obj.sprite.width, 0),
            v(0, 0)
        ])

        self.cursor_poligon = collision.Poly(v(0, 0),
        [
            v(-1, 1),
            v(1, 1),
            v(-1, -1),
            v(1, -1)
        ])

    def update_key(self, key):
        self.key = key
        self.text_obj.label.text = self.key

    def on_mouse_press(self, x, y, button, modifiers):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.image_poligon, self.cursor_poligon):
            sound.play('upgrade.wav')
            if not self.selected:
                self.selected = True
            else:
                self.selected = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.image_poligon, self.cursor_poligon):
            if not self.hover:
                sound.play('select.wav')
            self.hover = True
        else:
            self.hover = False

    def on_key_press(self, symbol, modifier):
        if self.selected:
            block_simv = [
                'F1',
                'F2',
                'F3',
                'F4',
                'F5',
                'F6',
                'F7',
                'F8',
                'F9',
                'F10',
                'F11',
                'F12',
                'ESCAPE',
                'ENTER',
                'LWINDOWS',
                'RWINDOWS'
            ]
            #print(symbol, chr(symbol), key.symbol_string(symbol))
            if not key.symbol_string(symbol) in block_simv:
                self.update_key(key.symbol_string(symbol))

            self.selected = False

    def draw(self):
        if self.shadow:
            drawp(self.image_shadow_obj)
        if self.hover or self.selected:
            drawp(self.image_selected_obj)
        else:
            drawp(self.image_obj)

        self.text_button.draw()
        self.text_obj.draw()

class slider_image():
    def __init__(self, x, y, image, image_slider, image_selected='', scale=1, shadow=False, color_shadow=(0, 0, 0, 128)):
        self.x = x
        self.y = y

        self.image = image
        self.image_selected = image_selected
        self.image_slider = image_slider

        self.shadow = shadow
        self.color_shadow = color_shadow

        self.image_shadow_obj = PIL_to_pyglet(get_pil_color_mask(Image.open('img/' + self.image).convert("RGBA"), self.color_shadow), scale, False)
        self.image_shadow_obj.x = x - scale
        self.image_shadow_obj.y = y + scale

        self.state = 0

        self.image_obj = image_label(self.image, x, y, scale=scale, center=False)
        self.image_selected_obj = image_label(self.image_selected, x, y, scale=scale, center=False)

        self.image_slider_obj = image_label(self.image_slider, x, y, scale=scale, center=False)

        self.max_width = self.image_obj.sprite.width - self.image_obj.sprite.width/4

        self.image_poligon = collision.Poly(v(x, y),
        [
            v(0, self.image_obj.sprite.height),
            v(self.image_obj.sprite.width, self.image_obj.sprite.height),
            v(self.image_obj.sprite.width, 0),
            v(0, 0)
        ])

        self.cursor_poligon = collision.Poly(v(0, 0),
        [
            v(-1, 1),
            v(1, 1),
            v(-1, -1),
            v(1, -1)
        ])

        self.hover = False

        self.left = self.image_obj.sprite.width/40
        self.right = self.image_obj.sprite.width/8

    def change_state(self, state):
        self.state = state
        self.update_state((self.x + ((self.image_obj.sprite.width - (self.left + self.right)) * state) ) )

    def update_state(self, state):
        if ((state - self.image_slider_obj.sprite.width/2) >= self.left
            and (state - self.image_slider_obj.sprite.width/2) <= self.image_obj.sprite.width - self.right
            ):
            self.image_slider_obj.x = state - self.image_slider_obj.sprite.width/2
            self.image_slider_obj.update_image(True)
            self.state = (1 / (self.image_obj.sprite.width - (self.left + self.right))) * (state - self.x)
            self.state = float("{0:.2f}".format(self.state)) - 0.09

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.image_poligon, self.cursor_poligon):
            if not self.hover:
                sound.play('select.wav')
            self.hover = True
        else:
            self.hover = False

    def on_mouse_press(self, x, y, button, modifiers):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.image_poligon, self.cursor_poligon):
            sound.play('upgrade.wav')
            self.update_state(x)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.image_poligon, self.cursor_poligon):
            self.update_state(x)

    def draw(self):
        if self.shadow:
            drawp(self.image_shadow_obj)

        if self.hover:
            drawp(self.image_selected_obj)
        else:
            drawp(self.image_obj)
        drawp(self.image_slider_obj)

class input_label_image():
    def change_text(self, text):
        self.text = text
        self.text_obj.text = text
        self.text_obj.text_label.label.text = text

    def __init__(self, x, y, image='', image_selected='', scale=1, font='default.ttf', color_text=(255, 255, 255, 255), text='', pre_text='', alpha=255, text_indent=0, text_input_indent=20, shadow=False, color_shadow=(0, 0, 0, 128)):

        self.x = x
        self.y = y
        self.image = image
        self.image_selected = image_selected
        self.scale = scale
        self.font = font
        self.color_text = color_text

        self.text = text
        self.pre_text = pre_text

        self.selected = False
        self.hover = False

        size = self.scale * 5.5
        self.text_button = text_label(self.x + text_indent, self.y + size*1.6, self.text, load_font=True, font=font, size=int(size), anchor_x='left', color=color_text)

        self.shadow = shadow
        self.color_shadow = color_shadow

        self.image_shadow_obj = PIL_to_pyglet(get_pil_color_mask(Image.open('img/' + self.image).convert("RGBA"), self.color_shadow), scale, False)
        self.image_shadow_obj.x = x - scale
        self.image_shadow_obj.y = y + scale

        self.image_obj = image_label(self.image, x, y, scale=scale, center=False)
        self.image_selected_obj = image_label(self.image_selected, x, y, scale=scale, center=False)

        self.text_obj = input_label(
            x + text_indent + self.text_button.label.content_width + text_input_indent, y + self.image_obj.sprite.height/35,
            self.image_obj.sprite.width - (text_indent + self.text_button.label.content_width + text_input_indent), self.image_obj.sprite.height,
            size=int(self.scale * 5.5), font='pixel.ttf', text=pre_text, color_text=color_text,
            color_background=(0, 0, 0, 0), color_background_selected=(0, 0, 0, 0)
        )

        self.image_poligon = collision.Poly(v(x, y),
        [
            v(0, self.image_obj.sprite.height),
            v(self.image_obj.sprite.width, self.image_obj.sprite.height),
            v(self.image_obj.sprite.width, 0),
            v(0, 0)
        ])


        self.cursor_poligon = collision.Poly(v(0, 0),
        [
            v(-1, 1),
            v(1, 1),
            v(-1, -1),
            v(1, -1)
        ])

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.image_poligon, self.cursor_poligon):
            if not self.hover and not self.selected:
                sound.play('select.wav')
            self.hover = True
        else:
            self.hover = False

    def on_mouse_press(self, x, y, button, modifiers):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.image_poligon, self.cursor_poligon):
            engine_settings.on_text_bool = True
            self.selected = True
            self.text_obj.selected = True
            sound.play('upgrade.wav')
            return True
        else:
            self.selected = False
            self.text_obj.selected = False
        return False

    def on_key_press(self, symbol, modifiers):
        self.text_obj.on_key_press(symbol, modifiers)

    def on_text(self, text): # функция для получения символов которые мы вводим с клавиатуры
        self.text_obj.on_text(text)

    def draw(self):
        if self.shadow:
            drawp(self.image_shadow_obj)

        if self.selected or self.hover:
            drawp(self.image_selected_obj)
            #self.image_selected_obj.draw()
        else:
            drawp(self.image_obj)
            #self.image_obj.draw()

        self.text_button.draw()
        self.text_obj.draw()

class input_label():
    def __init__(self, x, y, width, height, text='', size=18, font='default.ttf', color_text=(255, 255, 255, 255), color_background=(255, 255, 255, 255), color_background_selected=(255, 255, 255, 255)):
        self.x = x
        self.y = y
        self.size = size
        self.color_text = color_text
        self.color_background = color_background
        self.color_background_selected = color_background_selected
        self.font = font

        self.symbol_list = '1234567890!@$%^&*()-=_+qwertyuiop[]asdfghjkl;zxcvbnm,.QWERTYUIOPASDFGHJKL:"ZXCVBNM<>? йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'

        self.selected = False
        self.hover = False
        self.text = text

        self.width = width
        self.height = height

        #def __init__(self, x, y, size_x, size_y, color=(255, 255, 255), rotation=0, alpha=255)
        self.background_label = label(
            self.x, self.y,
            self.width, self.height,
            color=(color_background[0], color_background[1], color_background[2]),
            alpha=color_background[3]
        )

        self.background_label_selected = label(
            self.x, self.y,
            self.width, self.height,
            color=(color_background_selected[0], color_background_selected[1], color_background_selected[2]),
            alpha=color_background_selected[3]
        )

        self.text_label = text_label(
            self.x, self.y + self.height/2,
            self.text,
            load_font=True, font=self.font,
            size=self.size, anchor_x='left',
            color = self.color_text
        )

        # полигон для кнопки

        self.poligon = collision.Poly(v(self.x, self.y),
        [
            v(0, self.height),
            v(self.width, self.height),
            v(self.width, 0),
            v(0, 0)
        ])

        self.cursor_poligon = collision.Poly(v(0, 0),
        [
            v(-1, 1),
            v(1, 1),
            v(-1, -1),
            v(1, -1)
        ])

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.poligon, self.cursor_poligon):
            self.hover = True
        else:
            self.hover = False

    def on_mouse_press(self, x, y, button, modifiers):
        #engine_settings.on_mouse_press_bool = True
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.poligon, self.cursor_poligon):
            #engine_settings.on_mouse_press_bool = False
            engine_settings.on_text_bool = True
            self.selected = True
            return True
        else:
            self.selected = False
        return False

    def on_key_press(self, symbol, modifiers):
        if self.selected: # если мы выводим консоль, разрешаем пользователя нажимать на backspace и enter
            if symbol == key.BACKSPACE:
                self.text = self.text[:len(self.text)-1]
                self.text_label.label.text = self.text

            elif symbol == key.ENTER:
                self.selected = False
                engine_settings.on_text_bool = False

    def on_text(self, text): # функция для получения символов которые мы вводим с клавиатуры
        if self.selected:
            try:
                if text in self.symbol_list: # сравниваем символ со списком разрешённых символов, если такого символа нет, то просто не добавляем его в комманду
                    self.text += text
                    self.text_label.label.text = self.text
                    if self.text_label.label.content_width > self.width:
                        self.text = self.text[:len(self.text)-1]
                        self.text_label.label.text = self.text
            except:
                pass

    def draw(self):
        if self.selected or self.hover:
            self.background_label_selected.draw()
        else:
            self.background_label.draw()

        self.text_label.draw()

class text_label(): # класс для прорисовки текста
    def __init__(self, x, y, text, size=18, color=(255, 255, 255, 255), anchor_x='left', anchor_y='center', load_font=False, font='pixel.ttf', shadow=False, color_shadow=(255, 255, 255, 255), shadow_size=20, type_shadow=0, rotation=0, multiline=False):
        if load_font: # использовать ли свой шрифт
            #pyglet.font.add_file('font/' + font)
            self.font = pyglet.font.load('font/' + font, size)
            fnt = ImageFont.truetype('font/' + font, size)

        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.color = color
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

        self.multiline = multiline

        self.rotation = rotation

        self.shadow = shadow
        self.color_shadow = color_shadow
        self.shadow_size = shadow_size

        self.label = pyglet.text.Label(text,
            font_name= (fnt.getname()[0] if (load_font) else font),
            font_size=self.size,
            x=self.x, y=self.y,
            color=self.color,
            multiline=self.multiline,
            anchor_x=self.anchor_x, anchor_y=self.anchor_y) # создаём текст

        self.label_shadow = pyglet.text.Label(text,
            font_name= (fnt.getname()[0] if (load_font) else font),
            font_size=self.shadow_size,
            x=((self.x - self.size/6) if type_shadow == 0 else self.x), y=((self.y + self.size/6) if type_shadow == 0 else self.y),
            color=self.color_shadow,
            multiline=self.multiline,
            anchor_x=self.anchor_x, anchor_y=self.anchor_y) # создаём текст

    def draw(self):
        #if self.rotation != 0:
        #    glRotatef(self.rotation, 0.0, 0.0, 1.0)
        if self.shadow:
            self.label_shadow.draw()
        self.label.draw() # прорисовываем текст
        #if self.rotation != 0:
        #    glRotatef(0, 0.0, 0.0, 1.0)
        #    glLoadIdentity()


class image_label(): # класс для проприсвки картинки
    def update_image(self, sprite_up=False):
        if sprite_up:
            self.sprite = pyglet.sprite.Sprite(self.image, x = self.x, y = self.y)
            self.sprite.visible = self.visible
            self.sprite.opacity = self.alpha
            self.sprite.rotation = self.rotation
        #if self.center:
            #self.image.anchor_x = self.image.width // 2 ##this line is new
            #self.image.anchor_y = self.image.height // 2 ## and this line also
            #self.sprite = pyglet.sprite.Sprite(self.image, x = self.x, y = self.y)
            #self.sprite.anchor_x = self.sprite.width // 2
            #self.sprite.anchor_y = self.sprite.height // 2

        self.sprite.visible = self.visible
        self.sprite.opacity = self.alpha
        self.sprite.rotation = self.rotation
        if self.scale != 1:
            self.sprite.scale = self.scale
        elif (self.size_x != 1) and (self.size_y != 1):
            self.sprite.scale_x = self.size_x
            self.sprite.scale_y = self.size_y

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        if self.pixel:
            texture = self.image.get_texture()
            texture.width = self.sprite.width
            texture.height = self.sprite.height
            if self.center:
                texture.anchor_x = texture.width // 2
                texture.anchor_y = texture.height // 2

    def update_rotation(self, rotation):
        self.rotation = rotation
        self.update_image()
        #print(self.rotation)

    def __init__(self, image, x, y, scale_x = 1, scale_y = 1, scale = 1, visible=True, rotation=0, alpha=255, pixel=False, center=False, black_mask=False, alpha_mask=0, batch=None, group=None, no_image=False, shadow=False, color_shadow=(0, 0, 0, 128)):
        self.x = x
        self.y = y
        self.size_x = scale_y
        self.size_y = scale_y
        self.rotation = rotation
        self.pixel = pixel
        self.scale = scale
        self.visible = visible
        self.alpha = alpha

        self.shadow = shadow
        self.color_shadow = color_shadow

        if self.shadow:
            self.image_shadow_obj = PIL_to_pyglet(get_pil_color_mask(Image.open('img/' + str(image)).convert("RGBA"), self.color_shadow), scale, False)
            self.image_shadow_obj.x = x - scale
            self.image_shadow_obj.y = y + scale

        if black_mask:
            if no_image:
                image = Image.open('img/' + image).convert("RGBA")
            else:
                image = Image.open(image).convert("RGBA")
            image = get_pil_black_mask(image, alpha_mask)
            raw_image = image.tobytes()
            self.image = pyglet.image.ImageData(image.width, image.height, 'RGBA', raw_image, pitch=-image.width * 4)

        else:
            if no_image:
                self.image = pyglet.image.load(image)
            else:
                self.image = pyglet.image.load('img/' + image)
        if center:
            self.image.anchor_x = self.image.width // 2
            self.image.anchor_y = self.image.height // 2

        if batch != None:
            if group != None:
                self.sprite = pyglet.sprite.Sprite(self.image, x = self.x, y = self.y, batch=batch, group=group)
            else:
                self.sprite = pyglet.sprite.Sprite(self.image, x = self.x, y = self.y, batch=batch)
        else:
            self.sprite = pyglet.sprite.Sprite(self.image, x = self.x, y = self.y)

        self.center = center
        self.sprite.visible = self.visible
        self.sprite.opacity = self.alpha
        self.sprite.rotation = self.rotation

        self.update_image()

    def draw(self):
        if self.shadow:
            drawp(self.image_shadow_obj)

        if self.pixel:
            self.image.blit(self.x, self.y)
        else:
            #self.sprite.draw()
            drawp(self.sprite)

class label(): # класс для прорисовки 4х угольника
    def __init__(self, x, y, size_x, size_y, color=(255, 255, 255), rotation=0, alpha=255):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.color = color
        self.rotation = rotation
        self.alpha = alpha

        self.rec = pyglet.shapes.Rectangle(self.x, self.y, self.size_x, self.size_y, color = self.color)
        self.rec.opacity = self.alpha
        self.rec.rotation = self.rotation


    def draw(self):
        self.rec.draw()

class breathing_label(): # класс для прорисовки 4х угольника
    def __init__(self, x, y, size_x, size_y, color=(255, 255, 255), rotation=0, for_from=255, for_before=0, tick=-5, delay=0.03, function=None, arg=None):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.color = color
        self.rotation = rotation

        self.function = function
        self.arg = arg

        self.for_from = for_from
        self.for_before = for_before
        self.tick = tick
        self.i = self.for_from

        self.rec = pyglet.shapes.Rectangle(self.x, self.y, self.size_x, self.size_y, color = self.color)
        self.rec.opacity = self.i
        self.rec.rotation = self.rotation

        self.delay = delay
        self.time = time.perf_counter() + self.delay

        self.stop = False

    def update(self):
        if not self.stop:
            if self.time <= time.perf_counter():
                self.i += self.tick
                self.rec.opacity = self.i
                if ((self.tick > 0) and (self.i >= self.for_before)) or ((self.tick < 0) and (self.i <= self.for_before)):
                    self.stop = True
                    if self.function != None:
                        self.function()
                    elif self.arg != None:
                        exec(self.arg)
                self.time = time.perf_counter() + self.delay
        else:
            self.rec.opacity = self.for_before

    def draw(self):
        self.rec.draw()

class image_flag():
    def __init__(self, x, y, image, image_flag, scale=1, rotation=0, alpha=255, center=False, image_selected_flag=None, image_selected=None, poligon=False, function_bool = False, function=None, arg=None, text=None, text_color=(0, 0, 0, 0), text_indent=0, font='default.ttf', shadow=False, color_shadow=(0, 0, 0, 128)):
        self.x = x
        self.y = y
        self.image = image
        self.image_flag = image_flag
        self.image_selected_flag = image_selected_flag
        self.image_selected = image_selected
        self.alpha = alpha
        self.scale = scale
        self.center = center
        self.rotation = rotation

        self.function_bool = function_bool
        self.function = function
        self.arg = arg

        self.text = text
        self.text_color = text_color
        self.text_indent = text_indent
        self.font = font

        if self.text != None:
            size = self.scale * 5.5
            self.text_label = text_label(
                self.x + text_indent,
                self.y + size * 1.6,
                self.text,
                load_font=True, font=font, size=int(size),
                anchor_x='left', color=text_color
            )

        self.poligon = poligon

        self.selected = False
        self.flag = False

        self.shadow = shadow
        self.color_shadow = color_shadow

        self.image_shadow_obj = PIL_to_pyglet(get_pil_color_mask(Image.open('img/' + self.image).convert("RGBA"), self.color_shadow), scale, False)
        self.image_shadow_obj.x = x - scale
        self.image_shadow_obj.y = y + scale

        self.image_flag_shadow_obj = PIL_to_pyglet(get_pil_color_mask(Image.open('img/' + self.image_flag).convert("RGBA"), self.color_shadow), scale, False)
        self.image_flag_shadow_obj.x = x - scale
        self.image_flag_shadow_obj.y = y + scale

        self.image_obj = image_label(self.image, x, y, scale=scale, alpha=alpha, rotation=rotation, center=center)
        self.image_flag_obj = image_label(self.image_flag, x, y, scale=scale, alpha=alpha, rotation=rotation, center=center)

        if self.image_selected != None:
            self.image_selected_obj = image_label(self.image_selected, x, y, scale=scale, alpha=alpha, rotation=rotation, center=center)
        if self.image_selected_flag != None:
            self.image_selected_flag_obj = image_label(self.image_selected_flag, x, y, scale=scale, alpha=alpha, rotation=rotation, center=center)
        if center:
            self.image_poligon = collision.Poly(v(x, y),
            [
                v(-self.image_obj.sprite.width/2 + self.image_obj.sprite.width//50, -self.image_obj.sprite.height/2 + self.image_obj.sprite.height//50),
                v(self.image_obj.sprite.width/2 - self.image_obj.sprite.width//50, -self.image_obj.sprite.height/2 + self.image_obj.sprite.height//50),
                v(self.image_obj.sprite.width/2 - self.image_obj.sprite.width//50, self.image_obj.sprite.height/2 - self.image_obj.sprite.height//50),
                v(-self.image_obj.sprite.width/2 + self.image_obj.sprite.width//50, self.image_obj.sprite.height/2 - self.image_obj.sprite.height//50)
            ])
        else:
            self.image_poligon = collision.Poly(v(x, y),
            [
                v(0, self.image_obj.sprite.height),
                v(self.image_obj.sprite.width, self.image_obj.sprite.height),
                v(self.image_obj.sprite.width, 0),
                v(0, 0)
            ])

        self.cursor_poligon = collision.Poly(v(0, 0),
        [
            v(-1, 1),
            v(1, 1),
            v(-1, -1),
            v(1, -1)
        ])

    def on_mouse_press(self, x, y, button, modifiers):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.image_poligon, self.cursor_poligon):
            sound.play('upgrade.wav')

            if self.flag:
                self.flag = False
            else:
                self.flag = True

            if self.function_bool:
                if self.arg == None:
                    self.function()
                else:
                    exec(self.arg)


            return True
        return False

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_poligon.pos.x = x
        self.cursor_poligon.pos.y = y
        if collision.collide(self.image_poligon, self.cursor_poligon):
            if not self.selected:
                self.selected = True
                sound.play('select.wav')
        else:
            self.selected = False

    def update_pos(self, x_pol, y_pol, x_im, y_im):
        self.image_poligon.pos.x = x_pol
        self.image_poligon.pos.y = y_pol

        self.image_obj.sprite.x = x_im
        self.image_obj.sprite.y = y_im

        self.image_selected_obj.sprite.x = x_im
        self.image_selected_obj.sprite.y = y_im

        self.image_flag_obj.sprite.x = x_im
        self.image_flag_obj.sprite.y = y_im

        self.image_selected_flag_obj.sprite.x = x_im
        self.image_selected_flag_obj.sprite.y = y_im

    def draw(self):
        if self.shadow and not self.flag:
            drawp(self.image_shadow_obj)
        elif self.shadow and self.flag:
            drawp(self.image_flag_shadow_obj)

        if self.selected and self.flag and self.image_selected_flag != None:
            drawp(self.image_selected_flag_obj)
            #self.image_selected_flag_obj.draw()
        elif not self.selected and self.flag:
            drawp(self.image_flag_obj)
            #self.image_flag_obj.draw()
        elif self.selected and not self.flag and self.image_selected != None:
            drawp(self.image_selected_obj)
            #self.image_selected_obj.draw()
        elif not self.selected and not self.flag:
            drawp(self.image_obj)
            #self.image_obj.draw()

        if self.text != None:
            self.text_label.draw()

        if self.poligon:
            poligon = self.image_poligon
            points = (
                int(poligon.points[0][0]), int(poligon.points[0][1]),
                int(poligon.points[1][0]), int(poligon.points[1][1]),
                int(poligon.points[2][0]), int(poligon.points[2][1]),
                int(poligon.points[3][0]), int(poligon.points[3][1])
            )
            pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
                ('v2i', points)
            )




class image_button():
    def __init__(self, x, y, image, scale=1, rotation=0, alpha=255, center=False, function=None, arg=None, image_selected=None, poligon=False, text=None, text_color=(180, 180, 180, 255), font='pixel.ttf', text_indent=0, shadow=False, color_shadow=(0, 0, 0, 128), use=True):
        self.use = use

        self.x = x
        self.y = y
        self.image = image
        self.image_selected = image_selected
        self.alpha = alpha
        self.scale = scale
        self.center = center
        self.rotation = rotation
        self.function = function

        self.text = text

        if self.text != None:
            size = self.scale * 5.5#settings.height/150 * self.scale
            #print(size)
            self.text = text_label(self.x + text_indent, self.y + size*1.6, self.text, load_font=True, font=font, size=int(size), anchor_x='left', color=text_color)

        self.arg = arg

        self.poligon = poligon

        self.selected = False

        self.shadow = shadow
        self.color_shadow = color_shadow

        self.image_shadow_obj = PIL_to_pyglet(get_pil_color_mask(Image.open('img/' + self.image).convert("RGBA"), self.color_shadow), scale, False)
        self.image_shadow_obj.x = x - scale
        self.image_shadow_obj.y = y + scale

        self.image_obj = image_label(self.image, x, y, scale=scale, alpha=alpha, rotation=rotation, center=center)
        if self.image_selected != None:
            self.image_selected_obj = image_label(self.image_selected, x, y, scale=scale, alpha=alpha, rotation=rotation, center=center)
        if center:
            self.image_poligon = collision.Poly(v(x, y),
            [
                v(-self.image_obj.sprite.width/2 + self.image_obj.sprite.width//50, -self.image_obj.sprite.height/2 + self.image_obj.sprite.height//50),
                v(self.image_obj.sprite.width/2 - self.image_obj.sprite.width//50, -self.image_obj.sprite.height/2 + self.image_obj.sprite.height//50),
                v(self.image_obj.sprite.width/2 - self.image_obj.sprite.width//50, self.image_obj.sprite.height/2 - self.image_obj.sprite.height//50),
                v(-self.image_obj.sprite.width/2 + self.image_obj.sprite.width//50, self.image_obj.sprite.height/2 - self.image_obj.sprite.height//50)
            ])
        else:
            self.image_poligon = collision.Poly(v(x, y),
            [
                v(0, self.image_obj.sprite.height),
                v(self.image_obj.sprite.width, self.image_obj.sprite.height),
                v(self.image_obj.sprite.width, 0),
                v(0, 0)
            ])

        self.cursor_poligon = collision.Poly(v(0, 0),
        [
            v(-1, 1),
            v(1, 1),
            v(-1, -1),
            v(1, -1)
        ])

    def on_mouse_press(self, x, y, button, modifiers):
        if self.use:
            self.cursor_poligon.pos.x = x
            self.cursor_poligon.pos.y = y
            if collision.collide(self.image_poligon, self.cursor_poligon):
                sound.play('upgrade.wav')
                if self.arg == None:
                    self.function()
                else:
                    exec(self.arg)
                return True
            return False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.use:
            self.cursor_poligon.pos.x = x
            self.cursor_poligon.pos.y = y
            if collision.collide(self.image_poligon, self.cursor_poligon):
                if not self.selected:
                    sound.play('select.wav')
                self.selected = True
            else:
                self.selected = False

    def update_pos(self, x_pol, y_pol, x_im, y_im):
        self.image_poligon.pos.x = x_pol
        self.image_poligon.pos.y = y_pol

        self.image_obj.sprite.x = x_im
        self.image_obj.sprite.y = y_im

        self.image_selected_obj.sprite.x = x_im
        self.image_selected_obj.sprite.y = y_im

    def draw(self):
        if self.shadow:
            drawp(self.image_shadow_obj)
        if not self.selected:
            drawp(self.image_obj)
            #self.image_obj.draw()
        elif self.image_selected != None:
            drawp(self.image_selected_obj)
            #self.image_selected_obj.draw()

        if self.text != None:
            self.text.draw()

        if self.poligon:
            poligon = self.image_poligon
            points = (
                int(poligon.points[0][0]), int(poligon.points[0][1]),
                int(poligon.points[1][0]), int(poligon.points[1][1]),
                int(poligon.points[2][0]), int(poligon.points[2][1]),
                int(poligon.points[3][0]), int(poligon.points[3][1])
            )
            pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
                ('v2i', points)
            )

class circle_label():
    def __init__(self, x, y, rad, numPoints=50, size_circle=100, size=3, color=(0, 0, 0, 0)):
        self.verts = []
        self.color_points = []
        self.numPoints = numPoints
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.size_circle = size_circle
        self.circle = None
        self.rad = rad
        self.edit()

    def edit(self, rad=None, x=None, y=None, color=None, size=None, numPoints=50):
        self.rad = rad if (rad != None) else self.rad
        self.x = x if (x != None) else self.x
        self.y = y if (y != None) else self.y
        self.size = size if (size != None) else self.size
        self.numPoints = numPoints if (numPoints != None) else self.numPoints
        self.color = color if (color != None) else self.color

        self.verts = []
        self.color_points = []
        for i in range(self.numPoints):
            angle = math.radians(float(i)/self.numPoints * self.rad)
            x = self.size_circle * math.cos(angle) + self.x
            y = self.size_circle * math.sin(angle) + self.y
            self.verts += [x,y]
            self.color_points += self.color
        #print(self.verts)
        #print(self.color_points)
        self.circle = pyglet.graphics.vertex_list(self.numPoints,
            ('v2f', self.verts),
            ('c4B', self.color_points)
        )

    def draw(self):
        pyglet.gl.glLineWidth(self.size)
        #pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
        pyglet.gl.glEnable (GL_LINE_SMOOTH)
        #pyglet.gl.glColor3f(self.color[0], self.color[1], self.color[2])

        #glEnable(GL_BLEND)
        #glDisable(GL_DEPTH_TEST)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        self.circle.draw(GL_LINE_STRIP)
