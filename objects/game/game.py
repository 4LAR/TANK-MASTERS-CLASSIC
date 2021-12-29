
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

class tanks():
    def __init__(self):
        self.teams = ['red', 'green', 'blue', 'yellow', 'no_team']

        self.bases = ['tank_base', 'tank_quadrocopter_base', 'tank_wheels_base']
        self.bases_speed = [settings.height/60, settings.height/60, settings.height/50]
        self.bases_health = [100, 60, 60]

        self.towers = ['gun', 'bgun', 'mgun', 'rgun', 'rmgun']
        self.towers_damage = [60, 100, 10, 100, 60]
        self.towers_delay = [1, 1.5, 0.12, 1.5, 1]
        self.towers_scatter = [0, 0, 4, 0, 0]


tanks = tanks()

def play(
            map_name='test',
            bot=[False, False, False, False],
            tanks=[True, False, False, False],
            tank_settings=[[0, 0], [0, 0], [0, 0], [0, 0]]
        ):
    clear_display()
    add_display(game_settings())
    add_display(world(map_name))
    add_display(players(bot, tanks, tank_settings))
    add_display(bullets())
    add_display(walls())

def editor(map_name='test', new=False):
    engine_settings.on_mouse_scroll_bool = True
    clear_display()
    add_display(os_world())
    add_display(map(map_name, new))
    add_display(map_inventory())
