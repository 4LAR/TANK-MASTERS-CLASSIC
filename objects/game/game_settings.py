class Game_settings():
    def __init__(self):
        self.scatter_bool = True

        self.wind_deg = -45
        self.wind_bool = False

        self.rain = False

        self.snow = False

        self.pause = False

        self.multiplayer = False

class Graphics_settings():
    def __init__(self):
        self.draw_traces = False
        self.max_traces = 20

        self.draw_shadows = True

        self.draw_smoke = True

        self.game_in_menu = False

game_settings = Game_settings()
graphics_settings = Graphics_settings()
