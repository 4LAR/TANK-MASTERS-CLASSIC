class game_settings_page():
    def select_page(self, id):
        self.settings_page_buttons[id].flag = True
        self.page = id
        for i in range(len(self.settings_page_buttons)):
            if i != id:
                self.settings_page_buttons[i].flag = False

    def read_settings(self):
        self.settings_buttons[2][0].flag = graphics_settings.game_in_menu
        self.settings_buttons[2][1].flag = graphics_settings.draw_traces
        self.settings_buttons[2][2].flag = graphics_settings.draw_shadows
        self.settings_buttons[2][3].flag = graphics_settings.draw_smoke

    def save_settings(self):

        # 0 - game in menu
        # 1 - draw_traces
        # 2 - draw shadows
        # 3 - draw smoke

        graphics_settings.game_in_menu = self.settings_buttons[2][0].flag
        graphics_settings.draw_traces = self.settings_buttons[2][1].flag
        graphics_settings.draw_shadows = self.settings_buttons[2][2].flag
        graphics_settings.draw_smoke = self.settings_buttons[2][3].flag

        graphics_settings.save_settings()

    def __init__(self):

        self.save_settings_button = add_display(
            image_button(
                settings.width - (settings.height/120 * 48), settings.height/10,
                'buttons/button_clear_left.png', scale=settings.height/120,
                center=False, arg='get_obj_display("game_settings_page").save_settings(); menu()',
                image_selected='buttons/button_clear_left_selected.png',
                text='save', text_indent= settings.height/20
            )
        )

        self.page = 0
        # 0 - display
        # 1 - sound
        # 2 - graphics
        # 3 - keyboard

        self.settings_page_buttons = []
        self.settings_page_buttons_text = []

        buttons_distance = settings.width/5.4

        # display
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
                settings.width/30,
                settings.height - settings.height/6 + settings.height/50,
                'display',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )

        self.settings_page_buttons[0].flag = True

        # sound
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
                buttons_distance + settings.width/20,
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
                buttons_distance * 2 + settings.width/40,
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
                'keyboard',
                load_font=True, font='pixel.ttf',
                size=settings.height//24, anchor_x='left', anchor_y='bottom',
                color = (150, 150, 150, 255)
            )
        )

        self.settings_buttons = []

        # display
        self.settings_buttons.append([])
        #self.settings_buttons[0].append()

        # sound
        self.settings_buttons.append([])
        self.settings_buttons[1].append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/3.5,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

            )
        )

        # graphics
        self.settings_buttons.append([])

        self.settings_buttons[2].append(
            image_flag(
                settings.width/100,
                settings.height - settings.height/3.5,
                image='buttons/flag/flag.png',
                image_flag='buttons/flag/flag_selected.png',
                image_selected_flag='buttons/flag/flag_hover_selected.png',
                image_selected='buttons/flag/flag_hover.png',
                scale=settings.height/160,

                text='game in menu',
                text_color = (150, 150, 150, 255),
                font='pixel.ttf',
                text_indent=settings.height/8

            )
        )

        self.settings_buttons[2].append(
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
                text_indent=settings.height/8

            )
        )

        self.settings_buttons[2].append(
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
                text_indent=settings.height/8

            )
        )

        self.settings_buttons[2].append(
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
                text_indent=settings.height/8

            )
        )

        # keyboard
        self.settings_buttons.append([])


        self.read_settings()

    def on_mouse_press(self, x, y, button, modifiers):
        for s in self.settings_page_buttons:
            s.on_mouse_press(x, y, button, modifiers)

        for s in self.settings_buttons[self.page]:
            #for b in s:
            s.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for s in self.settings_page_buttons:
            s.on_mouse_motion(x, y, dx, dy)

        for s in self.settings_buttons[self.page]:
            #for b in s:
            s.on_mouse_motion(x, y, dx, dy)

    def draw(self):
        for s in self.settings_page_buttons:
            drawp(s)

        for s in self.settings_page_buttons_text:
            s.draw()

        for s in self.settings_buttons[self.page]:
            drawp(s)
