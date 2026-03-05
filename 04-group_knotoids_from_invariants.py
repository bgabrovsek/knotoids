
from pathlib import Path
from common import *
from collections import Counter
from knotpy.tables.diagram_reader import load_diagrams
from knotpy.tables.invariant_reader import load_invariant_table
import knotpy as kp
from tqdm import tqdm

print("v6")
kp.settings.allowed_moves = "r1,r2,r3"

input_results = Path("data/3-knotoids-invariants-all.csv")  # save PD codes of knotoids
output_u1 =     Path("data/4-knotoids-unique-part-1.txt")  # save PD codes of knotoids
output_n1 =     Path("data/4-knotoids-groups-stage-1.txt")  # save PD codes of knotoids
output_u_new =  Path("data/4-knotoids-unique-part-2.txt")  # save PD codes of knotoids
output_n_new =  Path("data/4-knotoids-groups-stage-2.txt")  # save PD codes of knotoids

data = load_invariant_table(input_results)

invariants = ["kbsm", "affine", "arrow", "mock", "yamada"]

groups = defaultdict(list)
for entry in data.values():
    key = tuple(entry[k] for k in invariants)
    groups[key].append(entry["diagram"])



unique_diagrams = []
non_unique_diagrams = []
for diagrams in groups.values():
    if len(diagrams) == 1:
        unique_diagrams.append(diagrams[0])
    else:
        non_unique_diagrams.append(diagrams)

print("Unique diagrams:", len(unique_diagrams))
print("Non-unique diagrams:", len(non_unique_diagrams))
print("Distribution:")
print(Counter(len(g) for g in non_unique_diagrams))


kp.save_diagrams(output_u1, unique_diagrams)
kp.save_diagram_sets(output_n1, non_unique_diagrams)


print("Continuing to simplify non-unique groups...")
new_unique_diagrams = []
new_non_unique_diagrams = []
for group in tqdm(non_unique_diagrams):
    names = [g.name for g in group]
    # print(f"Group of length {len(group)} []")
    eq = kp.reduce_equivalent_diagrams(group, depth=1)
    #
    # if len(eq) < len(group):
    #     print(f"Reduced to {len(eq)}")
    # else:
    #     print(f"No reduction ({len(eq)})")

    candidates = list(eq.keys())
    for c, name in zip(candidates, names):  # name the candidates (could be mixed up, but the invariants should be the same)
        c.name = name

    if len(eq) == 1:
        new_unique_diagrams.append(candidates[0])
    else:
        new_non_unique_diagrams.append(candidates)



print("Unique diagrams:", len(new_unique_diagrams))
print("Non-unique diagrams:", len(new_non_unique_diagrams))
print("Distribution:")
print(Counter(len(g) for g in new_non_unique_diagrams))

kp.save_diagrams(output_u_new, new_unique_diagrams)
kp.save_diagram_sets(output_n_new, new_non_unique_diagrams)

"""
Unique diagrams: 429
Non-unique diagrams: 503
Distribution:
Counter({2: 476, 3: 20, 4: 5, 6: 1, 5: 1})
Continuing to simplify non-unique groups...
Unique diagrams: 6
Non-unique diagrams: 497
Distribution:
Counter({2: 485, 3: 10, 4: 2})

after flip:




"""