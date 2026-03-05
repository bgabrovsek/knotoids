from pathlib import Path
import knotpy as kp
from tqdm import tqdm

"""
All available files:

1-all-knotoids-details.txt
1-all-knotoids.txt
2-knotoids-bridges.txt
2-knotoids-connected-sums.txt
2-knotoids-simplified.txt
3-knotoids-invariants-all.csv
4-knotoids-groups-stage-1.txt
4-knotoids-groups-stage-2.txt
5-knotoids-groups.txt
6-knotoids-groups-up-to-flip.txt
7-knotoids-groups-up-to-flip.txt


4-knotoids-unique-part-1.txt
4-knotoids-unique-part-2.txt
5-knotoids-unique.txt
6-knotoids-unique-up-to-flip.txt
7-knotoids-unique-up-to-flip.txt

"""


def match_invariants(invariants, values):
    matches = []
    for key, inv in invariants.items():
        #print(key, inv)
        # all pairs in values must be present and equal in inv
        if all(inv.get(k) == v for k, v in values.items()):
            matches.append(key)
    return matches

def kbsm2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.kauffman_bracket_skein_module(k, normalize=True)[0][0]

kp.settings.allowed_moves = "r1,r2,r3"

print("Loading knotoids")
unique_knotoids_files = ["4-knotoids-unique-part-1.txt", "4-knotoids-unique-part-2.txt", "5-knotoids-unique.txt"]
up_to_flip_knotoids_files = ["6-knotoids-unique-up-to-flip.txt", "7-knotoids-unique-up-to-flip.txt"]
up_to_flip_groups_file = ["7-knotoids-groups-up-to-flip.txt"]
data_path = Path("data")


# store all unique knotoids
unique_knotoids = [kp.load_diagrams(data_path / f) for f in unique_knotoids_files]
unique_knotoids = [_ for __ in unique_knotoids for _ in __]

# store all unique knotoids, where we removed flips, since they could not be distinguished
up_to_flip_knotoids = [kp.load_diagrams(data_path / f) for f in up_to_flip_knotoids_files]
up_to_flip_knotoids = [_ for __ in up_to_flip_knotoids for _ in __]

# store all knots that could not be distinguished
up_to_flip_knotoids_groups = [kp.load_diagram_sets(data_path / f) for f in up_to_flip_groups_file]
up_to_flip_knotoids_groups = [_ for __ in up_to_flip_knotoids_groups for _ in __]  # flatten groups
up_to_flip_knotoids_mutants = [_ for __ in up_to_flip_knotoids_groups for _ in __]

print("Unique knotoids:", len(unique_knotoids))
print("Up to flip knotoids:", len(up_to_flip_knotoids))
print("Up to flip knotoids groups:", len(up_to_flip_knotoids_groups), "containing", len(up_to_flip_knotoids_mutants))
print("Total knotoids:", len(unique_knotoids) + len(up_to_flip_knotoids) + len(up_to_flip_knotoids_mutants))

print()
print("Loading invariants")

invariants = kp.load_invariant_table(data_path / "3-knotoids-invariants-all.csv")


new_inv_dict = {}
all_processed_names = set()

print("Matching invariants for unique knotoids")

for k in tqdm(unique_knotoids):
    m = match_invariants(invariants, {"diagram": k})

    assert len(m) == 1, "Match not found"  # must find a single match
    m = m[0]
    assert m not in all_processed_names, "Duplicate name"
    all_processed_names.add(m)

    k.name = m
    invariants[m]["flip"] = None
    invariants[m]["mirror"] = None
    invariants[m]["unique"] = True
    invariants[m]["mutant"] = False
    new_inv_dict[m] = invariants[m]


print("Matching invariants for non-unique knotoids")

for k in tqdm(up_to_flip_knotoids):
    m = match_invariants(invariants, {"diagram": k})

    assert len(m) == 1, "Match not found"  # must find a single match
    m = m[0]
    assert m not in all_processed_names, "Duplicate name"
    all_processed_names.add(m)

    k.name = m
    invariants[m]["flip"] = None
    invariants[m]["mirror"] = None
    invariants[m]["unique"] = False
    invariants[m]["mutant"] = False
    new_inv_dict[m] = invariants[m]

print("Matching invariants for non-unique mutant knotoids")

for counter, (a, b) in tqdm(enumerate(up_to_flip_knotoids_groups)):

    ma = match_invariants(invariants, {"diagram": a})
    mb = match_invariants(invariants, {"diagram": b})

    assert len(ma) == 1, "Match not found"  # must find a single match
    ma = ma[0]
    assert ma not in all_processed_names, "Duplicate name"
    all_processed_names.add(ma)

    assert len(mb) == 1, "Match not found"  # must find a single match
    mb = mb[0]
    assert mb not in all_processed_names, "Duplicate name"
    all_processed_names.add(mb)

    a.name = ma
    b.name = mb

    invariants[ma]["flip"] = None
    invariants[ma]["mirror"] = None
    invariants[ma]["unique"] = False
    invariants[ma]["mutant"] = mb
    new_inv_dict[ma] = invariants[ma]

    invariants[mb]["flip"] = None
    invariants[mb]["mirror"] = None
    invariants[mb]["unique"] = False
    invariants[mb]["mutant"] = ma
    new_inv_dict[mb] = invariants[mb]



knotoids = unique_knotoids + up_to_flip_knotoids + [_ for __ in up_to_flip_knotoids_groups for _ in __]
kp.save_diagrams(data_path / "8-knotoids-up-to_symmetry.txt", knotoids)
kp.save_invariant_table(data_path / "8-knotoids-invariants.csv", new_inv_dict)