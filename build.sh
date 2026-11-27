#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build

COMMON32=(-m32 -O0 -g -fno-pie -no-pie -fno-stack-protector -fno-omit-frame-pointer -fcf-protection=none -mpreferred-stack-boundary=2 -mincoming-stack-boundary=2 -Wno-deprecated-declarations)

gcc "${COMMON32[@]}" ret2text32.c -o build/ret2text32 -Wl,-z,relro
gcc "${COMMON32[@]}" ret2shellcode32.c -o build/ret2shellcode32 -Wl,-z,relro
gcc "${COMMON32[@]}" ret2syscall32.c -o build/ret2syscall32 -Wl,-z,relro
gcc "${COMMON32[@]}" ret2libc1_32.c -o build/ret2libc1_32 -Wl,-z,relro
gcc "${COMMON32[@]}" ret2libc2_32.c -o build/ret2libc2_32 -Wl,-z,relro

gcc -O0 -g -fno-pie -no-pie -fno-stack-protector -fno-omit-frame-pointer -fcf-protection=none ret2csu64.c -o build/ret2csu64 -Wl,-z,relro

echo "Built five IA-32 classroom targets and one x86-64 ret2csu target in build/."
