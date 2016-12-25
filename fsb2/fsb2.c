#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char buf[512];
    printf("[+] buf = %p\n", buf);
    strncpy(buf, argv[1], sizeof(buf));
    printf(buf);
    putchar('\n');
    return 0;
}

void hack(){
  printf("書式文字列攻撃を使った呼び出しに成功\n");
}
