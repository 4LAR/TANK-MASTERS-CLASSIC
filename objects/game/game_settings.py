class Save_settings():
    def __init__(self):
        self.path = 'game_settings.txt'
        self.read_settings()

    def read_settings(self):
        if os.path.exists(self.path):
            config = configparser.ConfigParser()
            config.read(self.path)

            # Game
            user_game_settings.name = config.get("Game", "name")
            user_game_settings.draw_logo = True if (config.get("Game", "draw_logo")).lower() == 'true' else False

            # Sound
            sound_settings.use_sound_general = True if (config.get("Sound", "use_sound_general")).lower() == 'true' else False
            sound_settings.use_sound_buttons = True if (config.get("Sound", "use_sound_buttons")).lower() == 'true' else False
            sound_settings.use_sound_tanks = True if (config.get("Sound", "use_sound_tanks")).lower() == 'true' else False
            sound_settings.use_sound_background = True if (config.get("Sound", "use_sound_background")).lower() == 'true' else False

            sound_settings.sound_volume_buttons = float(config.get("Sound", "sound_volume_buttons"))
            sound_settings.sound_volume_tanks = float(config.get("Sound", "sound_volume_tanks"))
            sound_settings.sound_volume_background = float(config.get("Sound", "sound_volume_background"))

            sound_settings.update_sound()

            # Graphics
            graphics_settings.animated_water = True if (config.get("Graphics", "animated_water")).lower() == 'true' else False

            graphics_settings.draw_clouds = True if (config.get("Graphics", "draw_clouds")).lower() == 'true' else False

            graphics_settings.draw_leaf = True if (config.get("Graphics", "draw_leaf")).lower() == 'true' else False

            graphics_settings.draw_traces = True if (config.get("Graphics", "draw_traces")).lower() == 'true' else False
            graphics_settings.max_traces = int(config.get("Graphics", "max_traces"))

            graphics_settings.draw_shadows = True if (config.get("Graphics", "draw_shadows")).lower() == 'true' else False
            graphics_settings.better_shadows = True if (config.get("Graphics", "better_shadows")).lower() == 'true' else False

            graphics_settings.draw_smoke = True if (config.get("Graphics", "draw_smoke")).lower() == 'true' else False

            graphics_settings.game_in_menu = True if (config.get("Graphics", "game_in_menu")).lower() == 'true' else False
            graphics_settings.map_in_menu = config.get("Graphics", "map_in_menu")
            graphics_settings.paralax_in_menu = True if (config.get("Graphics", "paralax_in_menu")).lower() == 'true' else False

            graphics_settings.shadows_buttons = True if (config.get("Graphics", "shadows_buttons")).lower() == 'true' else False

            # Game_setup
            game_settings.scatter_bool = True if (config.get("Game_setup", "scatter_bool")).lower() == 'true' else False

            game_settings.wind_deg = int(config.get("Game_setup", "wind_deg"))
            game_settings.wind_bool = True if (config.get("Game_setup", "wind_bool")).lower() == 'true' else False
            game_settings.wind_power = int(config.get("Game_setup", "wind_power"))
            game_settings.random_wind = True if (config.get("Game_setup", "random_wind")).lower() == 'true' else False

            game_settings.crates_bool = True if (config.get("Game_setup", "crates_bool")).lower() == 'true' else False

            game_settings.rain = True if (config.get("Game_setup", "rain")).lower() == 'true' else False
            game_settings.snow = True if (config.get("Game_setup", "snow")).lower() == 'true' else False
            game_settings.random_weather = True if (config.get("Game_setup", "random_weather")).lower() == 'true' else False

            game_settings.time_bool = True if (config.get("Game_setup", "time_bool")).lower() == 'true' else False
            game_settings.time_set_min = int(config.get("Game_setup", "time_set_min"))
            game_settings.time_set_sec = int(config.get("Game_setup", "time_set_sec"))

            game_settings.collide_players = True if (config.get("Game_setup", "collide_players")).lower() == 'true' else False
            game_settings.random_tanks_bool = True if (config.get("Game_setup", "random_tanks_bool")).lower() == 'true' else False

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

        config.add_section("Game")
        config.set("Game", "name", str(user_game_settings.name))

        config.set("Game", "draw_logo", str(user_game_settings.draw_logo))

        # Sound
        config.add_section("Sound")
        config.set("Sound", "use_sound_general", str(sound_settings.use_sound_general))
        config.set("Sound", "use_sound_buttons", str(sound_settings.use_sound_buttons))
        config.set("Sound", "use_sound_tanks", str(sound_settings.use_sound_tanks))
        config.set("Sound", "use_sound_background", str(sound_settings.use_sound_background))

        config.set("Sound", "sound_volume_buttons", str(sound_settings.sound_volume_buttons))
        config.set("Sound", "sound_volume_tanks", str(sound_settings.sound_volume_tanks))
        config.set("Sound", "sound_volume_background", str(sound_settings.sound_volume_background))

        sound_settings.update_sound()

        # Graphics
        config.add_section("Graphics")

        config.set("Graphics", "animated_water", str(graphics_settings.animated_water))

        config.set("Graphics", "draw_clouds", str(graphics_settings.draw_clouds))

        config.set("Graphics", "draw_leaf", str(graphics_settings.draw_leaf))

        config.set("Graphics", "draw_traces", str(graphics_settings.draw_traces))
        config.set("Graphics", "max_traces", str(graphics_settings.max_traces))

        config.set("Graphics", "draw_shadows", str(graphics_settings.draw_shadows))
        config.set("Graphics", "better_shadows", str(graphics_settings.better_shadows))

        config.set("Graphics", "draw_smoke", str(graphics_settings.draw_smoke))

        config.set("Graphics", "game_in_menu", str(graphics_settings.game_in_menu))
        config.set("Graphics", "map_in_menu", str(graphics_settings.map_in_menu))
        config.set("Graphics", "paralax_in_menu", str(graphics_settings.paralax_in_menu))

        config.set("Graphics", "shadows_buttons", str(graphics_settings.shadows_buttons))

        # Game_setup
        config.add_section("Game_setup")

        config.set("Game_setup", "scatter_bool", str(game_settings.scatter_bool))

        config.set("Game_setup", "wind_deg", str(game_settings.wind_deg))
        config.set("Game_setup", "wind_bool", str(game_settings.wind_bool))
        config.set("Game_setup", "wind_power", str(game_settings.wind_power))
        config.set("Game_setup", "random_wind", str(game_settings.random_wind))

        config.set("Game_setup", "crates_bool", str(game_settings.crates_bool))

        config.set("Game_setup", "rain", str(game_settings.rain))
        config.set("Game_setup", "snow", str(game_settings.snow))
        config.set("Game_setup", "random_weather", str(game_settings.random_weather))

        config.set("Game_setup", "time_bool", str(game_settings.time_bool))
        config.set("Game_setup", "time_set_min", str(game_settings.time_set_min))
        config.set("Game_setup", "time_set_sec", str(game_settings.time_set_sec))

        config.set("Game_setup", "collide_players", str(game_settings.collide_players))
        config.set("Game_setup", "random_tanks_bool", str(game_settings.random_tanks_bool))

        # Tank
        config.add_section("Tank_MPL")
        for i in range(4):
            config.set("Tank_MPL", "P" + str(i + 1) + '_use', str(tank_settings.tanks[i][0]))
            config.set("Tank_MPL", "P" + str(i + 1) + '_bot', str(tank_settings.tanks[i][1]))
            config.set("Tank_MPL", "P" + str(i + 1) + '_body', str(tank_settings.tanks[i][2]))
            config.set("Tank_MPL", "P" + str(i + 1) + '_tower', str(tank_settings.tanks[i][3]))

        with open(self.path, "w") as config_file: # запись файла с настройками
            config.write(config_file)

class User_game_settings(): # game settings
    def __init__(self):
        self.name = 'PLAYER'

        self.draw_logo = True

class Game_settings(): # settings in game
    def __init__(self):
        self.scatter_bool = True

        self.wind_deg = -45
        self.wind_bool = True
        self.wind_power = 100
        self.random_wind = False

        self.rain = False
        self.snow = False
        self.random_weather = False

        self.time_bool = True
        self.time_set_min = 2
        self.time_set_sec = 0

        self.collide_players = True
        self.random_tanks_bool = False

        self.crates_bool = True

        self.pause = False # dont save
        self.run = False
        self.end_game = False # dont save
        self.multiplayer = False # dont save
        self.multiplayer_id = 0#int(input('id: ')) # dont save

    def reload(self):
        self.pause = False
        self.run = False
        self.end_game = False
        self.multiplayer = False
        self.multiplayer_id = 0

class Graphics_settings():
    def __init__(self):

        self.animated_water = False

        self.draw_clouds = True

        self.draw_leaf = True

        self.draw_traces = False
        self.max_traces = 20

        self.draw_shadows = True
        self.better_shadows = True

        self.draw_smoke = True

        self.game_in_menu = True
        self.map_in_menu = 'arcade/Castle'
        self.paralax_in_menu = True

        self.shadows_buttons = True

class Sound_settings():
    def __init__(self):
        self.use_sound_general = True
        self.use_sound_buttons = True
        self.use_sound_tanks = True
        self.use_sound_background = True

        self.sound_volume_buttons = 0.07
        self.sound_volume_tanks = 0.08
        self.sound_volume_background = 0.62

    def update_sound(self):
        if self.use_sound_general and self.use_sound_buttons:
            sound.sound_volume(settings.sound_volume * self.sound_volume_buttons)
        else:
            sound.sound_volume(0)
        #
        if self.use_sound_general and self.use_sound_background:
            background_sound.sound_volume(settings.sound_volume * self.sound_volume_background)
        else:
            background_sound.sound_volume(0)

class Tank_settings():
    def __init__(self):
        self.tanks = [
            [True, False, 0, 1],
            [False, False, 0, 1],
            [False, False,0, 1],
            [False, False,0, 1]
        ]

user_game_settings = User_game_settings()
game_settings = Game_settings()
graphics_settings = Graphics_settings()
sound_settings = Sound_settings()
tank_settings = Tank_settings()

save_settings = Save_settings()
