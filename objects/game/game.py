
#🐀

KEY_BINDS = {
    'main': {
        'up': 'W',
        'left': 'A',
        'down': 'S',
        'right': 'D',
        'shoot_a': 'SPACE'
    },

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

if os.path.exists('KEY_BINDS.json'):
    KEY_BINDS = read_dict('KEY_BINDS')
else:
    save_dict(KEY_BINDS, 'KEY_BINDS')

class tanks():
    def __init__(self):
        self.teams = ['red', 'blue', 'green', 'yellow', 'no_team']

        self.bases = ['tank_base', 'tank_quadrocopter_base', 'tank_wheels_base']
        self.bases_speed = [settings.height/60, settings.height/60, settings.height/50]
        self.bases_health = [100, 60, 60]

        self.towers = ['gun', 'bgun', 'mgun', 'rgun', 'rmgun']
        self.towers_speed = [settings.height/60, settings.height/60, settings.height/60, settings.height/60 * 1.5, settings.height/60 * 1.5]
        self.towers_damage = [60, 100, 15, 100, 60]
        self.towers_delay = [1, 1.5, 0.1, 0.2, 0.2]
        self.towers_scatter = [0, 0, 4, 0, 0]
        self.score = {
            'kill': 1
        }
        self.towers_laser_color = [
            (200, 0, 0),
            (0, 0, 200),
            (0, 200, 0),
            (200, 200, 0)
        ]
        self.team_colors = [
            (128, 0, 0),
            (0, 0, 128),
            (0, 128, 0),
            (128, 128, 0),
            (100, 100, 100)
        ]


tanks = tanks()

def play(
            map_name='test',
            bot=[False, False, False, False],
            tanks=[True, False, False, False],
            tank_settings=[[0, 0], [0, 0], [0, 0], [0, 0]],
            enemy_bool=False,
            enemy_count=0,
            enemy_bots=False,
            traning=False
        ):
    hide_cursor()
    clear_display()
    add_display(game_settings)
    add_display(graphics_settings)
    add_display(world(map_name))
    add_display(crates())
    add_display(players(bot, tanks, tank_settings, enemy_bool, enemy_count, enemy_bots, traning))
    add_display(bullets())
    add_display(wind())
    add_display(walls())
    add_display(smoke())
    add_display(weather())
    add_display(gui(traning))
    add_display(pause(traning))
    add_display(table_game(traning=traning))
    if game_settings.multiplayer:
        add_display(net_code())
    add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.01, for_from=255, for_before=0, tick=-5, arg='get_obj_display(\'gui\').start_run_time()'))


def editor(map_name='test', new=False):
    show_cursor()
    engine_settings.on_mouse_scroll_bool = True
    clear_display()
    add_display(os_world())
    add_display(map(map_name, new))
    add_display(map_inventory())
