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

class head_menu():
    def __init__(self, text='', align_top=True):
        self.align_top = align_top

        self.text = text_label(settings.width/2, settings.height - settings.height/35, text, load_font=True, font='pixel.ttf', size=settings.height//24, anchor_x='center', color = (150, 150, 150, 255))

        image = PIL_resize_image('img/buttons/button_clear.png', (settings.width//2, 16))

        raw_image = image.tobytes()
        if graphics_settings.shadows_buttons and not self.align_top:
            self.image_shadow_obj = PIL_to_pyglet(get_pil_color_mask(image, (0, 0, 0, 128)), settings.height/130, False)
            self.image_shadow_obj.x = -1 - settings.height/130
            self.image_shadow_obj.y = (-settings.height/15) + settings.height/130
            #self.image_shadow_obj.scale = settings.height/130

        self.image = pyglet.image.ImageData(image.width, image.height, 'RGBA', raw_image, pitch=-image.width * 4)
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x = -10, y = (settings.height - settings.height/15) if align_top else (-settings.height/15)
        )
        self.sprite.scale = settings.height/130

    def draw(self):
        if graphics_settings.shadows_buttons and not self.align_top:
            drawp(self.image_shadow_obj)
        drawp(self.sprite)
        self.text.draw()

class back():
    def __init__(self, function=None, arg=None):
        self.function = function
        self.arg = arg

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            if self.arg == None:
                self.function()
            else:
                exec(self.arg)

            return pyglet.event.EVENT_HANDLED


first_breath_menu = True

menu_world = None
menu_wind = None
menu_walls = None
menu_weather = None

game_in_menu_bool = False
def add_game_in_menu():
    global game_in_menu_bool
    global menu_world
    global menu_wind
    global menu_walls
    global menu_weather

    add_display(game_settings)
    if not game_in_menu_bool:
        add_display(graphics_settings)
        menu_world = world('Castle 2')
        add_display(menu_world)
        menu_wind = wind()
        add_display(menu_wind)
        menu_walls = walls()
        add_display(menu_walls)
        menu_weather = weather()
        game_in_menu_bool = True
        add_display(menu_weather)
    else:
        add_display(graphics_settings)
        add_display(menu_world)
        add_display(menu_wind)
        add_display(menu_walls)
        add_display(menu_weather)

def menu():
    show_cursor()
    global first_breath_menu
    clear_display()
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()

    add_display(head_menu())
    add_display(image_button(settings.width - (settings.height/120 * 48), settings.height - settings.height/3, 'buttons/button_clear_left.png', scale=settings.height/120, center=False, arg='select_map(editor=True)', function=play_menu, image_selected='buttons/button_clear_left_selected.png', text='editor', text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons))
    add_display(image_button(settings.width - (settings.height/120 * 48), settings.height - settings.height/2, 'buttons/button_clear_left.png', scale=settings.height/120, center=False, function=settings_menu, image_selected='buttons/button_clear_left_selected.png', text='settings', text_indent=settings.height/10, shadow=graphics_settings.shadows_buttons))
    #add_display(image_button(settings.width - (settings.height/120 * 48), settings.height - settings.height/1.5, 'buttons/button_clear_left.png', scale=settings.height/120, center=False, function=settings_menu, image_selected='buttons/button_clear_left_selected.png', text='settings', text_indent= settings.height//10, shadow=graphics_settings.shadows_buttons))

    add_display(image_button(0, settings.height - settings.height/3, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='single_game()', function=play_menu, image_selected='buttons/button_clear_selected.png', text='single', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))
    add_display(image_button(0, settings.height - settings.height/2, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='select_map(editor=False)', image_selected='buttons/button_clear_selected.png', text='mp local', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))
    add_display(image_button(0, settings.height - settings.height/1.5, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='multiplayer_game()', image_selected='buttons/button_clear_selected.png', text='mp online', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))
    add_display(image_button(settings.width - (settings.height/120 * 48), settings.height/10, 'buttons/button_clear_left.png', scale=settings.height/120, center=False, text='exit', image_selected='buttons/button_clear_left_selected.png', arg='exit()', text_indent= settings.height/6, shadow=graphics_settings.shadows_buttons))
    add_display(head_menu(align_top=False))
    add_display(text_label(settings.width/100, settings.height - settings.height/10, 'TANK MASTERS', load_font=True, font='pixel.ttf', size=settings.height//20, anchor_x='left', color = (150, 150, 150, 255), shadow=True, color_shadow=(20, 20, 20, 122), shadow_size=settings.height//20))
    add_display(text_label(settings.width/5, settings.height - settings.height/6.5, 'CLASSIC', load_font=True, font='pixel.ttf', size=settings.height//20, anchor_x='left', color = (150, 150, 150, 255), shadow=True, color_shadow=(20, 20, 20, 122), shadow_size=settings.height//20))
    add_display(text_label(settings.width/100, settings.height/40, version_engine + ' | ' + version, load_font=True, font='pixel.ttf', size=settings.height//48, anchor_x='left', color = (150, 150, 150, 255)))
    if first_breath_menu:
        add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.01, for_from=255, for_before=0, tick=-5))
        first_breath_menu = False

def create_new_map():
    def create_map():
        editor(get_obj_display('input_label_image').text_obj.text, True)

    show_cursor()
    clear_display()
    add_display(back(arg='select_map(editor=True)'))
    add_display(background_menu())
    add_display(head_menu('editor: new map'))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='select_map(editor=True)', image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))
    add_display(input_label_image(settings.width/25, settings.height - settings.height/4.4, 'buttons/input_world_name.png', 'buttons/input_world_name_selected.png', scale=settings.height/120, color_text=(150, 150, 150, 255), text='map name', pre_text='new world', font='pixel.ttf', text_indent=settings.height/15, text_input_indent=settings.height/10, shadow=graphics_settings.shadows_buttons))

    add_display(image_button(settings.width - (settings.height/120 * 48), settings.height/10, 'buttons/button_clear_left.png', scale=settings.height/120, center=False, function=create_map, image_selected='buttons/button_clear_left_selected.png', text='create', text_indent= settings.height//25, shadow=graphics_settings.shadows_buttons))

    add_display(head_menu(align_top=False))


def select_tank(map_name='test'):
    def play_with_select_tank():
        get_obj_display('select_tank_buttons').save()
        save_settings.save_settings()
        play(
            map_name,
            [
                get_obj_display('select_tank_buttons').buttons_bot[0].flag,
                get_obj_display('select_tank_buttons').buttons_bot[1].flag,
                get_obj_display('select_tank_buttons').buttons_bot[2].flag,
                get_obj_display('select_tank_buttons').buttons_bot[3].flag
            ],
            [
                get_obj_display('select_tank_buttons').buttons[0].flag,
                get_obj_display('select_tank_buttons').buttons[1].flag,
                get_obj_display('select_tank_buttons').buttons[2].flag,
                get_obj_display('select_tank_buttons').buttons[3].flag
            ],
            get_obj_display('select_tank_buttons').tank_settings
        )

    show_cursor()
    clear_display()
    add_display(back(arg='get_obj_display(\'select_tank_buttons\').save(); save_settings.save_settings(); select_map()'))
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()
    add_display(head_menu('select machine'))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='get_obj_display(\'select_tank_buttons\').save(); save_settings.save_settings(); select_map()', image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))
    add_display(image_button(settings.width / 3, settings.height/10, 'buttons/button_clear_full.png', scale=settings.height/120, center=False, arg='get_obj_display(\'select_tank_buttons\').reset()', image_selected='buttons/button_clear_full_selected.png', text='reset', text_indent= settings.height/9, shadow=graphics_settings.shadows_buttons))
    add_display(image_button(settings.width - (settings.height/120 * 48), settings.height/10, 'buttons/button_clear_left.png', scale=settings.height/120, center=False, function=play_with_select_tank, image_selected='buttons/button_clear_left_selected.png', text='start', text_indent= settings.height//25, shadow=graphics_settings.shadows_buttons))

    add_display(select_tank_buttons())

    add_display(head_menu(align_top=False))

def game_setup():
    show_cursor()
    clear_display()
    add_display(back(function=select_map))
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()
    add_display(head_menu('game setup'))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='global game_in_menu_bool; get_obj_display(\'game_setup_flags\').save_settings(); game_in_menu_bool = False; select_map()', image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))
    '''image_button(
        settings.width - (settings.height/120 * 48), settings.height/10,
        'buttons/button_clear_left.png', scale=settings.height/120,
        center=False, arg='get_obj_display("game_settings_page").save_settings(); menu()',
        image_selected='buttons/button_clear_left_selected.png',
        text='save', text_indent= settings.height/20, shadow=graphics_settings.shadows_buttons
    )'''

    add_display(game_setup_flags())
    add_display(image_button(settings.width / 3, settings.height/10, 'buttons/button_clear_full.png', scale=settings.height/120, center=False, arg='get_obj_display(\'game_setup_flags\').reset()', image_selected='buttons/button_clear_full_selected.png', text='reset', text_indent= settings.height/9, shadow=graphics_settings.shadows_buttons))


    add_display(head_menu(align_top=False))

def select_map(editor=False):
    show_cursor()
    clear_display()
    add_display(back(function=menu))
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()
    add_display(head_menu(('editor: select map') if editor else ('select map')))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=menu, image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))
    if editor:
        add_display(image_button(settings.width - (settings.height/120 * 48), settings.height/10, 'buttons/button_clear_left.png', scale=settings.height/120, center=False, function=create_new_map, image_selected='buttons/button_clear_left_selected.png', text='create map', text_indent= settings.height//25, shadow=graphics_settings.shadows_buttons))

    add_display(image_button(settings.width/3 + settings.width/3.55, settings.height/10, 'buttons/button_right_page.png', image_selected='buttons/button_right_page_selected.png', scale=settings.height/120, center=False, arg='get_obj_display(\'select_map_buttons\').page_up()', shadow=graphics_settings.shadows_buttons))
    add_display(image_label('buttons/page_indicator.png',
        settings.width/2.5, settings.height/10,
        scale=settings.height/120, pixel=True, shadow=graphics_settings.shadows_buttons
    ))
    add_display(image_button(settings.width/3, settings.height/10, 'buttons/button_left_page.png', image_selected='buttons/button_left_page_selected.png', scale=settings.height/120, center=False, arg='get_obj_display(\'select_map_buttons\').page_down()', shadow=graphics_settings.shadows_buttons))


    '''add_display(image_label('select_maps_panel_flags.png',
        0, (settings.height - settings.height/3.5) - (2 * settings.height/4.5),
        scale=settings.height/120, pixel=True
    ))'''

    if not editor:
        add_display(image_button(0, settings.height/3.5, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=game_setup, image_selected='buttons/button_clear_selected.png', text='game setup', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))

    '''add_display(
        image_flag(
            0,
            (settings.height - settings.height/3.5),
            image='menu/select tank/flag.png',
            image_flag='menu/select tank/flag_selected.png',
            image_selected_flag='menu/select tank/flag_hover_selected.png',
            image_selected='menu/select tank/flag_hover.png',
            scale=settings.height/160,

        )
    )'''

    add_display(select_map_buttons(editor))
    add_display(head_menu(align_top=False))

def play_menu():
    show_cursor()
    clear_display()
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=menu, image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))

    add_display(head_menu(align_top=False))

def settings_menu():
    global game_settings_page

    show_cursor()
    clear_display()
    add_display(back(function=menu))
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()
    add_display(head_menu('settings'))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, function=menu, image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))

    add_display(game_settings_page())

    add_display(head_menu(align_top=False))
