
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

print("v2")
kp.settings.allowed_moves = "r1,r2,r3,flype,flip"

input = Path("data/5-knotoids-groups.txt")  # save PD codes of knotoids
output_unique = Path("data/6-knotoids-unique-up-to-flip.txt")  # save PD codes of knotoids
output_nonunique = Path("data/6-knotoids-groups-up-to-flip.txt")  # save PD codes of knotoids

data = kp.load_diagram_sets(input)

print("Simplify groups...")
new_unique_diagrams = []
new_non_unique_diagrams = []
for group in tqdm(data):
    # print(f"Group of length {len(group)} []")
    eq = kp.reduce_equivalent_diagrams(group, depth=2, flype=True)

    if len(eq) == 1:
        new_unique_diagrams.append(list(eq.keys())[0])
    else:
        new_non_unique_diagrams.append(list(eq.keys()))


print("Unique diagrams:", len(new_unique_diagrams))
print("Non-unique diagrams:", len(new_non_unique_diagrams))
print("Distribution:")
print(Counter(len(g) for g in new_non_unique_diagrams))

kp.save_diagrams(output_unique, new_unique_diagrams)
kp.save_diagram_sets(output_nonunique, new_non_unique_diagrams)

kp.export_pdf_groups(new_non_unique_diagrams, Path("plot/6-knotoids-groups-flip.pdf"), ignore_errors=True, arc_width=2.0)


"""


Unique diagrams: 684
Non-unique diagrams: 68
Distribution:
Counter({2: 54, 3: 11, 4: 3})
0.25 False
0.25 False
0.25 False
0.25 False
0.25 False
0.25 False
Traceback (most recent call last):


"""