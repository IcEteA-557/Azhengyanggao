#!/usr/bin/env python3
"""Reference model for the J8 Lab 3 ALU.

The same model produces:
  * lab3/src/alu_expected.csv   (256 rows, every A/B/op combination)
  * the numbers used in the report tables and figures

Keeping one model avoids the classic problem of a report table that disagrees
with the VHDL.
"""

from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"

OP_NAMES = {0: "ADD", 1: "AND", 2: "XOR", 3: "SHR"}
OP7_NAMES = {
    0: "ADD",
    1: "SUB",
    2: "AND",
    3: "OR",
    4: "XOR",
    5: "SHR",
    6: "SHL",
    7: "RESERVED",
}


def model(a: int, b: int, op: int) -> tuple[int, int]:
    """Return (result, carry) for the four-operation ALU."""
    if op == 0:
        total = a + b
        return total & 0x7, 1 if total >= 8 else 0
    if op == 1:
        return a & b, 0
    if op == 2:
        return a ^ b, 0
    if op == 3:
        return a >> 1, 0
    raise ValueError(op)


def model7(a: int, b: int, op: int) -> tuple[int, int]:
    """Return (result, carry) for the seven-operation ALU."""
    if op == 0:
        total = a + b
        return total & 0x7, 1 if total >= 8 else 0
    if op == 1:
        return (a - b) & 0x7, 1 if a >= b else 0
    if op == 2:
        return a & b, 0
    if op == 3:
        return a | b, 0
    if op == 4:
        return a ^ b, 0
    if op == 5:
        return a >> 1, 0
    if op == 6:
        return (a << 1) & 0x7, 0
    if op == 7:
        return 0, 0
    raise ValueError(op)


def bits(value: int, width: int = 3) -> str:
    return format(value & ((1 << width) - 1), f"0{width}b")


def write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "A_dec",
                "A_bin",
                "B_dec",
                "B_bin",
                "op",
                "op_name",
                "result_bin",
                "result_dec",
                "carry",
            ]
        )
        for a in range(8):
            for b in range(8):
                for op in range(4):
                    result, carry = model(a, b, op)
                    writer.writerow(
                        [a, bits(a), b, bits(b), format(op, "02b"), OP_NAMES[op],
                         bits(result), result, carry]
                    )


if __name__ == "__main__":
    out = SRC / "alu_expected.csv"
    write_csv(out)
    print(f"wrote {out} ({sum(1 for _ in out.open()) - 1} rows)")
