/*
2 UDP Client in C (on Linux) and Server in Python (on Windows): 
the client sends a message and the Server counts the vowels,
then sends the number back to the client who displays it.
*/

#include <netinet/ip.h>
#include <string.h>
#include <stdio.h>

int sfd;
struct sockaddr_in s;
int len = sizeof(struct sockaddr_in);

int main(int argc, char **argv){

    char msg[55];
    printf("Enter message: ");
    fgets(msg,sizeof(msg),stdin);
    msg[strlen(msg)-1] = '\0';
    
    int n = strlen(msg);

    sfd = socket(AF_INET, SOCK_DGRAM, 0);
    s.sin_family = AF_INET;
    s.sin_port = htons(2222);
    s.sin_addr.s_addr = inet_addr("192.168.1.106");

    sendto(sfd, msg, n, 0, (struct sockaddr *)&s, len);

    int answer = 0;

    recvfrom(sfd, &answer, sizeof(int), 0, (struct sockaddr *)&s, (unsigned int *)&len);
    //answer = ntohs(answer);  - not ok in this case

    printf("The message has %d vowels.\n", answer);
    return 0;
}
