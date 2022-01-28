class crates():
    def __init__(self):
        self.creates_obj = []
        self.creates_obj.append(
            image_label(
                'crates/crate.png',
                settings.width//2, settings.height//2,
                scale= get_obj_display('player').scale_tank, pixel=False,
                center=True
            )
        )

    def update(self):
        pass

    def draw(self):
        pass
