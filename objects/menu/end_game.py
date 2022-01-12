def end_game(info):
    show_cursor()
    clear_display()
    add_display(back(arg='select_map(editor=False)'))
    add_display(background_menu())
    if graphics_settings.game_in_menu:
        add_game_in_menu()
    add_display(head_menu('end game'))
    add_display(image_button(0, settings.height/10, 'buttons/button_clear.png', scale=settings.height/120, center=False, arg='select_map(editor=False)', image_selected='buttons/button_clear_selected.png', text='exit', text_indent= settings.height//100, shadow=graphics_settings.shadows_buttons))

    add_display(end_game_table(info))
    add_display(table_game(end_game=True))

    add_display(head_menu(align_top=False))
    add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.01, for_from=255, for_before=0, tick=-5))

class end_game_table():
    def __init__(self, info):
        self.info = info
