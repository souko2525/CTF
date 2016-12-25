/* fsb.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char buf[512];
    char *pass;
    FILE *fp;
    
    //Fileを読み込む用のメモリを確保
    pass = malloc(2048);
    printf("[+] /etc/passwd = %p\n", pass);
    
    //ファイルを読み込み確保したメモリに書き込む
    fp = fopen("/etc/passwd", "r");
    fread(pass, 1, 2000, fp);
    fclose(fp);
    printf("length = %d\n", strlen(pass));

    //コマンドライン引数をbuffurに格納
    strncpy(buf, argv[1], sizeof(buf));
    
    //格納した内容を表示しているがここにフォーマット文字列攻撃の脆弱性
    printf(buf);

    //解放
    free(pass);
    return 0;
}
