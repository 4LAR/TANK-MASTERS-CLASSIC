import threading

class net_code():
    def __init__(self, host='127.0.0.1', port=25565):
        self.addr = (host,port)

        #self.client = client(host='127.0.0.1', port=25565)

        self.data_send = {}
        self.data_recive = {}

        self.thread_2 = threading.Thread(target=thread_multiplayer)
        self.thread_2.start()

    def update(self):
        self.data_send = {
            'id': get_obj_display('players').tanks[0].id,
            'name': get_obj_display('players').tanks[0].name,
            'pos': get_obj_display('players').tanks[0].pos,
            'bullets': []
        }
