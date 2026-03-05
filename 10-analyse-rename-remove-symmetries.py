import knotpy as kp
from pathlib import Path
from collections import defaultdict
kp.settings.allowed_moves = "r1,r2,r3"


"""
name,native notation,kbsm,affine,arrow,mock,yamada,flip,mirror,unique,mutant

name,    flip,   mirror,   unique,  mutant
7_57,    7_57,   7_1113,   True,     False
"""
knotoid_invariants = kp.load_invariant_table(Path("data") / "9-knotoids-invariants-with-symmetry.csv")

table = dict()
processed = set()
dsu = kp.utils.DisjointSetUnion()

quadruples = set()
for k, v in knotoid_invariants.items():

    unique = v["unique"].strip() == "True"
    mutant = v["mutant"].strip() != "False"
    mutant_name = v["mutant"].strip()
    mirror = v["mirror"].strip()
    flip = v["flip"].strip()


    dsu.add(k)

    if unique:
        # unique
        assert " " not in mirror, f"Mirror contains spaces: {mirror}"
        assert " " not in flip, f"Mirror contains spaces: {mirror}"
        v["kiral"] = (mirror != k)
        v["rotatable"] = (flip == k)

        # join knototid and its mirror
        if mirror != k:
            dsu[k] = mirror

        if flip != k:
            dsu[mirror] = flip

        #print("Kiral", v["kiral"], "Rotatable", v["rotatable"], end=" ")
        #print()

    else:
        # non-unique
        print(k, "U",unique, "M",mutant, "MN",mutant_name, "Mirror", mirror, "Flip", flip)


        if not mutant:
            assert mutant_name == "False"
            assert flip == k
            v["rotatable"] = "unlikely"
            v["kiral"] = (mirror != k)

            if mirror != k:
                dsu[k] = mirror

        else:
            assert mutant_name != "False"

            m1, m2 = mirror.split(" ")
            f1, f2 = flip.split(" ")

            assert k == f1 or k == f2
            v["kiral"] = ((m1 == k) or (m2 == k))
            v["rotatable"] = "unknown"
            if k not in quadruples:
                dsu[f1] = m1  # choice
                dsu[f2] = m2 # choice

            quadruples.add(m1)
            quadruples.add(m2)
            quadruples.add(f1)
            quadruples.add(f2)

def face_len_list(k):
    result = sorted([-len(_) for _ in k.faces])
    return result

table = dict()
representative_dict = dict()
for cls in dsu.classes():
    representative = min([knotoid_invariants[k]["diagram"] for k in cls])
    rep_name = representative.name
    representative_dict.update({k: rep_name for k in cls})
    table[rep_name] = knotoid_invariants[rep_name]

table_diagrams = [knotoid_invariants[_]["diagram"] for _ in table]
# sort by name and rename
table_c = [[k for k in table_diagrams if len(k) - 2 == c] for c in range(8)]

for i, t in enumerate(table_c):
    table_c[i] = sorted(t, key=lambda _: (kp.open_end_distance(_), face_len_list(_), _))



new_to_old, old_to_new, new_to_page, page_to_new = dict(), dict(), dict(), dict()

for i, t in enumerate(table_c):
    for j, k in enumerate(t, start=1):
        old, new = k.name, f"{i}_{j}"
        new_to_old[new] = old
        old_to_new[old] = new
        page_to_new[len(new_to_page) + 1] = new
        new_to_page[new] = len(new_to_page) + 1

def repl(o):
    print("r", o)
    if "_" not in o:
        return o
    if " " in o:
        return " ".join([old_to_new[_] if _ in old_to_new else "*" for _ in o.split(" ")])
    return old_to_new[o] if o in old_to_new else "*"

def get_class_repr(b):
    for k in new_to_old.keys():
        if dsu.connected(k, b):
            return k
    raise ValueError(f"No new equivalence classes found for {b}")

new_table = {old_to_new[k]: v for k, v in table.items()}
for k, v in new_table.items():
    v["diagram"].name = k
    # replace flip, mirror, mutant
    v["flip"] = repl(v["flip"])
    v["mirror"] = repl(v["mirror"])
    if v["mutant"] != "False":
        assert v["mutant"] in representative_dict
        v["mutant"] = repl(representative_dict[v["mutant"]])
    #v["mutant"] = repl(get_class_repr(v["mutant"])) if v["mutant"] != "False" else "False"


for k, v in new_table.items():
    v["page"] = new_to_page[k]
    v["em"] = kp.to_condensed_em_notation(v["diagram"])
    v["pd"] = kp.to_pd_notation(v["diagram"])

#for k, v in new_table.items():
#    print(k,"->", v)

kp.save_invariant_table(Path("data") / "10-knotoids-table.csv", new_table)

print("save pdf")
diagrams_sorted_list = []



assert sorted(new_to_page.values())  == sorted(page_to_new.keys())  == list(range(1, len(new_table) + 1))
for r in range(1, len(new_table) + 1):
    diagrams_sorted_list.append(new_table[page_to_new[r]]["diagram"])

for d in diagrams_sorted_list:
    assert kp.sanity_check(d)

#kp.export_pdf(diagrams_sorted_list, Path("data") / "knotoids.pdf", ignore_errors=True)
