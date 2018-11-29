#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

void proj_checksum();
int main() {
    proj_checksum();
    return 0;
}

char inputstrtmp[] = "0019E77A753F001ECDA380019E77A3F1ECDA30350028";

char * inputstr(){
    return inputstrtmp;
}

FILE *file_pointer;
char in_data[300];

void input(){
    file_pointer = fopen("/data/dev/school/network/checksum/C_lib/input.dat", "r");
    fscanf(file_pointer, "%s", in_data);
    fclose(file_pointer);
    printf("data : %s\n", in_data);
}

void engine(){
    unsigned long bit16;
    unsigned long sum = 0;
    for(int i = 0; i < 11; i++){
        char tmp[5];
        char * itmp = in_data+(4*i);
        sscanf( in_data+(4*i) , "%c%c%c%c", tmp, tmp + 1, tmp + 2, tmp + 3);
        tmp[4] = '\0';
        bit16 = (unsigned) strtol(tmp, 0, 16);
        sum += bit16;
    }
    int s = (int) pow(2.0, 16);
    while(sum >= pow(2.0, 16)){
        unsigned long carry = sum >> 16;
        unsigned long origin = sum & 0xffff;
        sum = carry + origin;
    }
    unsigned long cksum = (~sum) & 0xffff;
    printf("sum = %X\n", sum);
    printf("checksum = %X\n", cksum);
}

void proj_checksum(){
    input();
    engine();
}