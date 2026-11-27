from __future__ import annotations

import re
import struct
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"


def symbols(binary: Path) -> dict[str, int]:
    text = subprocess.check_output(["nm", "-an", str(binary)], text=True)
    result: dict[str, int] = {}
    for line in text.splitlines():
        match = re.match(r"^([0-9a-fA-F]+)\s+\w\s+(\S+)$", line.strip())
        if match:
            result[match.group(2)] = int(match.group(1), 16)
    return result


def plt(binary: Path, name: str) -> int:
    text = subprocess.check_output(["objdump", "-d", str(binary)], text=True)
    match = re.search(rf"^\s*([0-9a-fA-F]+)\s+<{re.escape(name)}@plt>:", text, re.M)
    if not match:
        raise RuntimeError(f"{name}@plt not found in {binary.name}")
    return int(match.group(1), 16)


def p32(value: int) -> bytes:
    return struct.pack("<I", value)


def p64(value: int) -> bytes:
    return struct.pack("<Q", value)


def execute(binary: Path, chunks: list[bytes], followup: bytes = b"", delay: float = 0.15) -> tuple[int, str]:
    process = subprocess.Popen(
        [str(binary)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    assert process.stdin is not None and process.stdout is not None
    for chunk in chunks:
        process.stdin.write(chunk)
        process.stdin.flush()
        time.sleep(delay)
    if followup:
        process.stdin.write(followup)
        process.stdin.flush()
    process.stdin.close()
    output = process.stdout.read().decode("utf-8", errors="replace")
    status = process.wait(timeout=5)
    return status, output


def print_result(name: str, status: int, output: str, marker: str) -> None:
    print(output, end="" if output.endswith("\n") else "\n")
    if marker not in output:
        raise SystemExit(f"[FAIL] {name}: expected marker {marker!r}; exit={status}")
    print(f"[PASS] {name}: observed {marker} (exit={status})")
