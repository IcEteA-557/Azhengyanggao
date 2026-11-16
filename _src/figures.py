#!/usr/bin/env python3
"""Generate the vector figures used by the Lab 3 documents.

All figures are plain SVG so they stay sharp in the PDFs and can be edited
later.  Coordinates are chosen on a 760-840 px wide canvas; the CSS scales
them to the text width.
"""

from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs"
OUT.mkdir(exist_ok=True)

FONT = "Times New Roman, Songti SC, serif"
CJK = "Songti SC, STSong, serif"
INK = "#111111"
MUTED = "#555555"
LIGHT = "#f2f2f2"
ACCENT = "#1a4f8a"


def head(w: int, h: int, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n"
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker>'
        '<marker id="arrowm" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/></marker></defs>\n'
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>\n'
    )


def t(x, y, s, size=11, anchor="start", italic=False, bold=False, fill=INK, font=FONT):
    style = f'font-family="{font}" font-size="{size}" fill="{fill}"'
    if italic:
        style += ' font-style="italic"'
    if bold:
        style += ' font-weight="bold"'
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" {style}>{s}</text>\n'


def line(x1, y1, x2, y2, stroke=INK, width=1.1, dash=None, marker=False):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    arrow = ' marker-end="url(#arrow)"' if marker else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{width}"{extra}{arrow}/>\n'
    )


def rect(x, y, w, h, fill="none", stroke=INK, width=1.1, rx=2):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>\n'
    )


def poly(points, fill="none", stroke=INK, width=1.1):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>\n'


def path(d, stroke=INK, width=1.1, fill="none", dash=None, marker=False):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    arrow = ' marker-end="url(#arrow)"' if marker else ""
    return (
        f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"'
        f"{extra}{arrow}/>\n"
    )


def dot(x, y, r=2.6, fill=INK):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>\n'


# ---------------------------------------------------------------- block diagram
def fig_block() -> str:
    s = head(760, 300, "3-bit ALU block diagram")
    s += rect(270, 66, 220, 174, fill="#fafafa")
    s += t(380, 112, "3-bit ALU", 15, "middle", bold=True)
    s += t(380, 132, "combinational logic", 10, "middle", italic=True, fill=MUTED)
    s += t(380, 162, "one operation selected by op[1:0]", 9.5, "middle")
    s += t(380, 186, "ADD   AND   XOR   SHR", 10, "middle", bold=True)

    for y, label in ((96, "A[2:0]"), (156, "B[2:0]"), (216, "op[1:0]")):
        s += t(40, y - 8, label, 11)
        s += line(96, y, 266, y, marker=True)

    for y, label in ((96, "result[2:0]"), (146, "carry"),
                     (190, "dup_result[2:0]"), (226, "dup_carry")):
        s += line(494, y, 560, y, marker=True)
        s += t(570, y + 4, label, 11)

    s += t(380, 262, "dup_result and dup_carry repeat the same values on JA1–JA4", 9.5, "middle", italic=True, fill=MUTED)
    s += t(380, 280, "so the logic analyser can observe the LED outputs.", 9.5, "middle", italic=True, fill=MUTED)
    s += "</svg>\n"
    return s


# ---------------------------------------------------------------- datapath
def fig_datapath() -> str:
    s = head(840, 470, "ALU datapath")
    # input buses
    s += t(22, 60, "A[2:0]", 11)
    s += t(22, 90, "B[2:0]", 11)
    s += line(68, 54, 92, 70)
    s += line(68, 84, 92, 98)
    s += line(92, 70, 92, 344)
    s += line(126, 98, 126, 344)
    s += t(78, 116, "3", 9, "middle", italic=True, fill=MUTED)

    # operation blocks
    blocks = [
        (200, 38, 150, 66, "4-bit adder", "sum = A + B"),
        (200, 138, 150, 50, "AND", "A and B"),
        (200, 214, 150, 50, "XOR", "A xor B"),
        (200, 290, 150, 50, "SHR", "A srl 1 (logical)"),
    ]
    for x, y, w, h, title, sub in blocks:
        s += rect(x, y, w, h, fill=LIGHT)
        s += t(x + w / 2, y + 24, title, 11.5, "middle", bold=True)
        s += t(x + w / 2, y + 41, sub, 9.5, "middle", italic=True, fill=MUTED)

    # A/B to adder
    s += line(92, 70, 196, 70, marker=True)
    s += line(126, 98, 196, 98, marker=True)
    # A/B to AND
    s += dot(92, 156); s += line(92, 156, 196, 156, marker=True)
    s += dot(126, 174); s += line(126, 174, 196, 174, marker=True)
    # A/B to XOR
    s += dot(92, 232); s += line(92, 232, 196, 232, marker=True)
    s += dot(126, 250); s += line(126, 250, 196, 250, marker=True)
    # A to SHR
    s += dot(92, 308); s += line(92, 308, 196, 308, marker=True)

    # operation outputs into the select block
    s += line(350, 70, 430, 70); s += line(430, 70, 430, 130); s += line(430, 130, 496, 130, marker=True)
    s += t(360, 64, "tmp[3:0]", 9, fill=MUTED)
    s += line(350, 163, 430, 163); s += line(430, 163, 430, 180); s += line(430, 180, 496, 180, marker=True)
    s += line(350, 239, 430, 239); s += line(430, 239, 430, 230); s += line(430, 230, 496, 230, marker=True)
    s += line(350, 315, 430, 315); s += line(430, 315, 430, 280); s += line(430, 280, 496, 280, marker=True)

    # select block
    s += rect(500, 110, 112, 250, fill="#fdfdfd")
    s += t(556, 190, "result /", 11, "middle", bold=True)
    s += t(556, 207, "carry", 11, "middle", bold=True)
    s += t(556, 224, "select", 11, "middle", bold=True)
    s += t(556, 252, "op[1:0]", 9, "middle", italic=True, fill=MUTED)
    s += line(556, 420, 556, 364, marker=True)
    s += t(566, 410, "op[1:0]", 10)

    # outputs
    s += line(612, 150, 668, 150, marker=True)
    s += t(678, 154, "result[2:0]", 11)
    s += line(612, 210, 668, 210, marker=True)
    s += t(678, 214, "carry", 11)
    s += line(612, 280, 668, 280, marker=True)
    s += t(678, 284, "dup_result[2:0]", 11)
    s += line(612, 330, 668, 330, marker=True)
    s += t(678, 334, "dup_carry", 11)

    s += t(420, 452, "tmp(3) becomes the carry for ADD; the other operations force carry = 0.", 9, "middle", italic=True, fill=MUTED)
    s += "</svg>\n"
    return s


# ---------------------------------------------------------------- waveform helper
def bus_wave(x0, x1, y, value, h=11, size=10):
    """Hexagon-style bus segment with the value written in the middle."""
    return (
        f'<polygon points="{x0},{y} {x0 + 7},{y - h} {x1 - 7},{y - h} '
        f'{x1},{y} {x1 - 7},{y + h} {x0 + 7},{y + h}" '
        f'fill="#ffffff" stroke="{INK}" stroke-width="0.9"/>\n'
        + t((x0 + x1) / 2, y + 3.5, value, size, "middle")
    )


def bit_wave(x0, x1, y, high, amp=9):
    yh, yl = y - amp, y + amp
    if high:
        return line(x0, yh, x1, yh, width=1.3)
    return line(x0, yl, x1, yl, width=1.3)


def fig_cp1() -> str:
    s = head(840, 480, "Checkpoint 1 simulation waveform")
    x0, x1 = 120, 780
    seg = (x1 - x0) / 4
    phases = ["ADD", "AND", "XOR", "SHR"]
    rows = [
        ("A[2:0]", 70, ["101"] * 4, "bus"),
        ("B[2:0]", 125, ["011"] * 4, "bus"),
        ("op[1:0]", 180, ["00", "01", "10", "11"], "bus"),
        ("result[2:0]", 235, ["000", "001", "110", "010"], "bus"),
        ("carry", 300, [1, 0, 0, 0], "bit"),
        ("dup_result[2:0]", 355, ["000", "001", "110", "010"], "bus"),
        ("dup_carry", 420, [1, 0, 0, 0], "bit"),
    ]
    # phase labels and grid
    for i, name in enumerate(phases):
        cx = x0 + seg * (i + 0.5)
        s += t(cx, 38, name, 10, "middle", bold=True, fill=ACCENT)
    for i in range(5):
        x = x0 + seg * i
        s += line(x, 48, x, 438, stroke="#bbbbbb", width=0.7, dash="3,3")
        s += t(x, 458, str(i * 10), 9.5, "middle", fill=MUTED)
    s += t(x0 - 10, 458, "ns", 9.5, "end", fill=MUTED)

    # cursor first, so that the white bus bodies and the bit traces cover it
    xc = x0 + seg * 3.5
    s += line(xc, 48, xc, 438, stroke="#b00020", width=1, dash="5,3")

    for label, y, values, kind in rows:
        s += t(24, y + 4, label, 10.5)
        s += line(x0, y, x1, y, stroke="#dddddd", width=0.6)
        for i, value in enumerate(values):
            a, b = x0 + seg * i, x0 + seg * (i + 1)
            if kind == "bus":
                s += bus_wave(a, b, y, value)
            else:
                s += bit_wave(a, b, y, bool(value))
                if i and value != values[i - 1]:
                    s += line(a, y - 9, a, y + 9, width=1.3)

    s += t(130, 26, "cursor at 35 ns: result = 010", 9, fill="#b00020")
    s += "</svg>\n"
    return s


def fig_cp4() -> str:
    s = head(840, 420, "Logic analyser capture")
    x0, x1 = 120, 790
    seg = (x1 - x0) / 10
    d0 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]
    d1 = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
    d2 = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
    d3 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    rows = [("D0  JA1  result[0]", 80, d0), ("D1  JA2  result[1]", 145, d1),
            ("D2  JA3  result[2]", 210, d2), ("D3  JA4  carry", 290, d3)]

    # pre-trigger shading
    s += rect(x0, 55, seg, 285, fill="#f0f0f0", stroke="none")

    for label, y, values in rows:
        s += t(20, y + 4, label, 10)
        s += line(x0, y + 10, x1, y + 10, stroke="#dddddd", width=0.6)
        for i, value in enumerate(values):
            a, b = x0 + seg * i, x0 + seg * (i + 1)
            s += bit_wave(a, b, y, bool(value))
            if i and value != values[i - 1]:
                s += line(a, y - 9, a, y + 9, width=1.2)

    # trigger marker at the 0 -> 1 edge of D0
    xt = x0 + seg
    s += line(xt, 55, xt, 340, stroke="#b00020", width=1.2, dash="5,3")
    s += t(xt + 4, 50, "D0 rising = trigger", 9, fill="#b00020")

    # A values under the sweep
    s += t(x0 - 20, 380, "A =", 9, "end", fill=MUTED)
    for i in range(8):
        s += t(x0 + seg * (i + 0.5), 380, str(i), 9.5, "middle", fill=MUTED)
    s += t(x0 + seg * 4, 398, "A sweeps 000 → 111, B = 000", 9, "middle", italic=True)
    s += t(x0 + seg * 9, 398, "B = 001, A = 111", 9, "middle", italic=True)

    # time axis
    for i in range(11):
        x = x0 + seg * i
        s += line(x, 342, x, 350, width=0.8)
        s += t(x, 360, str(i), 8.5, "middle", fill=MUTED)
    s += t(x1 + 6, 360, "ms", 8.5, fill=MUTED)
    s += t(420, 416, "5 M samples at 1 MHz = 5 s window; the sketch shows the first 10 ms.", 9, "middle", italic=True, fill=MUTED)
    s += "</svg>\n"
    return s


# ---------------------------------------------------------------- board map
def fig_board() -> str:
    s = head(820, 440, "Basys 3 pin map for the ALU")
    s += rect(60, 30, 600, 320, fill="#f7f7f7", rx=10)
    s += t(360, 58, "Basys 3", 14, "middle", bold=True)
    s += t(360, 76, "xc7a35tcpg236-1", 9.5, "middle", italic=True, fill=MUTED)

    # switches SW0..SW7
    sw_pins = ["V17", "V16", "W16", "W17", "W15", "V15", "W14", "W13"]
    for i in range(8):
        x = 110 + i * 44
        s += rect(x, 240, 26, 50, fill="#ffffff")
        s += t(x + 13, 231, sw_pins[i], 6.8, "middle", fill=MUTED)
        s += t(x + 13, 307, f"SW{i}", 8.2, "middle")

    # LEDs LD0..LD3
    for i in range(4):
        x = 470 + i * 39
        s += f'<circle cx="{x}" cy="112" r="9" fill="#ffffff" stroke="{INK}" stroke-width="1.2"/>\n'
        s += t(x, 139, f"LD{i}", 8.2, "middle")

    # JA header
    s += rect(658, 168, 42, 110, fill="#ffffff")
    for i in range(6):
        y = 178 + i * 17
        s += f'<circle cx="{679}" cy="{y}" r="3" fill="{INK}"/>\n'
        s += t(706, y + 3, f"JA{i + 1}", 8, "start")
    s += t(679, 294, "JA", 9, "middle", bold=True)

    # colour legend under the board
    legend = [
        ("A[2:0] = SW2..SW0", "#1a4f8a", 356),
        ("B[2:0] = SW5..SW3", "#2e6b2e", 378),
        ("op[1:0] = SW7..SW6", "#a05a00", 400),
    ]
    for text, color, y in legend:
        s += rect(150, y - 8, 9, 9, fill=color, stroke=color)
        s += t(166, y, text, 9.5, "start", bold=True, fill=color)

    # result / carry labels
    s += t(466, 88, "result[2:0] = LD2..LD0", 8.8, "start", bold=True, fill="#8a1a1a")
    s += t(616, 116, "carry = LD3", 8.8, "start", bold=True, fill="#5a2a7a")

    s += t(360, 428, "All pins are 3.3 V; JA1–JA4 are J1, L2, J2, G2.", 9, "middle", italic=True, fill=MUTED)
    s += "</svg>\n"
    return s


# ---------------------------------------------------------------- seven operations
def fig_7ops() -> str:
    s = head(840, 540, "Seven-operation ALU")
    s += t(22, 62, "A[2:0]", 11)
    s += t(22, 92, "B[2:0]", 11)
    s += line(70, 56, 96, 72)
    s += line(70, 86, 96, 102)
    s += line(92, 50, 92, 452)
    s += line(140, 64, 140, 452)

    ops = [
        ("ADD", "sum = A + B", 40),
        ("SUB", "diff = A - B", 95),
        ("AND", "A and B", 150),
        ("OR", "A or B", 205),
        ("XOR", "A xor B", 260),
        ("SHR", "A srl 1", 315),
        ("SHL", "A sll 1", 370),
    ]
    for index, (name, sub, y) in enumerate(ops):
        s += rect(190, y, 150, 42, fill=LIGHT)
        s += t(265, y + 19, name, 11, "middle", bold=True)
        s += t(265, y + 34, sub, 8.5, "middle", italic=True, fill=MUTED)
        s += dot(92, y + 14)
        s += line(92, y + 14, 190, y + 14, marker=True)
        if index < 5:
            s += dot(140, y + 28)
            s += line(140, y + 28, 190, y + 28, marker=True)
        s += line(340, y + 14, 516, y + 14, marker=True)

    s += rect(516, 30, 88, 392, fill="#fdfdfd")
    s += t(560, 22, "8:1 MUX", 10.5, "middle", bold=True)
    s += line(620, 422, 564, 422, marker=True)
    s += t(624, 426, "op[2:0]", 10)

    # carry logic
    s += rect(190, 455, 150, 42, fill=LIGHT)
    s += t(265, 474, "carry logic", 10.5, "middle", bold=True)
    s += t(265, 490, "sum(3) or not diff(3)", 8.5, "middle", italic=True, fill=MUTED)
    s += line(340, 476, 516, 476, marker=True)
    s += rect(516, 455, 88, 42, fill="#fdfdfd")
    s += t(560, 481, "carry MUX", 8.5, "middle", bold=True)

    # outputs
    s += line(604, 110, 660, 110, marker=True)
    s += t(670, 114, "result[2:0]", 11)
    s += line(604, 150, 660, 150, marker=True)
    s += t(670, 154, "dup_result[2:0]", 11)
    s += dot(630, 110); s += line(630, 110, 630, 150); s += line(630, 150, 660, 150, marker=True)
    s += line(604, 476, 660, 476, marker=True)
    s += t(670, 480, "carry", 11)
    s += line(604, 510, 660, 510, marker=True)
    s += t(670, 514, "dup_carry", 11)
    s += dot(630, 476); s += line(630, 476, 630, 510); s += line(630, 510, 660, 510, marker=True)

    s += line(620, 497, 564, 497, marker=True)
    s += t(624, 501, "op[2:0]", 10)
    s += t(330, 536, "op = 111 is reserved and drives result = 000, carry = 0", 9, "middle", italic=True, fill=MUTED)
    s += "</svg>\n"
    return s


# ---------------------------------------------------------------- flow
def fig_flow() -> str:
    s = head(760, 180, "Lab 3 workflow")
    steps = [("1", "写 VHDL", "alu.vhd"), ("2", "仿真", "XSim"), ("3", "综合", "Synthesis"),
             ("4", "实现", "Implementation"), ("5", "下载", "Program"), ("6", "验证", "Board + LA")]
    for i, (num, title, sub) in enumerate(steps):
        x = 20 + i * 122
        s += rect(x, 55, 100, 62, fill="#f7f7f7")
        s += t(x + 12, 74, num, 9, fill=MUTED)
        s += t(x + 50, 90, title, 10.5, "middle", bold=True)
        s += t(x + 50, 107, sub, 8.5, "middle", italic=True, fill=MUTED)
        if i < 5:
            s += line(x + 102, 86, x + 118, 86, marker=True)
    s += t(380, 150, "Each step has a checkpoint or a report artefact; the source and PDFs live in the same repository.", 9, "middle", italic=True, fill=MUTED)
    s += "</svg>\n"
    return s


def main() -> None:
    figures = {
        "fig_block.svg": fig_block(),
        "fig_datapath.svg": fig_datapath(),
        "fig_cp1.svg": fig_cp1(),
        "fig_cp4.svg": fig_cp4(),
        "fig_board.svg": fig_board(),
        "fig_7ops.svg": fig_7ops(),
        "fig_flow.svg": fig_flow(),
    }
    for name, content in figures.items():
        path = OUT / name
        path.write_text(content, encoding="utf-8")
        print(f"{name}: {len(content)} bytes")


if __name__ == "__main__":
    main()
