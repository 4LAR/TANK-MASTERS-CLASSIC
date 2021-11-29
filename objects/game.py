def play():
    clear_display()
    add_display(world())
    #for i in range(4):
    #    add_display(player(i))
    add_display(player(0))
    add_display(walls())

def editor():
    engine_settings.on_mouse_scroll_bool = True
    clear_display()
    add_display(os_world())
    add_display(map())
    add_display(map_inventory())
