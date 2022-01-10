class Save_settings():
    def __init__(self):
        self.path = 'game_settings.txt'
        self.read_settings()

    def read_settings(self):
        if os.path.exists(self.path):
            config = configparser.ConfigParser()
            config.read(self.path)

            # Graphics
            graphics_settings.draw_leaf = True if (config.get("Graphics", "draw_leaf")).lower() == 'true' else False

            graphics_settings.draw_traces = True if (config.get("Graphics", "draw_traces")).lower() == 'true' else False
            graphics_settings.max_traces = int(config.get("Graphics", "max_traces"))

            graphics_settings.draw_shadows = True if (config.get("Graphics", "draw_shadows")).lower() == 'true' else False

            graphics_settings.draw_smoke = True if (config.get("Graphics", "draw_smoke")).lower() == 'true' else False

            graphics_settings.game_in_menu = True if (config.get("Graphics", "game_in_menu")).lower() == 'true' else False
            graphics_settings.shadows_buttons = True if (config.get("Graphics", "shadows_buttons")).lower() == 'true' else False

            # Game
            game_settings.scatter_bool = True if (config.get("Game", "scatter_bool")).lower() == 'true' else False

            game_settings.wind_deg = int(config.get("Game", "wind_deg"))
            game_settings.wind_bool = True if (config.get("Game", "wind_bool")).lower() == 'true' else False
            game_settings.wind_power = int(config.get("Game", "wind_power"))

            game_settings.rain = True if (config.get("Game", "rain")).lower() == 'true' else False
            game_settings.snow = True if (config.get("Game", "snow")).lower() == 'true' else False

            game_settings.time_bool = True if (config.get("Game", "time_bool")).lower() == 'true' else False
            game_settings.time_set_min = int(config.get("Game", "time_set_min"))
            game_settings.time_set_sec = int(config.get("Game", "time_set_sec"))

            # Tank
            for i in range(4):
                tank_settings.tanks[i][0] = True if (config.get("Tank_MPL", "P" + str(i + 1) + '_use')).lower() == 'true' else False
                tank_settings.tanks[i][1] = True if (config.get("Tank_MPL", "P" + str(i + 1) + '_bot')).lower() == 'true' else False
                tank_settings.tanks[i][2] = int(config.get("Tank_MPL", "P" + str(i + 1) + '_body'))
                tank_settings.tanks[i][3] = int(config.get("Tank_MPL", "P" + str(i + 1) + '_tower'))

        else:
            self.save_settings()

    def save_settings(self):
        config = configparser.ConfigParser()

        # Graphics
        config.add_section("Graphics")

        config.set("Graphics", "draw_leaf", str(graphics_settings.draw_leaf))

        config.set("Graphics", "draw_traces", str(graphics_settings.draw_traces))
        config.set("Graphics", "max_traces", str(graphics_settings.max_traces))

        config.set("Graphics", "draw_shadows", str(graphics_settings.draw_shadows))

        config.set("Graphics", "draw_smoke", str(graphics_settings.draw_smoke))

        config.set("Graphics", "game_in_menu", str(graphics_settings.game_in_menu))
        config.set("Graphics", "shadows_buttons", str(graphics_settings.shadows_buttons))

        # Game
        config.add_section("Game")

        config.set("Game", "scatter_bool", str(game_settings.scatter_bool))

        config.set("Game", "wind_deg", str(game_settings.wind_deg))
        config.set("Game", "wind_bool", str(game_settings.wind_bool))
        config.set("Game", "wind_power", str(game_settings.wind_power))

        config.set("Game", "rain", str(game_settings.rain))
        config.set("Game", "snow", str(game_settings.snow))

        config.set("Game", "time_bool", str(game_settings.time_bool))
        config.set("Game", "time_set_min", str(game_settings.time_set_min))
        config.set("Game", "time_set_sec", str(game_settings.time_set_sec))

        # Tank
        config.add_section("Tank_MPL")
        for i in range(4):
            config.set("Tank_MPL", "P" + str(i + 1) + '_use', str(tank_settings.tanks[i][0]))
            config.set("Tank_MPL", "P" + str(i + 1) + '_bot', str(tank_settings.tanks[i][1]))
            config.set("Tank_MPL", "P" + str(i + 1) + '_body', str(tank_settings.tanks[i][2]))
            config.set("Tank_MPL", "P" + str(i + 1) + '_tower', str(tank_settings.tanks[i][3]))

        with open(self.path, "w") as config_file: # запись файла с настройками
            config.write(config_file)

class Game_settings():
    def __init__(self):
        self.scatter_bool = True

        self.wind_deg = -45
        self.wind_bool = True
        self.wind_power = 100

        self.rain = False

        self.snow = False

        self.pause = False # dont save

        self.time_bool = True
        self.time_set_min = 2
        self.time_set_sec = 0

        self.multiplayer = False # dont save

class Graphics_settings():
    def __init__(self):

        self.draw_leaf = True

        self.draw_traces = False
        self.max_traces = 20

        self.draw_shadows = True

        self.draw_smoke = True

        self.game_in_menu = False
        self.shadows_buttons = False

class Tank_settings():
    def __init__(self):
        self.tanks = [
            [True, False, 0, 1],
            [False, False, 0, 1],
            [False, False,0, 1],
            [False, False,0, 1]
        ]

game_settings = Game_settings()
graphics_settings = Graphics_settings()
tank_settings = Tank_settings()

save_settings = Save_settings()
