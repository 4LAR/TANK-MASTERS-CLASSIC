import threading

class net_code():
    def __init__(self, host='127.0.0.1', port=25565):
        self.addr = (host,port)

        self.data_send = {}
        self.data_recive = {}

        self.thread_2 = threading.Thread(target=thread_multiplayer)
        self.thread_2.start()

    def update(self):
        self.data_send = {
            'id': str(game_settings.multiplayer_id),
            'name': get_obj_display('players').tanks[game_settings.multiplayer_id].name,
            'pos': get_obj_display('players').tanks[game_settings.multiplayer_id].pos,
            'rotation': get_obj_display('players').tanks[game_settings.multiplayer_id].rotation,
            'bullets': []
        }

        for i in range(len(self.data_recive)):
            if i != game_settings.multiplayer_id:
                get_obj_display('players').tanks[i].pos = self.data_recive[str(i)]['pos']
                get_obj_display('players').tanks[i].rotation = self.data_recive[str(i)]['rotation']
