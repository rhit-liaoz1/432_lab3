/*client.c By Zeyu Liao and Doris Chen, 
**getting help from Week 3' lectures and Beej's Guide*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define PORT "3490"
#define MAXDATASIZE 100

bool readLine(char** line, size_t size, size_t* length);

/*supporting both IP4 and IP6*/
void *get_address(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(int argc, char *argv[])
{
    int sockfd, numbytes;  
    char buf[MAXDATASIZE];
    struct addrinfo hints, *servinfo, *p;
    int rv;
    char s[INET6_ADDRSTRLEN];

    

    if (argc != 3) {
        fprintf(stderr,"usage: client hostname\n");
        exit(1);
    }
    
    memset(&hints, 0, sizeof hints);
    /*go with either*/
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    if ((rv = getaddrinfo(argv[1], PORT, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    for(p = servinfo; p != NULL; p = p->ai_next) {
        if((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
            perror("client could not connect (socket)\n");
            close(sockfd);
            continue;
        }

        if(connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
            perror("client could not connect");
            close(sockfd);
            continue;
        }

        break;
    }

    if (p== NULL) {
        fprintf(stderr, "client: failed to connect\n");
        return 2;
    }

    inet_ntop(p->ai_family, get_address((struct sockaddr *)p->ai_addr), s, sizeof s);
    printf("client: connecting to %s\n", s);

    freeaddrinfo(servinfo);

    char* line = NULL;
    size_t size =0;
    size_t len;
    while(readLine(&line,&size,&len)){
        printf("\nSending string \"%s\"to server with '%d'\n",line,len);
        if(send(sockfd, line,len,0)==-1){
            perror("send error");
        }
        int lenr=0;
        int remain = len;
        //if(remain <=13){
        if ((numbytes = recv(sockfd, buf, MAXDATASIZE-1, 0)) == -1) {
        perror("receive error");
        exit(1);
        }
        
        buf[numbytes] = '\0';
        printf("client: received '%s'\n",buf);
        
        
       /* }else{
        while (remain > 0){
        if ((numbytes = recv(sockfd, buf, MAXDATASIZE-1, 0)) == -1) {
        perror("receive error");
        exit(1);
        }else{
            
            buf[numbytes] = '\0';
            remain =remain -13;
            printf("client: received '%s'remain '%d'\n",buf,remain);
            
        }
        
       }
        }*/
        
    };

    

    close(sockfd);

    return 0;

}

bool readLine(char** line, size_t size, size_t* length){
    while(1){
        printf("string for server> ");
        size_t len = getline(line, size, stdin);
        if(len == -1){
            return false;
        }

        if((*line)[len-1]=='\n'){
            (*line)[--len] ='\0';
        }
        *length =len;
        if(len ==0){
            continue;
        }
        return len > 1 || **line != '.';
    };
}
