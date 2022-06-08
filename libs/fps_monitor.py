#
#
#
#

import pyglet

class FPS_label(): # класс для показа fps в левом верхнем угле
    def __init__(self, x, y, size, color):
        self.x = x # позиция по высоте
        self.y = y # позиция по высоте (инвертировано)
        self.size = size # размер шрифта
        self.color = color # цвет шрифта

        self.label = pyglet.text.Label('0',
            font_size=self.size,
            x=self.x, y=self.y,
            color=self.color) # создаём текст

    def update(self): # постоянно обновляем показания
        self.label.text = str(int(pyglet.clock.get_fps()))

    def draw(self): # прорисовываем текст
        self.label.draw()
