
from pathlib import Path
from common import *
from collections import Counter
from knotpy.tables.diagram_reader import load_diagrams
from knotpy.tables.invariant_reader import load_invariant_table
import knotpy as kp
from tqdm import tqdm

from itertools import product, chain


# not important, just some checks
print("v4")

kp.settings.allowed_moves = "r1,r2,r3,flype,flip"

input = Path("data/7-knotoids-groups-up-to-flip.txt")  # save PD codes of knotoids
data = kp.load_diagram_sets(input)

def all_four(k):
    return k.copy(), kp.flip(k, inplace=False), kp.mirror(k, inplace=False), kp.flip(kp.mirror(k, inplace=False), inplace=False)

for i, (a, b) in enumerate(data):

    a_ = all_four(a)
    b_ = all_four(b)

    print("Yamadas for first knotoid")
    for _ in a_:
        print(kp.yamada(kp.closure(_, True, True)))

    print("Yamadas for second knotoid")
    for _ in b_:
        print(kp.yamada(kp.closure(_, True, True)))


    print(f"Knotoid {i}/{len(data)}", end=" ", flush=True)

    a_simplified = [kp.simplify(_, 3, flype=False) for _ in a_]

    print(".", end="", flush=True)
    b_simplified = [kp.simplify(_, 3, flype=False) for _ in a_]
    print(".", flush=True)


    same = any(x == y for x, y in product(a_simplified, b_simplified))

    if not same:
        print("All different")
    else:
        print("Some are same")

    for _ in chain(a_simplified, b_simplified):
        if kp.number_of_link_components() > 1:
            print("Mutliple components")
        if kp.is_disjoint_union(_):
            print("Disjoint union")
        elif kp.is_connected_sum(_):
            print("Connected sum")
        elif len(kp.bridges(_)) > 2:
            print("Has bridge")


# kp.save_diagrams("7-groups", new_unique_diagrams)
# kp.save_diagram_sets(output_nonunique, new_non_unique_diagrams)
#
# kp.export_pdf_groups(new_non_unique_diagrams, Path("8-knotoids-groups-flip.pdf"), ignore_errors=True, arc_width=2.0)

