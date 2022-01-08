def single_game():
    show_cursor()
    clear_display()
    add_display(back(arg='menu()'))
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()
    add_display(head_menu('single: select level'))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='menu()', image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))

    add_display(head_menu(align_top=False))
