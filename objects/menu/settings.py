class game_settings_page():
    def select_page(self, id):
        self.settings_page_buttons[id].flag = True
        self.page = id
        for i in range(len(self.settings_page_buttons)):
            if i != id:
                self.settings_page_buttons[i].flag = False

    def select_screen(self, id):
        self.settings_buttons[1][id].flag = True
        for i in range(len(self.settings_buttons[1])):
            if i != id:
                self.settings_buttons[1][i].flag = False

    def select_player(self, id):
        players = ['main', 'P1', 'P2', 'P3', 'P4']
        buttons = ['up', 'down', 'left', 'right', 'shoot_a']
        for i in range(5):
            self.KEY_BINDS[players[self.selected_player]][buttons[i]] = self.settings_buttons[4][5 + i].key
            self.settings_buttons[4][5 + i].update_key(self.KEY_BINDS[players[id]][buttons[i]])

        self.selected_player = id
        self.settings_buttons[4][id].flag = True
        for i in range(5):
            if i != id:
                self.settings_buttons[4][i].flag = False

    def read_settings(self):
        # game
        self.settings_buttons[0][0].change_text(str(user_game_settings.name))

        self.settings_buttons[0][1].flag = settings.show_fps
        self.settings_buttons[0][2].flag = settings.console

        self.settings_buttons[0][3].flag = user_game_settings.draw_logo

        # display
        self.settings_buttons[1][settings.full_screen].flag = True

        self.settings_buttons[1][3].change_text(str(settings.width))
        self.settings_buttons[1][4].change_text(str(settings.height))

        # sound
        self.settings_buttons[2][0].change_state(settings.sound_volume * 8)

        # graphics
        self.settings_buttons[3][0].flag = graphics_settings.draw_leaf
        self.settings_buttons[3][1].flag = graphics_settings.draw_traces
        self.settings_buttons[3][2].flag = graphics_settings.draw_shadows
        self.settings_buttons[3][3].flag = graphics_settings.draw_smoke

        self.settings_buttons[3][4].flag = graphics_settings.game_in_menu
        self.settings_buttons[3][5].flag = graphics_settings.paralax_in_menu

        self.settings_buttons[3][6].flag = graphics_settings.shadows_buttons

        #settings.save_settings()

    def save_settings(self):

        reboot_bool = False

        # 0 - game in menu
        # 1 - draw_traces
        # 2 - draw shadows
        # 3 - draw smoke
        # 4 - draw leaf

        # game
        user_game_settings.name = self.settings_buttons[0][0].text_obj.text_label.label.text

        settings.show_fps = self.settings_buttons[0][1].flag
        settings.console = self.settings_buttons[0][2].flag

        user_game_settings.draw_logo = self.settings_buttons[0][3].flag

        # display
        if self.settings_buttons[1][0].flag:
            full_screen = 0
        elif self.settings_buttons[1][1].flag:
            full_screen = 1
        elif self.settings_buttons[1][2].flag:
            full_screen = 2

        width = int(self.settings_buttons[1][3].text_obj.text_label.label.text)
        height = int(self.settings_buttons[1][4].text_obj.text_label.label.text)

        if (full_screen != settings.full_screen
        or width != settings.width
        or height != settings.height):
            reboot_bool = True

            settings.full_screen = full_screen
            settings.width = width
            settings.height = height


        # sound
        settings.sound_volume = self.settings_buttons[2][0].state / 8
        sound.update()

        # graphics
        graphics_settings.draw_leaf = self.settings_buttons[3][0].flag
        graphics_settings.draw_traces = self.settings_buttons[3][1].flag
        graphics_settings.draw_shadows = self.settings_buttons[3][2].flag
        graphics_settings.draw_smoke = self.settings_buttons[3][3].flag

        graphics_settings.game_in_menu = self.settings_buttons[3][4].flag
        graphics_settings.paralax_in_menu = self.settings_buttons[3][5].flag

        graphics_settings.shadows_buttons = self.settings_buttons[3][6].flag

        save_settings.save_settings()
        settings.save_settings()

        # keyboard
        global KEY_BINDS
        players = ['main', 'P1', 'P2', 'P3', 'P4']
        buttons = ['up', 'down', 'left', 'right', 'shoot_a']
        for i in range(5):
            self.KEY_BINDS[players[self.selected_player]][buttons[i]] = self.settings_buttons[4][5 + i].key
        KEY_BINDS = self.KEY_BINDS
        save_dict(KEY_BINDS, 'KEY_BINDS')

        if reboot_bool:
            #reboot()
            change_window_settings()
            #pass

    def __init__(self):

        self.save_settings_button = image_button(
            settings.width - (settings.height/120 * 48), settings.height/10,
            'buttons/button_clear_left.png', scale=settings.height/120,
            center=False, arg='get_obj_display("game_settings_page").save_settings(); global game_in_menu_bool; game_in_menu_bool=False; menu()',
            image_selected='buttons/button_clear_left_selected.png',
            text='save', text_indent= settings.height/20, shadow=graphics_settings.shadows_buttons
        )


        self.page = 0
        # 0 - geme
        # 1 - display
        # 2 - sound
        # 3 - graphics
        # 4 - keyboard

        self.selected_player = 0
        # 0 - main
        # 1 - P1
        # 2 - P2
        # 3 - P3
        # 4 - P4

        self.KEY_BINDS = KEY_BINDS

        self.settings_page_buttons = []
        self.settings_page_buttons_text = []

        buttons_distance = settings.width/5.4

        # game
        self.settings_page_buttons.append(
            image_flag(
                0,
                settings.height - settings.height/6,
                image='buttons/button_clear_full_kv.png',
                image_flag='buttons/button_clear_full_kv_flag.png',
                image_selected_flag='buttons/button_clear_full_kv_flag_selected.png',
                image_selected='buttons/button_clear_full_kv_selected.png',
                scale=settings.height/160,
                function_bool = True,
                arg='get_obj_display("game_settings_page").select_page(0)'

            )
        )

        self.settings_page_buttons_text.append(
            text_label(
                settings.width/20,
                settings.height - settings.height/6 + settings.height/50,
                'game',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )

        self.settings_page_buttons[0].flag = True

        # display
        self.settings_page_buttons.append(
            image_flag(
                buttons_distance,
                settings.height - settings.height/6,
                image='buttons/button_clear_full_kv.png',
                image_flag='buttons/button_clear_full_kv_flag.png',
                image_selected_flag='buttons/button_clear_full_kv_flag_selected.png',
                image_selected='buttons/button_clear_full_kv_selected.png',
                scale=settings.height/160,
                function_bool = True,
                arg='get_obj_display("game_settings_page").select_page(1)'

            )
        )

        self.settings_page_buttons_text.append(
            text_label(
                buttons_distance + settings.width/30,
                settings.height - settings.height/6 + settings.height/50,
                'display',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )

        # sound
        self.settings_page_buttons.append(
            image_flag(
                buttons_distance * 2,
                settings.height - settings.height/6,
                image='buttons/button_clear_full_kv.png',
                image_flag='buttons/button_clear_full_kv_flag.png',
                image_selected_flag='buttons/button_clear_full_kv_flag_selected.png',
                image_selected='buttons/button_clear_full_kv_selected.png',
                scale=settings.height/160,
                function_bool = True,
                arg='get_obj_display("game_settings_page").select_page(2)'
            )
        )

        self.settings_page_buttons_text.append(
            text_label(
                buttons_distance * 2 + settings.width/20,
                settings.height - settings.height/6 + settings.height/50,
                'sound',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )

        # graphics
        self.settings_page_buttons.append(
            image_flag(
                buttons_distance * 3,
                settings.height - settings.height/6,
                image='buttons/button_clear_full_kv.png',
                image_flag='buttons/button_clear_full_kv_flag.png',
                image_selected_flag='buttons/button_clear_full_kv_flag_selected.png',
                image_selected='buttons/button_clear_full_kv_selected.png',
                scale=settings.height/160,
                function_bool = True,
                arg='get_obj_display("game_settings_page").select_page(3)'
            )
        )

        self.settings_page_buttons_text.append(
            text_label(
                buttons_distance * 3 + settings.width/40,
                settings.height - settings.height/6 + settings.height/50,
                'graphics',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )

        # keyboard
        self.settings_page_buttons.append(
            image_flag(
                buttons_distance * 4,
                settings.height - settings.height/6,
                image='buttons/button_clear_full_kv.png',
                image_flag='buttons/button_clear_full_kv_flag.png',
                image_selected_flag='buttons/button_clear_full_kv_flag_selected.png',
                image_selected='buttons/button_clear_full_kv_selected.png',
                scale=settings.height/160,
                function_bool = True,
                arg='get_obj_display("game_settings_page").select_page(4)'
            )
        )

        self.settings_page_buttons_text.append(
            text_label(
                buttons_distance * 4 + settings.width/40,
                settings.height - settings.height/6 + settings.height/50,
                'keyboard',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )

        self.settings_buttons = []

        # game
        self.settings_buttons.append([])

        # left
        self.settings_buttons[0].append(
            input_label_image(
                settings.width/100,
                settings.height - settings.height/3.5 - (settings.height/8) * 0,
                'buttons/button_clear_2_reverse.png', 'buttons/button_clear_selected_2_reverse.png',
                scale=settings.height/160, color_text=(150, 150, 150, 255),
                text='name', pre_text='PLAYER', font='pixel.ttf',
                text_indent=settings.height/12, text_input_indent=settings.height/6, shadow=graphics_settings.shadows_buttons
            )
        )

        # right
        self.settings_buttons[0].append(
            image_flag(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/3.5 - (settings.height/8) * 0,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='draw fps',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        self.settings_buttons[0].append(
            image_flag(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/3.5 - (settings.height/8) * 1,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='console (F1)',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        self.settings_buttons[0].append(
            image_flag(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/3.5 - (settings.height/8) * 2,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='draw logo',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        # display
        self.settings_buttons.append([])

        # left
        self.settings_buttons[1].append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/3.5 - (settings.height/8) * 0,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='windowed',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8,

                function_bool = True,
                arg='get_obj_display("game_settings_page").select_screen(0)', shadow=graphics_settings.shadows_buttons

            )
        )
        self.settings_buttons[1].append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/3.5 - (settings.height/8) * 1,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='windowed no frames',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8,

                function_bool = True,
                arg='get_obj_display("game_settings_page").select_screen(1)', shadow=graphics_settings.shadows_buttons

            )
        )
        self.settings_buttons[1].append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/3.5 - (settings.height/8) * 2,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='Full Screen',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8,

                function_bool = True,
                arg='get_obj_display("game_settings_page").select_screen(2)', shadow=graphics_settings.shadows_buttons

            )
        )

        # right
        self.settings_buttons[1].append(
            input_label_image(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/2.5 - (settings.height/8) * 0,
                'buttons/button_clear_2_reverse.png', 'buttons/button_clear_selected_2_reverse.png',
                scale=settings.height/160, color_text=(150, 150, 150, 255),
                text='width', pre_text='1600', font='pixel.ttf',
                text_indent=settings.height/12, text_input_indent=settings.height/6, shadow=graphics_settings.shadows_buttons
            )
        )

        self.settings_buttons[1].append(
            input_label_image(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/2.5 - (settings.height/8) * 1,
                'buttons/button_clear_2_reverse.png', 'buttons/button_clear_selected_2_reverse.png',
                scale=settings.height/160, color_text=(150, 150, 150, 255),
                text='height', pre_text='900', font='pixel.ttf',
                text_indent=settings.height/12, text_input_indent=settings.height/6, shadow=graphics_settings.shadows_buttons
            )
        )

        # sound
        self.settings_buttons.append([])
        #add_display(slider_image(300, 300, 'buttons/slider_medium/input_slider.png', 'buttons/slider_medium/slider.png', 'buttons/slider_medium/input_slider_hover.png',scale=settings.height/120, shadow=graphics_settings.shadows_buttons))
        self.settings_buttons[2].append(
            slider_image(
                    settings.width/100,
                    settings.height - settings.height/3.5 - (settings.height/8) * 1,
                    'buttons/slider_medium/input_slider.png',
                    'buttons/slider_medium/slider.png',
                    'buttons/slider_medium/input_slider_hover.png',
                    scale=settings.height/160, shadow=graphics_settings.shadows_buttons
                )
        )

        self.settings_buttons[2].append(
            slider_image(
                    settings.width/100,
                    settings.height - settings.height/3.5 - (settings.height/8) * 2,
                    'buttons/slider_medium/input_slider.png',
                    'buttons/slider_medium/slider.png',
                    'buttons/slider_medium/input_slider_hover.png',
                    scale=settings.height/160, shadow=graphics_settings.shadows_buttons
                )
        )

        self.settings_buttons[2].append(
            slider_image(
                    settings.width/100,
                    settings.height - settings.height/3.5 - (settings.height/8) * 3,
                    'buttons/slider_medium/input_slider.png',
                    'buttons/slider_medium/slider.png',
                    'buttons/slider_medium/input_slider_hover.png',
                    scale=settings.height/160, shadow=graphics_settings.shadows_buttons
                )
        )

        # graphics
        self.settings_buttons.append([])

        # left page
        self.settings_buttons[3].append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/3.5,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='draw leaf',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        self.settings_buttons[3].append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/3.5 - (settings.height/8) * 1,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='draw traces',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        self.settings_buttons[3].append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/3.5 - (settings.height/8) * 2,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='draw shadows',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        self.settings_buttons[3].append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/3.5 - (settings.height/8) * 3,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='draw smoke',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        # right page
        self.settings_buttons[3].append(
            image_flag(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/3.5 - (settings.height/8) * 0,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='game in menu',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        self.settings_buttons[3].append(
            image_flag(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/3.5 - (settings.height/8) * 1,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='paralax in menu',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        self.settings_buttons[3].append(
            image_flag(
                settings.width/100 + settings.width/2,
                settings.height - settings.height/3.5 - (settings.height/8) * 2,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='buttons shadow',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8, shadow=graphics_settings.shadows_buttons

            )
        )

        # keyboard
        self.settings_buttons.append([])
        players = ['main', 'P1', 'P2', 'P3', 'P4']
        for i in range(5):
            self.settings_buttons[4].append(
                image_flag(
                    buttons_distance * i,
                    settings.height - settings.height/6 - settings.height/10,
                    image='buttons/button_clear_full_kv.png',
                    image_flag='buttons/button_clear_full_kv_flag.png',
                    image_selected_flag='buttons/button_clear_full_kv_flag_selected.png',
                    image_selected='buttons/button_clear_full_kv_selected.png',
                    scale=settings.height/160,
                    function_bool = True,
                    arg='get_obj_display("game_settings_page").select_player(' + str(i) + ')',

                    text=players[i],
                    text_color = (150, 150, 150, 255),
                    font='pixel.ttf',
                    text_indent=settings.height/10 if i == 0 else settings.height/8

                )
            )


        # inputs
        inputs_pos = [
            [settings.width/100, settings.height - settings.height/3.5 - (settings.height/8) * 1],
            [settings.width/100, settings.height - settings.height/3.5 - (settings.height/8) * 2],
            [settings.width/100 + settings.width/2, settings.height - settings.height/3.5 - (settings.height/8) * 1],
            [settings.width/100 + settings.width/2, settings.height - settings.height/3.5 - (settings.height/8) * 2],
            [settings.width/100, settings.height - settings.height/3.5 - (settings.height/8) * 3.5],
        ]
        inputs_indent = [
            settings.height/5,
            settings.height/6,
            settings.height/6,
            settings.height/6,
            settings.height/6.2,

        ]

        inputs_text = ['up   ', 'down ', 'left ', 'right', 'shoot']
        for i in range(5):
            self.settings_buttons[4].append(
                read_key_image(
                    inputs_pos[i][0],
                    inputs_pos[i][1],
                    'buttons/button_clear_2_reverse.png',
                    'buttons/button_clear_selected_2_reverse.png',
                    scale=settings.height/160, color_text=(150, 150, 150, 255),
                    text=inputs_text[i], font='pixel.ttf', text_indent=settings.height/10,
                    text_input_indent=inputs_indent[i], shadow=graphics_settings.shadows_buttons
                )
            )

        self.settings_buttons[4][5].update_key(self.KEY_BINDS['main']['up'])
        self.settings_buttons[4][6].update_key(self.KEY_BINDS['main']['down'])
        self.settings_buttons[4][7].update_key(self.KEY_BINDS['main']['left'])
        self.settings_buttons[4][8].update_key(self.KEY_BINDS['main']['right'])
        self.settings_buttons[4][9].update_key(self.KEY_BINDS['main']['shoot_a'])

        self.select_player(0)

        self.read_settings()

    def on_mouse_press(self, x, y, button, modifiers):
        for s in self.settings_page_buttons:
            s.on_mouse_press(x, y, button, modifiers)

        for s in self.settings_buttons[self.page]:
            #for b in s:
            s.on_mouse_press(x, y, button, modifiers)

        return self.save_settings_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for s in self.settings_page_buttons:
            s.on_mouse_motion(x, y, dx, dy)

        for s in self.settings_buttons[self.page]:
            #for b in s:
            s.on_mouse_motion(x, y, dx, dy)

        self.save_settings_button.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for s in self.settings_buttons[self.page]:
            try:
                s.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            except:
                pass

    def on_key_press(self, symbol, modifier):
        for s in self.settings_buttons[self.page]:
            try:
                s.on_key_press(symbol, modifier)
            except:
                pass

    def on_key_press(self, symbol, modifiers):
        for s in self.settings_buttons[self.page]:
            try:
                s.on_key_press(symbol, modifiers)
            except:
                pass

    def on_text(self, text):
        for s in self.settings_buttons[self.page]:
            try:
                s.on_text(text)
            except:
                pass

    def draw(self):
        drawp(self.save_settings_button)
        for s in self.settings_page_buttons:
            drawp(s)

        for s in self.settings_page_buttons_text:
            s.draw()

        for s in self.settings_buttons[self.page]:
            drawp(s)

#game_settings_page = game_settings_page()
