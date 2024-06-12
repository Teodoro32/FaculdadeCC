using System.Net;
using System.Net.Sockets;
using System.Text;

class Server
{
    private Socket socket;
    private List<Socket> clientSockets = new List<Socket>();
    private Dictionary<Socket, Guid> clientIDs = new Dictionary<Socket, Guid>();
    
    public Server()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
    }

    public void OpenServer()
    {
        socket.Bind(new IPEndPoint(IPAddress.Any, 8000));
        socket.Listen(10);
        
        Console.WriteLine("Server started \n");

        while (true)
        {
            Socket clientSocket = socket.Accept();
            Guid clientID = GenerateClientID();
            clientSockets.Add(clientSocket);
            clientIDs.Add(clientSocket, clientID);

            new Thread(() => ReceiveMessage(clientSocket)).Start();
        }
    }

    private void ReceiveMessage(Socket clientSocket)
    {
        while (true)
        {
            byte[] buffer = new byte[1024];
            int bytesReceived = clientSocket.Receive(buffer);

            if (bytesReceived > 0)
            {
                string message = Encoding.UTF8.GetString(buffer, 0, bytesReceived);
                //Console.WriteLine("mensagem recebida no servidor" + message);
                BroadcastMessage(message, clientSocket);
            }
        }
    }

    private void BroadcastMessage(string message, Socket senderSocket)
    {
        foreach (Socket clientSocket in clientSockets)
        {
            if (clientIDs[clientSocket] != clientIDs[senderSocket])
            {
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                clientSocket.Send(buffer);
            }
        }
    }

    private Guid GenerateClientID()
    {
        return Guid.NewGuid();
    }
}