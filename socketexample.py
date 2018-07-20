import socket
import threading

host = ''
port = 5555

input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
input_connection = None


def setup_input():
    try:
        input_socket.bind((host, port))
    except socket.error as e:
        print(str(e))
    input_socket.listen(5)
    connection, address = input_socket.accept()
    global input_connection
    input_connection = connection
    print(f'connected to : {address[0]} : {address[1]}')

def output():
    user_input_host = input('enter host: ')
    output_socket.connect((user_input_host, 5556))


input_conn_listener_thread = threading.Thread(target=setup_input)
user_input_thread = threading.Thread(target=output)
input_conn_listener_thread.start()
user_input_thread.start()








