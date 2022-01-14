
def thread_multiplayer():
    while True:
        try:
            tcp_socket = socket(AF_INET, SOCK_STREAM)
            tcp_socket.connect(get_obj_display('net_code').addr)

            data = get_obj_display('net_code').data_send
            data = json.dumps(data).encode('utf-8')
            tcp_socket.send(data)

            get_obj_display('net_code').data_recive = tcp_socket.recv(BUFFERSIZE)

            tcp_socket.close()
        except:
            pass
