#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <string.h>
#include <sys/types.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <ctype.h>
#include <sys/wait.h>
#include <time.h>

#define MAX_MSG_SIZE 100

double evaluate_postfix(char *postfix)
{
    char arr[256]= {'\0'};
    strcpy(arr, postfix);
    double stack[MAX_MSG_SIZE];
    int top = -1;
    char *token = strtok(arr, " ");
    while (token != NULL)
    {
        if (isdigit(token[0]) || token[0] == '-' && isdigit(token[1]))
        {
            stack[++top] = atof(token);
        }
        else
        {
            double operand2 = stack[top--];
            double operand1 = stack[top--];
            double result;
            switch (token[0])
            {
            case '+':
                result = operand1 + operand2;
                break;
            case '-':
                result = operand1 - operand2;
                break;
            case '*':
                result = operand1 * operand2;
                break;
            case '/':
                result = operand1 / operand2;
                break;
            default:
                printf("Invalid operator: %c\n", token[0]);
                return 0.0;
            }
            stack[++top] = result;
        }
        token = strtok(NULL, " ");
    }
    return stack[top];
}

int main()
{
    int port = 8918; // Port Number of server
    pthread_mutex_t mutex;
    int n;
    char buffer[256];
    struct sockaddr_in serv_addr;

    // Creating server socket
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
    {
        perror("Socket Creation has been Failed\n");
        return 0;
    }
    int len = sizeof(serv_addr);
    bzero((char *)&serv_addr, len);

    // Specifying Server Address
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(port);

    // Binding the socket
    len = sizeof(serv_addr);
    int val = bind(sockfd, (struct sockaddr *)&serv_addr, len);
    if (val < 0)
    {
        perror("Binding has been Failed.\n");
        return 0;
    }
    else
    {
        printf("Successfully Binded\n");
    }

    // Listening for connections
    if (listen(sockfd, 10) < 0)
    {
        perror("Error in Listen\n");
        return 0;
    }

    while (1)
    {
        struct sockaddr_in caddr;

        printf("Waiting for incoming connections...\n");

        int clen = sizeof(caddr);
        // Listening incomming connections
        int clientfd = accept(sockfd, (struct sockaddr *)&caddr, &clen);

        if (clientfd < 0)
        {
            perror("Error on Accept.\n");
            continue;
        }

        pid_t pid = fork();
        if (pid == -1)
        {
            perror("Failed to fork");
            close(clientfd);
            continue;
        }
        else if (pid == 0)
        {
            while (1)
            {

                pthread_mutex_lock(&mutex);

                bzero(buffer, 256);
                char *buff_rec = buffer;
                time_t start_time,end_time;

                // Receiving request from client
                time(&start_time);
                n = recv(clientfd, buffer, 256, 0);
                if (n < 0)
                {
                    perror("Error on Receiving Buffer.\n");
                    continue;
                }
                char *pos_1 = strstr(buffer, ":");
                char buf[1024];
                sscanf(pos_1 + 1, "%[^\n]s", buf);
                double output = evaluate_postfix(buf);

                char *str = strstr(buffer, "t");
                int clientid = str[1] - '0';

                int writefd = open("server_records.txt", O_WRONLY | O_APPEND);
                if (writefd == -1)
                {
                    perror("Failed to open the file");
                    exit(0);
                }

                char strbuf1[2048];
                char *client_write_Val;
                time(&end_time);
                int time_taken = (int)difftime(end_time, start_time);
                sprintf(strbuf1, "%d %s %.2f %d\n", clientid, buf, output, time_taken);

                client_write_Val = strbuf1;
                int len1 = strlen(client_write_Val);
                write(writefd, client_write_Val, len1);

                sprintf(buffer, "%.2f", output);
                close(writefd);

                // Sending the ouput to client
                int len3 = strlen(buffer);
                n = send(clientfd, buffer, len3, 0);
                if (n < 0)
                {
                    perror("Error on Sending.\n");
                    continue;
                }

                bzero(buffer, 256);
                pthread_mutex_unlock(&mutex);
            }
        }
        else
        {
            close(clientfd);
        }
    }
    close(sockfd);
}
