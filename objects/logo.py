#
#
#
#

import time

window.set_icon(pyglet.image.load('img/stone_engine.png'))

time.sleep(1)

class skip():
	def __init__(self, type=0):
		self.type = type
		pass

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.ESCAPE:
			if self.type == 0:
			#	text_logo()
			#else:
				main()
			return pyglet.event.EVENT_HANDLED
		elif symbol == pyglet.window.key.SPACE:
			if self.type == 0:
			#	text_logo()
			#else:
				main()
		return True

# логотип 100LAR STUDIO
def logo_stop():
    add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.04, function=text_logo, for_from=0, for_before=255, tick=5))

def logo_text():

    add_display(text_label(settings.width//2, settings.height//4, '100LAR STUDIO', load_font=True, font='pixel.ttf', size=settings.height//10, anchor_x='center', color = (180, 180, 180, 255)))
    add_display(breathing_label(0, settings.height//6, settings.width, settings.height//6, (0, 0, 0), 0, delay=0.04, function=logo_stop))
#main()
add_display(skip())
add_display(label(settings.width, settings.height, settings.width, settings.height, (0, 0, 0)))
add_display(image_label('logo_studio.png', settings.width//2.5, settings.height//3, scale=settings.height//180, pixel=True))
add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.04, function=logo_text))

# предупреждающий текст
def add_timer_text_logo():
	add_display(timer(
		2,
		None,
		'add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.04, function=main, for_from=0, for_before=255, tick=5))'
	))

def text_logo():
	clear_display()
	add_display(skip())
	add_display(label(settings.width, settings.height, settings.width, settings.height, (0, 0, 0)))
	add_display(text_label(settings.width//2, settings.height//2, 'This project is under development.', load_font=True, font='pixel.ttf', size=settings.height//20, anchor_x='center', color = (180, 180, 180, 255)))
	add_display(text_label(settings.width//2, settings.height//2 - settings.height//19, 'It will improve with each update.', load_font=True, font='pixel.ttf', size=settings.height//20, anchor_x='center', color = (180, 180, 180, 255)))
	add_display(breathing_label(0, 0, settings.width, settings.height, (0, 0, 0), 0, delay=0.04, function=add_timer_text_logo))
