#
#
#
#

import screeninfo
import configparser
import os

class settings():
    def __init__(self):
        super().__init__()
        
        self.width = screeninfo.get_monitors()[0].width # ширина окна
        self.height = screeninfo.get_monitors()[0].height # высота окна
        self.full_screen = 1 # как будет работать окно (0 - окно с рамками, 1 - окно без рамок, полный экран (не стабильно) )
        self.gamma = 1.0 # гамма (не используется)

        self.fps = 120 # максимальный fps при обновлении классов

        self.show_fps = False # показ текущего fps

        self.console = False # включение консоли (не используется)

        self.sound_volume = 0.4 # громкость звука (1 - максимальное значение)

        self.use_window = True # False для включения только консольного режима (не используется)

        self.use_numba = False # Использовать библиотку numba для более быстрых рассчётов

        self.read_settings() # читаем настроки

    def save_settings(self):
        config = configparser.ConfigParser()

        config.add_section("Screen")
        config.set("Screen", "use_window", str(self.use_window)) # хз как делать
        config.set("Screen", "width", str(self.width))
        config.set("Screen", "height", str(self.height))
        config.set("Screen", "full-screen", str(self.full_screen))

        config.add_section("User_interface")
        config.set("User_interface", "show-fps", str(self.show_fps))
        config.set("User_interface", "console", str(self.console))

        config.add_section("Sound")
        config.set("Sound", "volume", str(self.sound_volume))

        config.add_section("Engine")
        config.set("Engine", "use_numba", str(self.use_numba))


        with open("settings.txt", "w") as config_file: # запись файла с настройками
            config.write(config_file)


    def read_settings(self):
        if not os.path.exists("settings.txt"): # проверка файла с настройками
            self.save_settings()
            self.read_settings()
        else:
            config = configparser.ConfigParser()
            config.read("settings.txt")
            self.use_window = True if (config.get("Screen", "use_window")).lower() == 'true' else False
            if ( screeninfo.get_monitors()[0].width >= int(config.get("Screen", "width")) and screeninfo.get_monitors()[0].height >= int(config.get("Screen", "height"))):
                self.width = int(config.get("Screen", "width"))
                self.height = int(config.get("Screen", "height"))

            self.full_screen = int(config.get("Screen", "full-screen"))

            self.show_fps = True if (config.get("User_interface", "show-fps")).lower() == 'true' else False

            self.console = True if (config.get("User_interface", "console")).lower() == 'true' else False

            self.sound_volume = float(config.get("Sound", "volume"))

            self.use_numba = True if (config.get("Engine", "use_numba")).lower() == 'true' else False
            if self.use_numba:
                import numba # типо оптимизация
