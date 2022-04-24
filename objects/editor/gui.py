class editor_gui():
    def __init__(self):
        # top bar

        self.hover = False

        self.head = head_menu(draw_user=False)

        self.show_layers_flag = image_flag(
            settings.width - settings.width/4.3,
            settings.height - settings.height/6 - (settings.height/10)*(-1),
            image='buttons/button_clear_full_kv.png',
            image_flag='buttons/button_clear_full_kv.png',
            image_selected_flag='buttons/button_clear_full_kv_selected.png',
            image_selected='buttons/button_clear_full_kv_selected.png',
            scale=settings.height/160,
            #function_bool = True,
            #arg='get_obj_display(\'map_inventory\').inventory_buttons_select(' + str(i) + ')',

            text='layers',
            text_color = (150, 150, 150, 255),
            font='pixel.ttf',
            text_indent=settings.height/20,

            text_size_y=1.2

        )

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

    def update(self):
        self.hover = self.show_layers_flag.selected
        
        for b in self.layers_buttons:
            if b.selected:
                self.hover = True
                break

    def on_mouse_motion(self, x, y, dx, dy):
        # top bar
        self.show_layers_flag.on_mouse_motion(x, y, dx, dy)

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

        # right bar
        if self.show_layers_flag.flag:
            for b in self.layers_buttons:
                b.on_mouse_press(x, y, button, modifiers)

    def draw(self):
        # top bar
        self.head.draw()
        self.show_layers_flag.draw()

        # right bar
        if self.show_layers_flag.flag:
            for b in self.layers_buttons:
                b.draw()

        # bottom bar
        self.pos_text.draw()
