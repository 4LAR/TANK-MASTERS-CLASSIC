
def thread_multiplayer():
    while True:
        try:
            tcp_socket = socket(AF_INET, SOCK_STREAM)
            tcp_socket.connect(get_obj_display('net_code').addr)

            data = get_obj_display('net_code').data_send
            data = json.dumps(data).encode('utf-8')
            tcp_socket.send(data)

            data = tcp_socket.recv(BUFFERSIZE)
            get_obj_display('net_code').data_recive = json.loads(data.decode('utf-8'))

            tcp_socket.close()
        except Exception as e:
            print(e)
