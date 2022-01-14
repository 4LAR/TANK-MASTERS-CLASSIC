
import asyncore

class server(asyncore.dispatcher):
    def __init__(self, addr='127.0.0.1', port=25565):
        self.addr = addr
        asyncore.dispatcher.__init__(self)
        self.create_socket(AF_INET, SOCK_STREAM)
        self.bind(('', port))
        self.listen(10)

        self.data = None

    def handle_accept(self):
        #start_time = time.time()
        try:
            conn, addr = self.accept()

            self.data = conn.recv(BUFFERSIZE)
            data = json.loads(self.data.decode('utf-8'))

            data_server = json.dumps(data).encode('utf-8')
            conn.send(data_server)
        except Exception as e:
            print(e)

    def update(self):
        pass

def run_handler(addr='127.0.0.1', port=25565):
    server(addr, port)
    asyncore.loop()

run_handler()
