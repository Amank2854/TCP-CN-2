#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <netdb.h>

int main()
{

    int newsocketfd, n;
    struct sockaddr_in server_addr;
    struct hostent *server;

    char buffer[256];

    // Creating socket
    int socketfd = socket(AF_INET, SOCK_STREAM, 0);
    if (socketfd < 0)
    {
        printf("There is an Error opening Socket\n");
        close(socketfd);
        exit(-1);
    }

    int port = 8918;
    char hostname[256];
    gethostname(hostname, sizeof(hostname));
    server = gethostbyname(hostname);

    if (server == NULL)
    {
        printf("Error, no such host\n");
        close(socketfd);
        exit(-1);
    }

    // Specifying address
    int size_serv = sizeof(server_addr);
    bzero((char *)&server_addr, size_serv);

    server_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&server_addr.sin_addr.s_addr, server->h_length);
    server_addr.sin_port = htons(port);

    // Connecting to the server
    int val = connect(socketfd, (struct sockaddr *)&server_addr, sizeof(server_addr));
    if (val < 0)
    {
        printf("Connection has been Failed\n");
        close(socketfd);
        exit(-1);
    }
    else
    {
        printf("Connected to server\n");
    }
    while (1)
    {

        // Reading input from user
        printf("Please enter the message to the server: ");
        bzero(buffer, 256);
        scanf("\n%[^\n]s", buffer);
        char s[256] = "Client1:";
        strcat(s,buffer);
        // Sending string to the server
        int len = strlen(s);
        n = send(socketfd, s, len, 0);
        if (n <= 0)
        {
            printf("Error on Writing buffer\n");
            close(socketfd);
            exit(-1);
        }

        bzero(buffer, 256);

        // Receiving output from the server
        n = recv(socketfd, buffer, 256, 0);
        if (n <= 0)
        {
            printf("Error on Reading buffer\n");
            close(socketfd);
            exit(-1);
        }

        // Printing the output and closing the connection
        printf("Server replied: %s\n", buffer);
    }
}