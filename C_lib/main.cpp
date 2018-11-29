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
char in_data[300]; // 입력될 16진수 문자열이 저장될 배열

void input(){
    file_pointer = fopen("/data/dev/school/network/checksum/C_lib/input.dat", "r");
    fscanf(file_pointer, "%s", in_data);
    fclose(file_pointer);
    printf("data : %s\n", in_data);
}

void engine(){
    unsigned long sum = 0;
    for(int i = 0; i < 11; i++){ // 입력 데이터의 길이에서 4를 나눈 수 만큼 반복
        char tmp[5];
        // tmp 배열에 다음 4글자씩 문자 형태로 저장하는 작업을 반복
        sscanf( in_data+(4*i) , "%4s\n", tmp);
        // tmp 배열에 담긴 4글자의 16진수 문자열을 정수형으로 변환 후 sum에 더해 저장
        sum += strtoul(tmp, 0, 16);
    }
    // 2의 16승, 17번째 비트가 1이되는 수보다 같거나 크다면 Carry가 발생한 상황
    while(sum >= pow(2.0, 16)){
        // Carry 부분 (sum >> 16)과 bit and 연산으로 도출된 마지막 16비트 부분 (sum & 0xffff)
        sum = (sum >> 16) + (sum & 0xffff);
    }
    // sum에 보수를 취하면 마지막 16비트를 제외한 부분도 전부 1이 된다
    // 마지막 16비트를 1로 채운 0xffff와 bit and 연산으로 마지막 16비트 부분만 도출해낸다
    unsigned long cs = (~sum) & 0xffff;
    printf("sum = %04lX\n", sum);
    printf("checksum = %04lX\n", cs);
}

void proj_checksum(){
    input();
    engine();
}