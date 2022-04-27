class editor_gui():
    def __init__(self):
        self.hover = False

        # top bar

        self.head = head_menu(draw_user=False)

        self.back_button = image_button(
            settings.width - settings.width/25,
            settings.height - settings.height/6 - (settings.height/10)*(-1),
            'buttons/button_clear_full_kv.png',
            scale=settings.height/160,
            center=False,
            arg="get_obj_display(\'map\').exit()",

            image_selected='buttons/button_clear_full_kv_selected.png',
            text=language.json['menu']['exit'],
            text_color = (150, 150, 150, 255),
            font='pixel.ttf',
            text_indent=settings.height/5,

            text_size_y=1.2
        )
        self.back_button_image = image_label(
            'editor/exit.png',
            settings.width - settings.width/30,
            settings.height - settings.height/6.4 - (settings.height/10)*(-1),
            scale=settings.height/300,
            pixel=True
        )

        self.show_layers_flag = image_flag(
            settings.width - settings.width/4.3,
            settings.height - settings.height/6 - (settings.height/10)*(-1),
            image='buttons/button_clear_full_kv.png',
            image_flag='buttons/button_clear_full_kv.png',
            image_selected_flag='buttons/button_clear_full_kv_selected.png',
            image_selected='buttons/button_clear_full_kv_selected.png',
            scale=settings.height/160,

            text='layers',
            text_color = (150, 150, 150, 255),
            font='pixel.ttf',
            text_indent=settings.height/20,

            text_size_y=1.2

        )

        self.save_button = image_button(
            settings.width - settings.width/2.9,
            settings.height - settings.height/6 - (settings.height/10)*(-1),
            'editor/save_button/button.png',
            scale=settings.height/160,
            center=False,

            arg='get_obj_display(\'map\').save()',

            image_selected='editor/save_button/button_selected.png',
            text='save',
            text_color = (150, 150, 150, 255),
            font='pixel.ttf',
            text_indent=settings.height/40,

            text_size_y=1.2
        )

        # 0 - drag and drop
        # 1 - pressing
        # 2 - clamping
        self.cursor_type = []
        for i in range(3):
            self.cursor_type.append(
                image_flag(
                    settings.width/100 + (settings.width/23)*i,
                    settings.height - settings.height/6 - (settings.height/10)*(-1),
                    image='buttons/ramka_med/ramka.png',
                    image_flag='buttons/ramka_med/ramka_selected.png',
                    image_selected_flag='buttons/ramka_med/ramka_selected.png',
                    image_selected='buttons/ramka_med/ramka_selected.png',

                    function_bool=True,
                    arg='get_obj_display(\'editor_gui\').change_cursor_type(' + str(i) + ')',

                    scale=settings.height/240,
                    center=False,

                )
            )
            self.cursor_type[0].flag = True

        # 0 - draw
        # 1 - delete
        self.draw_type = []
        for i in range(2):
            self.draw_type.append(
                image_flag(
                    settings.width/100 + (settings.width/20)*3 + (settings.width/20)*i,
                    settings.height - settings.height/6 - (settings.height/10)*(-1),
                    image='buttons/ramka_med/ramka.png',
                    image_flag='buttons/ramka_med/ramka_selected.png',
                    image_selected_flag='buttons/ramka_med/ramka_selected.png',
                    image_selected='buttons/ramka_med/ramka_selected.png',

                    function_bool=True,
                    arg='get_obj_display(\'editor_gui\').change_draw_type(' + str(i) + ')',

                    scale=settings.height/240,
                    center=False,

                )
            )
        self.draw_type[0].flag = True
        

        # right bar
        self.layers_buttons = []
        self.layers_name = [
            'floor',
            'wall',
            'other_down',
            'water',
            'vegetation',
            'other_up',
            #'celling',
            #'effect_up',
            'grid'
        ]
        self.layers_name_code = [
            'show_floor',
            'show_wall',
            'show_other_down',
            'show_water',
            'show_vegetation',
            'show_other_up',
            #'show_celling',
            #'show_effect_up',
            'show_grid'
        ]

        for i in range(len(self.layers_name)):
            self.layers_buttons.append(
                image_flag(
                    settings.width - settings.width/4.3,
                    settings.height - settings.height/7.5 - (settings.height/15)*i,
                    image='editor/layers_flag/flag.png',
                    image_flag='editor/layers_flag/flag_selected.png',
                    image_selected_flag='editor/layers_flag/flag_selected_hover.png',
                    image_selected='editor/layers_flag/flag_hover.png',
                    scale=settings.height/160,
                    #function_bool = True,
                    #arg='get_obj_display(\'map_inventory\').inventory_buttons_select(' + str(i) + ')',

                    text=self.layers_name[i],
                    text_color = (150, 150, 150, 255),
                    font='pixel.ttf',
                    text_indent=settings.height/9,
                    text_scale=4.2,
                    text_size_y=1.3

                )
            )
            self.layers_buttons[i].flag = True

        # bottom bar
        self.font_scale = settings.height//36
        self.pos_text = text_label(settings.width - settings.width/5, settings.height/30, "cursor: 0 0", load_font=True, font='pixel.ttf', size=self.font_scale, anchor_x='left', color = (180, 180, 180, 255))

    def change_cursor_type(self, id):
        for i in range(len(self.cursor_type)):
            if (i != id):
                self.cursor_type[i].flag = False

    def change_draw_type(self, id):
        for i in range(len(self.draw_type)):
            if (i != id):
                self.draw_type[i].flag = False

    def update(self):
        self.hover = self.show_layers_flag.selected

        self.hover = True if self.save_button.selected else self.hover
        self.hover = True if self.back_button.selected else self.hover

        for b in self.layers_buttons:
            if b.selected:
                self.hover = True
                break

        for b in self.cursor_type:
            if b.selected:
                self.hover = True
                break

        for b in self.draw_type:
            if b.selected:
                self.hover = True
                break

    def on_mouse_motion(self, x, y, dx, dy):
        # top bar
        self.show_layers_flag.on_mouse_motion(x, y, dx, dy)
        self.back_button.on_mouse_motion(x, y, dx, dy)
        self.save_button.on_mouse_motion(x, y, dx, dy)

        for b in self.cursor_type:
            b.on_mouse_motion(x, y, dx, dy)

        for b in self.draw_type:
            b.on_mouse_motion(x, y, dx, dy)

        # right bar
        if self.show_layers_flag.flag:
            for b in self.layers_buttons:
                b.on_mouse_motion(x, y, dx, dy)

        # bottom bar
        x_ = int( ( ( (get_obj_display('map').pos[0] - x)/get_obj_display('map').scale )//get_obj_display('map').size) ) + 1
        y_ = int( ( ( (get_obj_display('map').pos[1] - y)/get_obj_display('map').scale )//get_obj_display('map').size) )

        _x_ = int(math.sqrt(x_ ** 2))
        _y_ = get_obj_display('map').world_size[1] - int(math.sqrt(y_ ** 2))

        self.pos_text.label.text = "cursor: " + str(_x_) + " " + str(_y_)

    def on_mouse_press(self, x, y, button, modifiers):
        # top bar
        self.show_layers_flag.on_mouse_press(x, y, button, modifiers)
        self.back_button.on_mouse_press(x, y, button, modifiers)
        self.save_button.on_mouse_press(x, y, button, modifiers)

        for b in self.cursor_type:
            b.on_mouse_press(x, y, button, modifiers)

        for b in self.draw_type:
            b.on_mouse_press(x, y, button, modifiers)

        # right bar
        if self.show_layers_flag.flag:
            for b in self.layers_buttons:
                b.on_mouse_press(x, y, button, modifiers)

    def draw(self):
        # top bar
        self.head.draw()
        self.show_layers_flag.draw()
        self.back_button.draw()
        self.back_button_image.draw()
        self.save_button.draw()

        for b in self.cursor_type:
            b.draw()

        for b in self.draw_type:
            b.draw()

        # right bar
        if self.show_layers_flag.flag:
            for b in self.layers_buttons:
                b.draw()

        # bottom bar
        self.pos_text.draw()
