import knotpy as kp
from pathlib import Path
from tqdm import tqdm
kp.settings.allowed_moves = "r1,r2,r3,flype"
"""
(True, 'kiral', 'flippable') : 786
(True, 'akiral', 'flippable') : 5
(True, 2, 'flippable') : 1
(False, 2, 2) : 56
(False, 'kiral', 2) : 2


What we want:

1) Table of knotoids (flippable: T/F/U, Chiral: T/F/U)
4) How many knotoids are flippable/chiral + combination.
3) How strong are polynomials: kbsm, affine, arrow, mock, yamada
4) Print whole table.
5) Print smaller table.
6) print exceptions. 
"""

knotoids = kp.load_invariant_table(Path("data") / "10-knotoids-table.csv")

print("Loaded", len(knotoids), "knotoids.")
print("Crossings", set(len(knotoids[k]["diagram"]) for k in knotoids))

# figure out
print("Verifying Unlikely")

rot, irot = 0, 0
for k in tqdm([k for k in knotoids if knotoids[k]["rotatable"] == "unlikely"]):

    d = knotoids[k]["diagram"].copy()
    f = kp.flip(d, inplace=False)
    e = kp.reduce_equivalent_diagrams([d, f], depth=1, flype=True)

    rot += len(e) == 1
    irot += len(e) == 2
    if len(e) == 1:
        knotoids[k]["rotatable"] = "True"

print("From unilikely:", rot, "rotatable", irot, "non-rotatable")
# figure out
print("Verifying Unknown")

rot, irot = 0, 0
for k in tqdm([k for k in knotoids if knotoids[k]["rotatable"] == "unknown"]):

    d = knotoids[k]["diagram"].copy()
    f = kp.flip(d, inplace=False)
    e = kp.reduce_equivalent_diagrams([d, f], depth=2, flype=True)

    rot += len(e) == 1
    irot += len(e) == 2
    if len(e) == 1:
        knotoids[k]["rotatable"] = "True"


print("From unknown:", rot, "rotatable", irot, "non-rotatable")

kp.save_invariant_table(Path("data") / "11-knotoids-table.csv", knotoids)





# split the csv into separate csv's

import csv
import os
import sys
from collections import defaultdict

ALLOWED_A = {0, 1, 2, 3, 4, 5, 6, 7}

def parse_name(name: str):
    """
    Parse name formatted as 'a_b' where a is a single-digit integer and b is an integer.
    Returns (a, b) as ints.
    """
    if not name or "_" not in name:
        raise ValueError(f"Invalid name format (expected 'a_b'): {name!r}")

    a_str, b_str = name.split("_", 1)

    if len(a_str) != 1 or not a_str.isdigit():
        raise ValueError(f"Invalid 'a' part (expected single digit): {name!r}")

    try:
        a = int(a_str)
        b = int(b_str)
    except ValueError as e:
        raise ValueError(f"Invalid integer in name: {name!r}") from e

    return a, b


def split_csv(input_csv_path: str, output_dir: str = "results"):
    os.makedirs(output_dir, exist_ok=True)

    groups = defaultdict(list)  # a -> list of (b, row_dict)

    with open(input_csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("Input CSV appears to have no header.")

        if "name" not in reader.fieldnames:
            raise ValueError("Input CSV header must include a 'name' column.")

        fieldnames = reader.fieldnames

        for row_idx, row in enumerate(reader, start=2):  # 2 because header is line 1
            name = row.get("name", "")
            try:
                a, b = parse_name(name)
            except ValueError as e:
                raise ValueError(f"Row {row_idx}: {e}") from e

            if a in ALLOWED_A:
                groups[a].append((b, row))
            # else: ignore (including a==2 and anything outside 0..7)

    # Write outputs
    for a in sorted(ALLOWED_A):
        out_path = os.path.join(output_dir, f"knotoids-{a}.csv")
        rows = groups.get(a, [])
        rows.sort(key=lambda t: t[0])  # sort by b

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for _, row in rows:
                writer.writerow(row)

        print(f"Wrote {len(rows)} rows -> {out_path}")



split_csv(Path("data") / "11-knotoids-table.csv", output_dir="results")