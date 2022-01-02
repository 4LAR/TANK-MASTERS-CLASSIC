class Game_settings():
    def __init__(self):
        self.scatter_bool = False

        self.wind_deg = 45
        self.wind_bool = True
        self.wind_power = 100

        self.rain = False

        self.snow = False

        self.pause = False

        self.multiplayer = False

class Graphics_settings():
    def __init__(self):

        self.path = 'game_settings.txt'
        self.draw_traces = False
        self.max_traces = 20

        self.draw_shadows = True

        self.draw_smoke = True

        self.game_in_menu = False

        self.read_settings()

    def read_settings(self):
        if os.path.exists(self.path):
            config = configparser.ConfigParser()
            config.read(self.path)

            self.draw_traces = True if (config.get("Graphics", "draw_traces")).lower() == 'true' else False
            self.max_traces = int(config.get("Graphics", "max_traces"))

            self.draw_shadows = True if (config.get("Graphics", "draw_shadows")).lower() == 'true' else False

            self.draw_smoke = True if (config.get("Graphics", "draw_smoke")).lower() == 'true' else False

            self.game_in_menu = True if (config.get("Graphics", "game_in_menu")).lower() == 'true' else False
        else:
            self.save_settings()

    def save_settings(self):
        config = configparser.ConfigParser()
        config.add_section("Graphics")

        config.set("Graphics", "draw_traces", str(self.draw_traces))
        config.set("Graphics", "max_traces", str(self.max_traces))

        config.set("Graphics", "draw_shadows", str(self.draw_shadows))

        config.set("Graphics", "draw_smoke", str(self.draw_smoke))

        config.set("Graphics", "game_in_menu", str(self.game_in_menu))

        with open(self.path, "w") as config_file: # запись файла с настройками
            config.write(config_file)

game_settings = Game_settings()
graphics_settings = Graphics_settings()
