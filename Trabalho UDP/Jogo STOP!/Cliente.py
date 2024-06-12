import socket

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect((host, port))
    return client_socket

def send_nick(client_socket, host, port):
    nick = input("Digite seu nome: ")
    client_socket.sendto(nick.encode(), (host, port))
    return nick

def receive_player_list(client_socket):
    players_received = 0
    player_list = ""
    while True:
        player_list_received, _ = client_socket.recvfrom(1024)
        player_list = player_list_received.decode()
        print(f"Jogadores na partida: {player_list}")
        players_received = len(player_list.split(", "))
        if players_received == 4:
            break

def receive_letter(client_socket):
    letter_received, _ = client_socket.recvfrom(1024)
    print(f"A letra aleatória é {letter_received.decode()}")

def receive_form_data():
    form_data = {}
    form_data["Nome"] = input("Nome: ") + "\n"
    form_data["Cidade"] = input("Cidade: ") + "\n"
    form_data["País"] = input("País: ") + "\n"
    form_data["Animal"] = input("Animal: ") + "\n"
    form_data["Objeto"] = input("Objeto: ") + "\n    		  |===>"
    return form_data

def send_form_data(client_socket, form_data, nick, host, port):
    form_data["Remetente"] = nick + "\n____________________________________________\n\n"
    form_string = ", ".join([f"{key}: {value}" for key, value in form_data.items()])
    client_socket.sendto(form_string.encode(), (host, port))

def receive_result(client_socket):
    print("Aguardando resultado...")
    result_received, _ = client_socket.recvfrom(1024)
    print("Resultado recebido:\n____________________________________________\n", result_received.decode())

def close_connection(client_socket):
    client_socket.close()

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = connect_to_server(host, port)
    
    nick = send_nick(client_socket, host, port)

    receive_player_list(client_socket)

    receive_letter(client_socket)

    form_data = receive_form_data()

    send_form_data(client_socket, form_data, nick, host, port)

    receive_result(client_socket)

    input("Pressione Enter para fechar...")

    close_connection(client_socket)

if __name__ == "__main__":
    main()
