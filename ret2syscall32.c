#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char binsh[] = "/bin/sh";

__attribute__((naked, used)) void gadget_pop_eax_ret(void) { __asm__("pop %eax; ret;"); }
__attribute__((naked, used)) void gadget_pop_ebx_ret(void) { __asm__("pop %ebx; ret;"); }
__attribute__((naked, used)) void gadget_pop_ecx_ret(void) { __asm__("pop %ecx; ret;"); }
__attribute__((naked, used)) void gadget_pop_edx_ret(void) { __asm__("pop %edx; ret;"); }
__attribute__((naked, used)) void gadget_int80_ret(void) { __asm__("int $0x80; ret;"); }

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

__attribute__((used, noinline)) static void retain_symbols(void) {
    if (getpid() == -1) execl("/bin/true", "true", NULL);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("[ret2syscall32] binsh=%p; syscall number for execve is 11\n", binsh);
    vulnerable();
    return 0;
}
