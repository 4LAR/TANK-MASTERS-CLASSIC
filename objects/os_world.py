import pickle
from PIL import ImageEnhance
import os

#


# класс который потом будет сохранён в файл или же наоборот
class save_world():
    def __init__(self):

        self.name = 'test' # название карты
        self.info = 'hello world' # информация о карте
        self.game_mode = 'death match' # игровой режим

        self.use_sound = False

        self.sound = [
            '', # default
            '', # rain
            '', # snow
            ''  # snow rain
        ]

        self.icon = None # иконка карты

        self.mods = [] # скрипты (передвежение объектов)

        self.spawn = [] # точки спавна игроков (x, y)
        self.flags = [] # точки для захвата (x, y, size)

        self.world_size = [64, 64] # размер карты

        self.map_floor = np.array([], dtype='<U32') # пол

        self.map_wall = np.array([], dtype='<U32') # стены

        self.map_water = np.array([], dtype='<U32') # жидкости

        self.map_middle = np.array([], dtype='<U32') # статичные объекты

        self.map_vegetation = np.array([], dtype='<U32') # растительность

        self.map_ceiling = np.array([], dtype='<U32') # крыши

        self.map_other_up = np.array([], dtype='<U32') # декор (лампы)
        self.map_other_down = np.array([], dtype='<U32') # декор (грязь, пол)

        self.map_effect_up = np.array([], dtype='<U32') # еффекты над игроком
        self.map_effect_down = np.array([], dtype='<U32') # еффекты под игроком

    # функция для обновлния массивов (для загрузки карты из файла)
    def write_world(self, world_size, map_floor, map_wall, map_water, map_vegetation, map_ceiling, map_middle, map_other_up, map_other_down, map_effect_up, map_effect_down,
            #info, game_mode, use_sound, sound, flags,
            old=False
        ):

        self.world_size = world_size

        self.map_floor = map_floor # пол

        self.map_wall = map_wall # стены

        self.map_water = map_water # жидкости

        self.map_middle = map_middle # статичные объекты

        self.map_vegetation = map_vegetation # растительность

        self.map_ceiling = map_ceiling # крыши

        self.map_other_up = map_other_up
        self.map_other_down = map_other_down

        self.map_effect_up = map_effect_up
        self.map_effect_down = map_effect_down

# класс который хранит в себе спрайты блоков, названия блоков и манипулирует с классом save_world
class os_world():
    def __init__(self):
        self.name = 'test' # название карты
        self.info = 'hello world' # информация о карте
        self.game_mode = 'death match' # игровой режим

        self.use_sound = False

        self.sound = [
            '', # default
            '', # rain
            '', # snow
            ''  # snow rain
        ]

        self.flags = [] # точки для захвата (x, y, size)

        self.size = 8 # разркшкние спрайтов
        self.resize = (8, 8) # тоже разрешение спрайтов, но содержит ширину и высоту

        self.save_world_obj = save_world() # инициализируем класс для карт

        self.floor_blocks_img = {} # текстуры блоков пола
        self.floor_snow_blocks_img = {} # текстуры блоков пола (снег)

        self.wall_block_img = {} # текстуры блоков стен

        self.water_block_img = {} # текстуры блоков жидкостей
        self.water_snow_block_img = {} # текстуры блоков жидкостей (снег)


        self.middle_block_img = {} # текстуры блоков хз чего (не используется)

        self.vegetation_block_img = {} # текстуры блоков растений
        self.vegetation_snow_block_img = {} # текстуры блоков растений (снег)

        self.ceiling_block_img = {} # текстуры блоков крыш

        self.other_up_block_img = {} # текстуры блоков декораций над игроком

        self.other_down_block_img = {} # текстуры блоков декораций под танком
        self.other_down_snow_block_img = {} # текстуры блоков декораций под танком


        self.effect_up_img = {} #

        # снизу циклы по считыванию названий блоков
        files_middle_block = os.listdir('img/world/other_up')
        self.other_up_block_name = []
        for block in files_middle_block:
            if block.split('.')[1] == 'png':
                self.other_up_block_name.append(block.split('.')[0])

        files_middle_block = os.listdir('img/world/other_down')
        self.other_down_block_name = []
        for block in files_middle_block:
            if block.split('.')[1] == 'png':
                self.other_down_block_name.append(block.split('.')[0])

        files_middle_block = os.listdir('img/world/snow/other_down') # snow
        self.other_down_snow_block_name = []
        for block in files_middle_block:
            if block.split('.')[1] == 'png':
                self.other_down_snow_block_name.append(block.split('.')[0])

        files_middle_block = os.listdir('img/world/middle')
        self.middle_block_name = []
        for block in files_middle_block:
            if block.split('.')[1] == 'png':
                self.middle_block_name.append(block.split('.')[0])

        files_floor_block = os.listdir('img/world/floor')
        self.floor_blocks_name = []
        for block in files_floor_block:
            if block.split('.')[1] == 'png':
                self.floor_blocks_name.append(block.split('.')[0])

        files_floor_block = os.listdir('img/world/snow/floor') # snow
        self.floor_snow_blocks_name = []
        for block in files_floor_block:
            if block.split('.')[1] == 'png':
                self.floor_snow_blocks_name.append(block.split('.')[0])

        files_wall_block = os.listdir('img/world/wall')
        self.wall_block_name = []
        for block in files_wall_block:
            if block.split('.')[1] == 'png':
                self.wall_block_name.append(block.split('.')[0])

        files_ceiling_block = os.listdir('img/world/ceiling')
        self.ceiling_block_name = []
        for block in files_ceiling_block:
            if block.split('.')[1] == 'png':
                self.ceiling_block_name.append(block.split('.')[0])

        files_waters_block = os.listdir('img/world/liquid')
        self.water_block_name = []
        for block in files_waters_block:
            file = os.listdir('img/world/liquid/' + block)
            for block_ in file:
                if block_.split('.')[1] == 'png':
                    self.water_block_name.append(block + '/' + block_.split('.')[0])

        files_waters_block = os.listdir('img/world/snow/liquid') # snow
        self.water_snow_block_name = []
        for block in files_waters_block:
            file = os.listdir('img/world/snow/liquid/' + block)
            for block_ in file:
                if block_.split('.')[1] == 'png':
                    self.water_snow_block_name.append(block + '/' + block_.split('.')[0])

        files_vegetation_block = os.listdir('img/world/vegetation')
        self.vegetation_block_name = []
        for block in files_vegetation_block:
            if block.split('.')[1] == 'png':
                self.vegetation_block_name.append(block.split('.')[0])

        files_vegetation_block = os.listdir('img/world/vegetation')
        self.vegetation_snow_block_name = []
        for block in files_vegetation_block:
            if block.split('.')[1] == 'png':
                self.vegetation_snow_block_name.append(block.split('.')[0])

        #

        files_effect_up_name_block = os.listdir('img/world/effect_up')
        self.effect_up_name = []
        for block in files_effect_up_name_block:
            if block.split('.')[1] == 'png':
                self.effect_up_name.append(block.split('.')[0])

        # снизу циклы для открытия спрайтов
        for block in self.other_up_block_name:
            self.other_up_block_img[block] = Image.open('img/world/other_up/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        for block in self.other_down_block_name:
            self.other_down_block_img[block] = Image.open('img/world/other_down/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        for block in self.other_down_snow_block_name: # snow
            self.other_down_snow_block_img[block] = Image.open('img/world/snow/other_down/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")


        for block in self.middle_block_name:
            self.middle_block_img[block] = Image.open('img/world/middle/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        for block in self.floor_blocks_name:
            self.floor_blocks_img[block] = Image.open('img/world/floor/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        for block in self.floor_snow_blocks_name: # зима
            self.floor_snow_blocks_img[block] = Image.open('img/world/snow/floor/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        for block in self.wall_block_name:
            self.wall_block_img[block] = Image.open('img/world/wall/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        for block in self.water_block_name:
            self.water_block_img[block] = Image.open('img/world/liquid/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        for block in self.water_snow_block_name: # snow
            self.water_snow_block_img[block] = Image.open('img/world/snow/liquid/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        for block in self.vegetation_block_name:
            self.vegetation_block_img[block] = Image.open('img/world/vegetation/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

            for block in self.vegetation_snow_block_name: # snow
                self.vegetation_snow_block_img[block] = Image.open('img/world/snow/vegetation/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")


        for block in self.ceiling_block_name:
            self.ceiling_block_img[block] = Image.open('img/world/ceiling/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        #

        for block in self.effect_up_name:
            self.effect_up_img[block] = Image.open('img/world/effect_up/'+block+'.png').resize(self.resize, Image.NEAREST).convert("RGBA")

        self.world_size = [64, 64] # размер карты по умолчанию

        self.map_floor = np.array([], dtype='<U32') # пол

        self.map_wall = np.array([], dtype='<U32') # стены

        self.map_middle = np.array([], dtype='<U32') #

        self.map_water = np.array([], dtype='<U32') # жидкости

        self.map_vegetation = np.array([], dtype='<U32') # растительность

        self.map_ceiling = np.array([], dtype='<U32') # крыши
        #
        self.map_other_up = np.array([], dtype='<U32') # декор (лампы)
        self.map_other_down = np.array([], dtype='<U32') # декор (грязь, пол)

        self.map_effect_up = np.array([], dtype='<U32') # еффекты над игроком
        self.map_effect_down = np.array([], dtype='<U32') # еффекты под игроком

    # функция для генерации новой карты
    def generate_world(self, world_size = [64, 64]):

        self.world_size = world_size

        # код для генерации мира (всё что закомментировано - это старая герерация мира), оспользуется для создания новых карт
        print("GENERATE WORLD")
        print("SPAWN FLOOR")
        self.map_floor = np.full(self.world_size[0] * self.world_size[1], 'grass.0', dtype='<U32')#grass.0

        print("SPAWN WALLS")
        self.map_wall = np.full(self.world_size[0] * self.world_size[1], 'none', dtype='<U32')

        print("SPAWN WATER")
        self.map_water = np.full(self.world_size[0] * self.world_size[1], 'none', dtype='<U32')

        print("SPAWN VEGETATION")
        self.map_vegetation = np.full(self.world_size[0] * self.world_size[1], 'none', dtype='<U32')

        print("SPAWN CEILING")
        self.map_ceiling = np.full(self.world_size[0] * self.world_size[1], 'none', dtype='<U32')

        print("SPAWN MIDDLE")
        self.map_middle = np.full(self.world_size[0] * self.world_size[1], 'none', dtype='<U32')

        print("SPAWN OTHER")
        self.map_other_up = np.full(self.world_size[0] * self.world_size[1], 'none', dtype='<U32')
        self.map_other_down = np.full(self.world_size[0] * self.world_size[1], 'none', dtype='<U32')

        print("SPAWN EFFECT")
        self.map_effect_up = np.full(self.world_size[0] * self.world_size[1], 'none', dtype='<U32')
        self.map_effect_down = np.full(self.world_size[0] * self.world_size[1], 'none', dtype='<U32')

        # записываем всё что сгенерировали в класс os_world
        self.save_world_obj.write_world(
            self.world_size,
            self.map_floor,
            self.map_wall,
            self.map_water,
            self.map_vegetation,
            self.map_ceiling,
            self.map_middle,
            self.map_other_up,
            self.map_other_down,
            self.map_effect_up,
            self.map_effect_down
        )

    # функция для сохраниения карты
    def save_file(self, file):
        if not os.path.exists('maps/'+file+'.map'): # если папки с картой не существует, то создаём её
            os.mkdir('maps/'+file+'.map')

        print(file)

        # сохряняем карту в obj файл
        save_obj(self.save_world_obj, 'maps/'+file+'.map/save')

    # функция для открытия карты
    def read_file(self, file, old=False):
        try:
            self.save_world_obj = load_obj('maps/'+file+'.map/save')

            self.world_size = self.save_world_obj.world_size

            self.map_floor = self.save_world_obj.map_floor

            self.map_wall = self.save_world_obj.map_wall

            self.map_middle = self.save_world_obj.map_middle

            self.map_water = self.save_world_obj.map_water

            self.map_vegetation = self.save_world_obj.map_vegetation

            self.map_ceiling = self.save_world_obj.map_ceiling

            self.map_other_up = self.save_world_obj.map_other_up
            self.map_other_down = self.save_world_obj.map_other_down

            self.map_effect_up = self.save_world_obj.map_effect_up
            self.map_effect_down = self.save_world_obj.map_effect_down

            # для переноса карт
            if not old:
                self.info = self.save_world_obj.info
                self.game_mode = self.save_world_obj.game_mode
                self.use_sound = self.save_world_obj.use_sound

                self.sound = self.save_world_obj.sound
                self.flags = self.save_world_obj.flags
                pass
            else:
                self.save_world_obj.info = self.info
                self.save_world_obj.game_mode = self.game_mode
                self.save_world_obj.use_sound = self.use_sound

                self.save_world_obj.sound = self.sound
                self.save_world_obj.flags = self.flags
                pass

            return True
        except Exception as e:
            print(e)
            return False

        #print(self.map_other_up)
