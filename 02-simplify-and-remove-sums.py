from pathlib import Path
from datetime import datetime
from collections import defaultdict
import knotpy as kp
from common import *
from time import time

print("version: 1.0")
input = Path("data/1-all-knotoids.txt")
output = Path("data/2-knotoids-simplified.txt")
output_disjoint = Path("data/2-knotoids-disjoint-sums.txt")
output_sums = Path("data/2-knotoids-connected-sums.txt")
output_multiple = Path("data/2-knotoids-connected-sums.txt")
output_bridges = Path("data/2-knotoids-bridges.txt")

if __name__ == "__main__":
    kp.settings.allowed_moves = "r1,r2,r3"
    stats = defaultdict(int)

    knotoids_sets = []
    #knotoids_1, knotoids_2, knotoids_3, knotoids_4 = set(), set(), set(), set()
    knotoids_connected_sums = []
    knotoids_disjoint_sums = []
    knotoids_multiple_components = []
    knotoids_bridges = []

    knotoids_sets.append(kp.load_diagrams(input))
    stats["knotoids (all)"] = len(knotoids_sets[0])

    for i, f in enumerate([
        lambda _: kp.simplify_non_increasing(_, greediness=0),
        lambda _: kp.simplify(_, depth=1),
        lambda _: kp.simplify(_, depth=1, flype=True),
        lambda _: kp.simplify(_, depth=2)
            ]):

        t = time()
        print("Phase:", i)
        new_knotoids = set()

        for k in kp.bar(knotoids_sets[-1]):
            k = kp.canonical(f(k))

            if kp.number_of_link_components(k) > 1:
                knotoids_multiple_components.append(k)
                stats["multiple components"] += 1
            elif kp.is_disjoint_union(k):
                knotoids_disjoint_sums.append(k)
                stats["disjoint sum"] += 1
            elif kp.is_connected_sum(k):
                stats["connected sum"] += 1
                knotoids_connected_sums.append(k)
            elif len(kp.bridges(k)) > 2:
                stats["bridges"] += 1
                knotoids_bridges.append(k)

            else:
                new_knotoids.add(k)

        knotoids_sets.append(new_knotoids)

        stats[f"level {i}"] = len(new_knotoids)
        print(f"Time level {i}:", time() - t)

    print("Saving simplified knotoids...")
    kp.save_diagrams(output,knotoids_sets[-1], comment=f"{datetime.now().isoformat()}")
    print("Saving connected sums...")
    kp.save_diagrams(output_sums, knotoids_connected_sums, comment=f"{datetime.now().isoformat()}")
    print("Saving disjoint sums...")
    kp.save_diagrams(output_disjoint, knotoids_disjoint_sums, comment=f"{datetime.now().isoformat()}")
    print("Saving multiple components...")
    kp.save_diagrams(output_multiple, knotoids_multiple_components, comment=f"{datetime.now().isoformat()}")
    print("Saving bridges...")
    kp.save_diagrams(output_bridges, knotoids_bridges, comment=f"{datetime.now().isoformat()}")

    print_stats(stats)

    # kp.export_pdf(knotoids_sets[-1], "plot/2-simplified.pdf", title=True)
    # kp.export_pdf(knotoids_connected_sums, "plot/2-connected-sums.pdf", title=True)
    # kp.export_pdf(knotoids_multiple_components, "plot/2-multiple-components.pdf", title=True)
    # kp.export_pdf(knotoids_disjoint_sums, "plot/2-disjoint-sums.pdf", title=True)
    # kp.export_pdf(knotoids_bridges, "plot/2-bridges.pdf", title=True)


"""

knotoids (all) : 6535
connected sum : 1081
bridges : 413
level 0 : 1921
level 1 : 1576
level 2 : 1506
level 3 : 1472

NEW WITH FLIPS


knotoids (all) : 160785
connected sum : 11612
bridges : 1163
level 0 : 5863
level 1 : 4049
level 2 : 3115
level 3 : 2600


"""