
#🐀

KEY_BINDS = {
    'P1': {
        'up': 'W',
        'left': 'A',
        'down': 'S',
        'right': 'D',
        'shoot_a': 'SPACE'
    },

    'P2': {
        'up': 'UP',
        'left': 'LEFT',
        'down': 'DOWN',
        'right': 'RIGHT',
        'shoot_a': 'RCTRL'
    },

    'P3': {
        'up': 'U',
        'left': 'H',
        'down': 'J',
        'right': 'K',
        'shoot_a': 'B'
    },

    'P4': {
        'up': 'NUM_8',
        'left': 'NUM_4',
        'down': 'NUM_5',
        'right': 'NUM_6',
        'shoot_a': 'NUM_0'
    }
}

def play(map_name='test'):
    clear_display()
    add_display(world(map_name))
    add_display(players())
    add_display(bullets())
    add_display(walls())

def editor():
    engine_settings.on_mouse_scroll_bool = True
    clear_display()
    add_display(os_world())
    add_display(map())
    add_display(map_inventory())
