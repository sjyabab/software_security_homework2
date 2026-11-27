from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "exp_ret2text32.py",
    "exp_ret2shellcode32.py",
    "exp_ret2syscall32.py",
    "exp_ret2libc1_32.py",
    "exp_ret2libc2_32.py",
    "exp_ret2csu64.py",
]

for script in SCRIPTS:
    print(f"\n$ python3 {script}", flush=True)
    subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)

print("\nAll six local ROP demonstrations completed successfully.")
