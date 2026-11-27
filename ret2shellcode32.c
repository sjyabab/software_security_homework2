#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

static void *code_area;

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
    code_area = mmap((void *)0x41410000, 4096, PROT_READ | PROT_WRITE | PROT_EXEC,
                     MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
    if (code_area == MAP_FAILED) {
        perror("mmap");
        return 1;
    }
    printf("[ret2shellcode32] RWX area=%p; send 256 code bytes, then the overflow\n", code_area);
    if (read(STDIN_FILENO, code_area, 256) <= 0) return 1;
    vulnerable();
    return 0;
}
