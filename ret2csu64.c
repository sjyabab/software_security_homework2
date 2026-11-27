#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

const char proof_message[] = "CTFWIKI_RET2CSU_OK\n";
static ssize_t (*call_table[1])(int, const void *, size_t) = {write};

__attribute__((naked, used)) void gadget_csu_pop(void) {
    __asm__("pop %rbx; pop %rbp; pop %r12; pop %r13; pop %r14; pop %r15; ret;");
}

__attribute__((naked, used)) void gadget_csu_call(void) {
    __asm__(
        "mov %r13d, %edi\n"
        "mov %r14, %rsi\n"
        "mov %r15, %rdx\n"
        "call *(%r12,%rbx,8)\n"
        "add $1, %rbx\n"
        "cmp %rbp, %rbx\n"
        "jne 1f\n"
        "add $8, %rsp\n"
        "pop %rbx\n"
        "pop %rbp\n"
        "pop %r12\n"
        "pop %r13\n"
        "pop %r14\n"
        "pop %r15\n"
        "ret\n"
        "1: ret\n");
}

__attribute__((naked, used)) void gadget_ret(void) { __asm__("ret;"); }

__attribute__((naked, noinline)) static void vulnerable(void) {
    __asm__ volatile(
        "push %rbp\n"
        "mov %rsp, %rbp\n"
        "sub $64, %rsp\n"
        "lea -64(%rbp), %rsi\n"
        "mov $512, %edx\n"
        "xor %edi, %edi\n"
        "call read@PLT\n"
        "leave\n"
        "ret\n");
}

__attribute__((used, noinline)) static void finish(void) {
    puts("[ret2csu64] cleanup chain returned normally");
    _exit(0);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("[ret2csu64] target ready; proof=%p\n", (const void *)proof_message);
    vulnerable();
    return 0;
}
