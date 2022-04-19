def first_name():

    def save_name():
        save_settings.save_settings()
        user_game_settings.name = get_obj_display('input_label_image').text_obj.text_label.label.text
        save_settings.save_settings()
        off_input()
        add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.01, for_from=0, for_before=255, tick=5, arg="on_input(); menu()"))


    show_cursor()
    clear_display()
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()

    # background
    
    add_display(
            label(
                settings.width/60,
                settings.height/3.6,
                settings.width / 2.15,
                settings.height/1.8,
                (0, 0, 0), alpha=120
            )
        )
        
    add_display(
        text_label(
            settings.width/45,
            settings.height - settings.height/3.5 + (settings.height/8) * 0.5,
            'player',
            load_font=True, font='pixel.ttf',
            size=settings.height//24, anchor_x='left', anchor_y='bottom',
            color = (150, 150, 150, 255)
        )
    )

    add_display(
            label(
                settings.width/60 + settings.width/2,
                settings.height/3.6,
                settings.width / 2.15,
                settings.height/1.8,
                (0, 0, 0), alpha=120
            )
        )
        
    add_display(
        text_label(
            settings.width/45 + settings.width/2,
            settings.height - settings.height/3.5 + (settings.height/8) * 0.5,
            'traning',
            load_font=True, font='pixel.ttf',
            size=settings.height//24, anchor_x='left', anchor_y='bottom',
            color = (150, 150, 150, 255)
        )
    )
    
    # buttons
    add_display(image_button(settings.width - (settings.height/120 * 48), settings.height/10, 'buttons/button_clear_left.png', scale=settings.height/120, center=False, function=save_name, image_selected='buttons/button_clear_left_selected.png', text=language.json['menu']['continue'], text_indent= settings.height//25, shadow=graphics_settings.shadows_buttons))

    add_display(
        input_label_image(
            settings.width/25,
            settings.height - settings.height/3.5 - (settings.height/8) * 0.5,
            'buttons/button_clear_2_reverse.png', 'buttons/button_clear_selected_2_reverse.png',
            scale=settings.height/160, color_text=(150, 150, 150, 255),
            text='name', pre_text='PLAYER', font='pixel.ttf',
            text_indent=settings.height/12, text_input_indent=settings.height/6, shadow=graphics_settings.shadows_buttons
        )
    )

    add_display(
        image_flag(
            settings.width/25 + settings.width/2,
            settings.height - settings.height/3.5 - (settings.height/8) * 0.5,#3.5,
            image='buttons/flag_small/flag.png',
            image_flag='buttons/flag_small/flag_selected.png',
            image_selected_flag='buttons/flag_small/flag_hover_selected.png',
            image_selected='buttons/flag_small/flag_hover.png',
            scale=settings.height/160,

            text='education',
            text_color = (150, 150, 150, 255),
            font='pixel.ttf',
            text_indent=settings.height/8,

            shadow=graphics_settings.shadows_buttons

        )
    )

    add_display(head_menu('welcome'))
    add_display(head_menu(align_top=False, draw_user=False))

    add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.01, for_from=255, for_before=0, tick=-5))

def first_traning():
    pass
