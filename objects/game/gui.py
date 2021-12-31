class gui():
    def __init__(self):

        self.images_gui = []

        self.text_health = []
        self.text_ammo = []
        self.text_score = []

        self.pos = [
            [0, settings.height - settings.height/15],
            [settings.width - settings.width/8, settings.height - settings.height/15],
            [0, 0],
            [settings.width - settings.width/8, 0]
        ]

        self.pos_text = [
            [settings.width/80, settings.height - settings.height/15, 'left'],
            [settings.width - settings.width/80, settings.height - settings.height/15, 'right'],
            [settings.width/80, 0, 'left'],
            [settings.width - settings.width/80, 0, 'right']
        ]

        for i in range(4):
            self.images_gui.append(
                image_label('gui/ramka_' + tanks.teams[i] + '.png',
                    self.pos[i][0], self.pos[i][1],
                    scale=settings.height/240, pixel=True
                )
            )

            self.text_health.append(
                text_label(
                    self.pos_text[i][0], self.pos_text[i][1] + settings.height/18,
                    '100',
                    load_font=True, font='pixel.ttf', size=settings.height//72,
                    anchor_x=self.pos_text[i][2], color=(150, 150, 150, 255)
                )
            )

            self.text_ammo.append(
                text_label(
                    self.pos_text[i][0], self.pos_text[i][1] + settings.height/18 - settings.height/50,
                    '100',
                    load_font=True, font='pixel.ttf', size=settings.height//72,
                    anchor_x=self.pos_text[i][2], color=(150, 150, 150, 255)
                )
            )

            self.text_score.append(
                text_label(
                    self.pos_text[i][0], self.pos_text[i][1] + settings.height/18 - settings.height/50 - settings.height/50,
                    '100',
                    load_font=True, font='pixel.ttf', size=settings.height//72,
                    anchor_x=self.pos_text[i][2], color=(150, 150, 150, 255)
                )
            )



    def draw(self):
        for img in self.images_gui:
            drawp(img)

        for text in self.text_health:
            text.draw()
        for text in self.text_ammo:
            text.draw()
        for text in self.text_score:
            text.draw()
