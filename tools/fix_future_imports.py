# tools/fix_future_imports.py
"""
Moves `from __future__ import annotations` to the earliest legal spot in app/safety/safety.py:
- Keeps an optional module docstring at very top
- Ensures no code/imports appear before the future import
- De-duplicates repeated future imports
- Writes a .bak backup
"""
from __future__ import annotations
from pathlib import Path
import re

p = Path("app/safety/safety.py")
src = p.read_text(encoding="utf-8")

lines = src.splitlines(keepends=True)
docstring_end_idx = None

# Detect leading docstring ("""...""" or '''...'''), must be first non-empty token
joined = "".join(lines)
# quick tokenization of the top region
i = 0
while i < len(lines) and lines[i].strip() == "":
    i += 1

def is_doc_start(line: str) -> bool:
    s = line.lstrip()
    return (s.startswith('"""') or s.startswith("'''"))

if i < len(lines) and is_doc_start(lines[i]):
    quote = '"""' if lines[i].lstrip().startswith('"""') else "'''"
    # find end of docstring
    j = i
    found_end = False
    if lines[i].count(quote) >= 2 and lines[i].strip().endswith(quote) and len(lines[i].strip()) > 3:
        # one-line docstring """..."""
        docstring_end_idx = i
        found_end = True
    else:
        j += 1
        while j < len(lines):
            if quote in lines[j]:
                docstring_end_idx = j
                found_end = True
                break
            j += 1
    if not found_end:
        # malformed docstring; treat as no docstring
        docstring_end_idx = None

# Remove any existing future lines; we will reinsert one
future_re = re.compile(r"^\s*from\s+__future__\s+import\s+annotations\s*$")
kept = []
had_future = False
for line in lines:
    if future_re.match(line.strip()):
        had_future = True
        continue
    kept.append(line)

# If no future import existed, we still want to add it
insert_lines = kept[:]
header = []
tail_start = 0
if docstring_end_idx is not None:
    # keep everything up to docstring end
    header = kept[:docstring_end_idx + 1]
    tail_start = docstring_end_idx + 1
else:
    # keep leading blank/comment lines only
    k = 0
    while k < len(kept) and (kept[k].strip() == "" or kept[k].lstrip().startswith("#")):
        k += 1
    header = kept[:k]
    tail_start = k

body = kept[tail_start:]

# Ensure exactly one blank line after future import
future_block = ["from __future__ import annotations\n", "\n"]

new_src = "".join(header + future_block + body)

# Avoid duplicate blank lines
new_src = re.sub(r"\n{3,}", "\n\n", new_src)

# Write backup and file
p.with_suffix(".py.bak").write_text(src, encoding="utf-8")
p.write_text(new_src, encoding="utf-8")
print("Fixed header for:", p)
