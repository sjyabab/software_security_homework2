#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((noinline, used)) void secure_shell(void) {
    system("/bin/sh");
    _exit(0);
}

__attribute__((naked, noinline)) static void vulnerable(void) {
    __asm__ volatile(
        "push %ebp\n"
        "mov %esp, %ebp\n"
        "sub $64, %esp\n"
        "lea -64(%ebp), %eax\n"
        "push $512\n"
        "push %eax\n"
        "push $0\n"
        "call read@PLT\n"
        "add $12, %esp\n"
        "leave\n"
        "ret\n");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("[ret2text32] local target ready; send 68 bytes then a return address");
    vulnerable();
    return 0;
}
