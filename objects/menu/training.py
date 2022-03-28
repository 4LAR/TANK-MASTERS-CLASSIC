def training():
    show_cursor()
    clear_display()
    add_display(back(arg='menu()'))
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()
    add_display(head_menu('training'))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='menu()', image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))

    add_display(head_menu(align_top=False))

    add_display(label(0, 0,settings.width, settings.height,(0, 0, 0), alpha = 128))
    add_display(text_label(settings.width/2, settings.height/1.5, 'in the next updates', load_font=True, font='pixel.ttf', size=settings.height//18, anchor_x='center', color = (150, 150, 150, 255)))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='menu()', image_selected='buttons/button_clear_selected.png', text='back', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))
    training_start()

def training_start():
    play(
        "traning/traning",
        enemy_bool=True,
        enemy_bots=False,
        enemy_count = 8,
        traning=True
    )
