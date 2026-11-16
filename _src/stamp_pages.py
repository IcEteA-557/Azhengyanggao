"""Stamp centred page numbers on every page except the title page."""
from pathlib import Path
import os
import fitz

HERE = Path(__file__).resolve().parent
LAB3 = HERE.parent

FILES = [
    "EE2000_Lab3_Report.pdf",
    "EE2000_Lab3_Report_中文版.pdf",
    "EE2000_Lab3_中文版.pdf",
    "EE2000_Lab3_检查点达成指南.pdf",
]

for name in FILES:
    path = LAB3 / name
    doc = fitz.open(path)
    for index, page in enumerate(doc):
        if index == 0:
            continue
        label = str(index + 1)
        size = 11
        width = fitz.get_text_length(label, fontname="times-roman", fontsize=size)
        x = (page.rect.width - width) / 2
        y = page.rect.height - 22
        page.insert_text((x, y), label, fontname="times-roman", fontsize=size, color=(0, 0, 0))
    tmp = path.with_suffix(".stamped.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, path)
    print(f"stamped {name}: {path.stat().st_size} bytes")
