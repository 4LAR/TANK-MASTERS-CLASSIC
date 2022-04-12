def first_name():
    show_cursor()
    clear_display()
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()

    add_display(image_button(settings.width - (settings.height/120 * 48), settings.height/10, 'buttons/button_clear_left.png', scale=settings.height/120, center=False, function=menu, image_selected='buttons/button_clear_left_selected.png', text=language.json['menu']['continue'], text_indent= settings.height//25, shadow=graphics_settings.shadows_buttons))

    add_display(head_menu('welcome'))
    add_display(head_menu(align_top=False, draw_user=False))

    add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.01, for_from=255, for_before=0, tick=-5))

def first_traning():
    pass
