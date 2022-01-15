
import asyncore

data_server = {}
for i in range(4):
    data_server[str(i)] = {}
    data_server[str(i)]['use'] = False
    data_server[str(i)]['pos'] = [0, 0]
    data_server[str(i)]['rotation'] = 0


class server(asyncore.dispatcher):
    def __init__(self, addr='127.0.0.1', port=25565):
        self.addr = addr
        asyncore.dispatcher.__init__(self)
        self.create_socket(AF_INET, SOCK_STREAM)
        self.bind(('', port))
        self.listen(10)

        self.data = None

    def get_id(self):
        for i in range(len(data_server)) :
            if not data_server[i]['use']:
                data_server[i]['use'] = True
                return i

        return False

    def handle_accept(self):
        global data_server
        try:
            conn, addr = self.accept()

            self.data = conn.recv(BUFFERSIZE)
            data = json.loads(self.data.decode('utf-8'))

            data_server[str(data['id'])]['pos'] = data['pos']
            data_server[str(data['id'])]['rotation'] = data['rotation']

            data_server_send = json.dumps(data_server).encode('utf-8')
            conn.send(data_server_send)
        except Exception as e:
            print(e)

    def update(self):
        pass

def run_handler(addr='127.0.0.1', port=25565):
    server(addr, port)
    asyncore.loop()

run_handler()
