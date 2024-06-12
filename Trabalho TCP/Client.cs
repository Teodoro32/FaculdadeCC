using System.Net.Sockets;
using System.Text;

namespace TcpChat;

public class Client
{
    private Socket socket;
    private string nickname;


    public Client()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
    }

    public void RunClient()
    {
        socket.Connect("127.0.0.1", 8000);
        
        Console.WriteLine("Client started \n");

        Console.WriteLine("Say your name: ");
        nickname = Console.ReadLine();

        byte[] buffer = Encoding.UTF8.GetBytes(nickname + " joinned the chat!");
        socket.Send(buffer);

        new Thread(() => ReceiveMessage()).Start();
        new Thread(() => SendMessage()).Start();
    }

    private void ReceiveMessage()
    {
        while (true)
        {
            byte[] buffer = new byte[1024];
            int bytesReceived = socket.Receive(buffer);
            string message = Encoding.UTF8.GetString(buffer, 0, bytesReceived);
            Console.WriteLine("Mensagem recebida no client: " + message);
        }
    }

    private void SendMessage()
    {
        while (true)
        {
            string message = Console.ReadLine();
            byte[] buffer = Encoding.UTF8.GetBytes(nickname + ": " + message);
            socket.Send(buffer);
        }
    }
}