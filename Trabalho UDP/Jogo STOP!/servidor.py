import socket
import random

def bind_server_socket(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    return server_socket

def connect_players(server_socket):
    players = []
    remetentes = []

    while len(players) < 4:
        data, address = server_socket.recvfrom(1024)
        nick = data.decode()
        players.append((nick, address))
        remetentes.append(nick)
        print(f"Jogador {nick} se conectou - {len(players)}/4")

        for player in players:
            player_socket = player[1]
            player_list = ", ".join([p[0] for p in players])
            server_socket.sendto(player_list.encode(), player_socket)

    return players, remetentes

def choose_random_letter(server_socket, players):
    random_letter = chr(random.randint(65, 90))
    print(f"Letra escolhida: {random_letter}")

    for player in players:
        player_socket = player[1]
        server_socket.sendto(random_letter.encode(), player_socket)
        print(f"Letra enviada para {player[0]}")

def receive_player_data(server_socket, players):
    player_data = []
    for i, player in enumerate(players):
        player_socket = player[1]
        form_data, _ = server_socket.recvfrom(1024)
        player_data.append((form_data, player[0]))

    return player_data

def sort_and_format_player_data(player_data, remetentes):
    sorted_player_data = sorted(player_data, key=lambda x: remetentes.index(x[1]))
    result = "\n".join([f"{i + 1}° Lugar\nFormulário: {data[0].decode()}" for i, data in enumerate(sorted_player_data)])
    return result

def send_result_to_players(server_socket, players, result):
    for player in players:
        player_socket = player[1]
        server_socket.sendto(result.encode(), player_socket)

def main():
    print("Sessão iniciada")
    host = '127.0.0.1'
    port = 12345

    with bind_server_socket(host, port) as server_socket:
        players, remetentes = connect_players(server_socket)
        choose_random_letter(server_socket, players)
        player_data = receive_player_data(server_socket, players)
        result = sort_and_format_player_data(player_data, remetentes)
        send_result_to_players(server_socket, players, result)

if __name__ == "__main__":
    main()
