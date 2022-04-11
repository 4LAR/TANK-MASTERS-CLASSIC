class player_info_class():
    def __init__(self):
        pass

class player_info_save():
    def __init__(self):
        self.path = 'info.pkl'
        self.info = None

        self.read()

    def get_info(self):
        return self.info

    def save(self):
        save_obj(self.info, self.path)
    
    def read(self):
        try:
            self.info = load_obj(self.path)
        
        except:
            self.info = player_info_class()
            self.save()
