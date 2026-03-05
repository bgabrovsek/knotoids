"""
Convert PD codes of graphs to PD and native KP/EM codes of knotoids.
Remove knotoids that allow an unpoke R2 move.
Remove knotoids with more than 1 component (linkoids)
Put knotoids into canonical form and save them into gzipped files.
"""
from knotpy import number_of_link_components

print("version: 1.0")

from datetime import datetime
from pathlib import Path
from collections import defaultdict

import knotpy as kp
from common import *

MAX_NUMBER_OF_CROSSINGS = 7
DATA_FOLDER = Path("data")
#input = DATA_FOLDER / "graphs_pdcodes.txt"  # get PD codes of planar graphs
output = DATA_FOLDER / "1-all-knotoids.txt"  # save PD codes of knotoids
output_details = DATA_FOLDER / "1-all-knotoids-details.txt"  # save PD codes of knotoids
comment = f"Knotoids up to {MAX_NUMBER_OF_CROSSINGS} crossings from graphs with all possible crossing combinations"

if __name__ == "__main__":

    kp.settings.allowed_moves = "r1,r2,r3"
    stats = defaultdict(int)

    # Load graphs
    graphs__ = [ kp.load_diagrams(f"data/graphs/graphs{i}-knotoids.txt", "native") for i in [2,4,5,6,7,8,9]]
    graphs = [_ for g in graphs__ for _ in g]  # flatten

    #graphs = kp.load_diagrams(input, "pd")
    print(f"Loaded {len(graphs)} graphs having {min(len(g) for g in graphs)-2} to {max(len(g) for g in graphs)-2} crossings")

    # Put graphs in canonical form
    graphs = [g for g in graphs if len(g) - 2 <= MAX_NUMBER_OF_CROSSINGS]
    print(f"Using {len(graphs)} graphs having {min(len(g) for g in graphs)-2} to {max(len(g) for g in graphs)-2} crossings")

    stats["graphs"] = len(graphs)

    canonical_graphs = sorted({kp.canonical(g) for g in graphs})
    stats["canonical graphs"] = len(graphs)


    print("Phase 1: converting graphs to knotoids.")

    all_knotoids = set()
    # Convert graphs to knotoids
    # with kp.DiagramWriter(output, notation="native", comment=f"{comment} - {datetime.now().isoformat()}") as writer:
    counter = 0
    for g in kp.bar(canonical_graphs, comment="Graphs to knots"):
        # get all possible knotoids by changing signs
        knotoids = kp.vertices_to_crossings(g, all_crossing_signs=True)
        if number_of_link_components(knotoids[0]) > 1:
            continue

        knotoids += [kp.canonical(kp.flip(_)) for _ in knotoids] # also add flips
        knotoids = set(knotoids)

        for _ in knotoids:
            _.name = counter
            counter += 1

        all_knotoids.update(knotoids)
        stats["knotoids"] += len(knotoids)

    print("Phase 2: simplify + canonical")

    detailed_information = []

    all_canonical_knotoids = set()

    for k in kp.bar(all_knotoids):
        k_simplified = kp.canonical(kp.simplify_decreasing(k))
        if k_simplified in all_canonical_knotoids:
            k_pair = next(_ for _ in all_canonical_knotoids if _ == k_simplified) # get instance in set
            detailed_information.append(f"{k.name} was simplified to {k_pair.name}")
        else:
            all_canonical_knotoids.add(k_simplified)



    stats["simplified (decreasing)"] = len(all_canonical_knotoids)
    kp.clear_attributes(all_canonical_knotoids, exceptions=["name"])
    for _ in all_canonical_knotoids:
        print(_)

    lines = ["first line", "second line", "third line"]

    with open(output_details, "w") as f:
        f.writelines(line + "\n" for line in detailed_information)

    kp.save_diagrams(output, all_knotoids, comment=f"{comment} - {datetime.now().isoformat()}")

    print_stats(stats)

"""
16.2.2025
Loaded 2479 graphs having 0 to 7 crossings
Using 2479 graphs having 0 to 7 crossings
Phase 1: converting graphs to knotoids.

Phase 2: simplify + canonical
Diagram named 8400 a → V(b0), b → V(a0)
Stats:
graphs : 2479
canonical graphs : 2479
knotoids : 80729
simplified (decreasing) : 15343


WITH FLIPS:

graphs : 2479
canonical graphs : 2479
knotoids : 160825
simplified (decreasing) : 28447





"""