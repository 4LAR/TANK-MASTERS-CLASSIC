
def editor(map_name='test', new=False):
    background_sound.pause()
    show_cursor()
    engine_settings.on_mouse_scroll_bool = True
    clear_display()
    add_display(os_world())
    add_display(map(map_name, new))
    add_display(editor_gui())
    add_display(map_inventory())
