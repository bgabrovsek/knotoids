
from pathlib import Path
from common import *
from collections import Counter
from knotpy.tables.diagram_reader import load_diagrams
from knotpy.tables.invariant_reader import load_invariant_table
import knotpy as kp
from tqdm import tqdm
#
# data = kp.load_diagram_sets(Path("data/5-knotoids-groups.txt"))
# kp.export_pdf_groups(data, Path("plot/5-knotoids-groups.pdf"), ignore_errors=True, arc_width=2.0)
#
# exit()

print("v4")
kp.settings.allowed_moves = "r1,r2,r3,flype"

input = Path("data/4-knotoids-groups-stage-2.txt")  # save PD codes of knotoids
output_unique = Path("data/5-knotoids-unique.txt")  # save PD codes of knotoids
output_nonunique = Path("data/5-knotoids-groups.txt")  # save PD codes of knotoids

data = kp.load_diagram_sets(input)

print("Simplify groups...")
new_unique_diagrams = []
new_non_unique_diagrams = []
for group in tqdm(data):
    names = [g.name for g in group]
    # print(f"Group of length {len(group)} []")
    eq = kp.reduce_equivalent_diagrams(group, depth=2, flype=True)

    candidates = list(eq.keys())
    for name, c in zip(names, candidates):
        c.name = name

    if len(eq) == 1:
        new_unique_diagrams.append(candidates[0])
    else:
        new_non_unique_diagrams.append(candidates)

print("Unique diagrams:", len(new_unique_diagrams))
print("Non-unique diagrams:", len(new_non_unique_diagrams))
print("Distribution:")
print(Counter(len(g) for g in new_non_unique_diagrams))

kp.save_diagrams(output_unique, new_unique_diagrams)
kp.save_diagram_sets(output_nonunique, new_non_unique_diagrams)

