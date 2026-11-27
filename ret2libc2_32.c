#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char writable_area[32];

__attribute__((naked, used)) void gadget_pop3_ret(void) {
    __asm__("pop %ebx; pop %ecx; pop %edx; ret;");
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

__attribute__((used, noinline)) static void retain_plt_entries(void) {
    if (getpid() == -1) {
        system("/bin/true");
        exit(0);
    }
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("[ret2libc2] no /bin/sh string is stored in this target");
    vulnerable();
    return 0;
}
