/*
1. TCP Client in C (on Linux) and Multi Threaded Server in Python (on Windows): 
the client sends a message and the server displays the ip+port of each client, 
then sends "Message received" back.
*/

#include <sys/socket.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <netinet/ip.h>

char msg[55];
char receive[22];
struct sockaddr_in s;
int sfd, rc;

int main(int argc, char **argv){
    sfd = socket(AF_INET, SOCK_STREAM, 0);
    
    s.sin_family = AF_INET;
    s.sin_addr.s_addr = inet_addr("192.168.1.106");  // set the IP address of the server
    s.sin_port = htons(2222);

    rc = connect(sfd, (struct sockaddr *)&s, sizeof(s));

    while(1){
        printf("Enter message: ");
        fgets(msg,sizeof(msg),stdin);
        msg[strlen(msg)-1] = '\0';
        
        rc = send(sfd, msg, strlen(msg), 0);
        rc = recv(sfd, receive, 22, 0);
        printf(receive);
        printf("\n");
        if(!strcmp(msg,"close"))
            break;
    }
    return 0;
}