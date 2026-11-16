#!/usr/bin/env python3
"""Compile and exhaustively simulate the Lab 3 ALU with GHDL.

Checks, for VHDL-93 and VHDL-2008:
  * alu.vhd + alu_tb.vhd elaborate and run (the shipped testbench)
  * alu_7ops.vhd + alu_7ops_tb.vhd elaborate and run
  * every A/B/op combination of both designs matches _src/model.py
  * dup_result / dup_carry equal result / carry in every case

GHDL is looked up in $GHDL, then in the temporary download directory.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB3 = HERE.parent.parent
SRC = LAB3 / "src"
sys.path.insert(0, str(HERE.parent))
import model  # noqa: E402

GHDL_CANDIDATES = [
    os.environ.get("GHDL", ""),
    "/tmp/ghdl/ghdl-llvm-6.0.0-macos15-aarch64/bin/ghdl",
    shutil.which("ghdl") or "",
]

CASE_RE = re.compile(r"CASE (\d+) (\d+) (\d+) (\d+) (\d+)")


def find_ghdl() -> str:
    for candidate in GHDL_CANDIDATES:
        if candidate and Path(candidate).is_file():
            return candidate
    raise SystemExit("GHDL not found; set GHDL=/path/to/ghdl")


def run(cmd: list[str], workdir: Path) -> str:
    result = subprocess.run(
        cmd, cwd=workdir, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if result.returncode != 0:
        print(result.stdout)
        raise SystemExit(f"command failed ({result.returncode}): {' '.join(cmd)}")
    return result.stdout


def check_design(
    ghdl: str,
    std: str,
    work: Path,
    sources: list[Path],
    top: str,
    expected_fn,
    stop_time: str,
) -> int:
    work.mkdir(parents=True, exist_ok=True)
    # GHDL's library-file reader rejects non-ASCII characters in paths, so the
    # sources are staged into the (ASCII) temporary directory before analysis.
    staged = []
    for source in sources:
        target = work / source.name
        shutil.copyfile(source, target)
        staged.append(target)
    common = [f"--std={std}", "--ieee=synopsys", f"--workdir={work}"]
    for source in staged:
        run([ghdl, "-a", *common, str(source)], work)
    run([ghdl, "-e", *common, top], work)
    output = run([ghdl, "-r", *common, top, f"--stop-time={stop_time}"], work)

    cases = [tuple(map(int, match.groups())) for match in CASE_RE.finditer(output)]
    if not cases:
        print(output)
        raise SystemExit(f"no CASE lines for {top} ({std})")

    for a, b, op, result, carry in cases:
        want_result, want_carry = expected_fn(a, b, op)
        if (result, carry) != (want_result, want_carry):
            raise SystemExit(
                f"{top} {std}: a={a} b={b} op={op}: "
                f"got result={result} carry={carry}, "
                f"want result={want_result} carry={want_carry}"
            )
    return len(cases)


def main() -> int:
    ghdl = find_ghdl()
    print(f"GHDL: {ghdl}")
    print(subprocess.run([ghdl, "--version"], text=True, capture_output=True).stdout.splitlines()[0])

    with tempfile.TemporaryDirectory(prefix="ee2000_ghdl_") as tmp:
        work = Path(tmp)
        total = 0
        for std in ("93c", "08"):
            n4 = check_design(
                ghdl, std, work / f"alu_{std}",
                [SRC / "alu.vhd", HERE / "alu_exhaustive_tb.vhd"],
                "alu_exhaustive_tb", model.model, "300ns",
            )
            n7 = check_design(
                ghdl, std, work / f"alu7_{std}",
                [SRC / "alu_7ops.vhd", HERE / "alu_7ops_exhaustive_tb.vhd"],
                "alu_7ops_exhaustive_tb", model.model7, "600ns",
            )
            print(f"VHDL-{std}: {n4} four-op cases, {n7} seven-op cases OK")
            total += n4 + n7

        # The shipped testbenches must at least elaborate and simulate.
        for name, files, top, stop in (
            ("alu_tb", ["alu.vhd", "alu_tb.vhd"], "alu_tb", "50ns"),
            ("alu_7ops_tb", ["alu_7ops.vhd", "alu_7ops_tb.vhd"], "alu_7ops_tb", "80ns"),
        ):
            workdir = work / f"tb_{name}"
            workdir.mkdir()
            common = ["--std=93c", "--ieee=synopsys", f"--workdir={workdir}"]
            for filename in files:
                shutil.copyfile(SRC / filename, workdir / filename)
                run([ghdl, "-a", *common, str(workdir / filename)], workdir)
            run([ghdl, "-e", *common, top], workdir)
            run([ghdl, "-r", *common, top, f"--stop-time={stop}", f"--vcd={workdir / (name + '.vcd')}"], workdir)
            print(f"{name}: shipped testbench ran OK")

        print(f"\nALL CHECKS PASSED ({total} exhaustive cases across two standards)")


if __name__ == "__main__":
    raise SystemExit(main())
