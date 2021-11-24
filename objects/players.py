class player():
    def __init__(self, id):
        self.id = id
        self.pos = [settings.width//2, settings.height//2]

        self.scale_tank = get_obj_display('world').scale

        self.def_speed = [settings.height/60]
        self.speed_tick = self.def_speed[0]/10
        self.speed = 0
        self.rotation = 0

        self.anim_ticks = 0
        self.anim_body_state = 0

        self.obj_tanks = []
        self.obj_tanks.append([])

        self.obj_tanks[0].append(image_label('tanks/body/no_team/tank_base.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))
        self.obj_tanks[0].append(image_label('tanks/body/no_team/tank_base_1.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))

        self.obj_tanks.append(image_label('tanks/tower/gun.png', settings.width//2, settings.height//2, scale=self.scale_tank, pixel=False, center=True))


    def anim_tick(self):
        self.anim_ticks += 1
        if self.anim_ticks >= 10:
            if len(self.obj_tanks[0]) > self.anim_body_state + 1:
                self.anim_body_state += 1
            else:
                self.anim_body_state = 0
            self.anim_ticks = 0


    def update(self):
        if keyboard[key.A]:
            self.pos[0] -= self.speed_tick
            self.rotation = -90
            self.anim_tick()
        elif keyboard[key.D]:
            self.pos[0] += self.speed_tick
            self.rotation = 90
            self.anim_tick()
        elif keyboard[key.W]:
            self.pos[1] += self.speed_tick
            self.rotation = 0
            self.anim_tick()
        elif keyboard[key.S]:
            self.pos[1] -= self.speed_tick
            self.rotation = 180
            self.anim_tick()

        for i in range(len(self.obj_tanks)):
            if i != 0:
                self.obj_tanks[i].update_rotation(self.rotation)

                self.obj_tanks[i].x = self.pos[0]
                self.obj_tanks[i].y = self.pos[1]
                self.obj_tanks[i].update_image(True)

            else:
                self.obj_tanks[i][self.anim_body_state].update_rotation(self.rotation)

                self.obj_tanks[i][self.anim_body_state].x = self.pos[0]
                self.obj_tanks[i][self.anim_body_state].y = self.pos[1]
                self.obj_tanks[i][self.anim_body_state].update_image(True)

    def draw(self):
        for i in range(len(self.obj_tanks)):
            if i != 0:
                drawp(self.obj_tanks[i])
            else:
                drawp(self.obj_tanks[i][self.anim_body_state])
