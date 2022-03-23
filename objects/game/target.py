class tragets():
    def __init__(self, count):
        self.targets = []

        for i in range(count):
            self.targets.append(target(i))

    def update(self):
        for t in self.targets:
            t.update()

    def draw(self):
        for t in self.targets:
            t.draw()

class target():
    def __init__(self, id):
        self.pos = [0, 0]

        self.dead = False

        self.death_delay = 2
        self.death_time = time.perf_counter() + self.death_delay

        self.image = None

    def update(self):
        pass

    def draw(self):
        pass


