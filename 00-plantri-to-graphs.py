"""
Plantri parameters:
./plantri  -p -c1 -m1 -a 2 > g2.txt
./plantri  -p -c1 -m1 -a 3 > g3.txt
...
./plantri  -p -c1 -m1 -a 8 > g8.txt

"""
from collections import deque

import knotpy as kp
import os, glob

def clean_graph_files(path="data/plantri/"):
    for fname in glob.glob(os.path.join(path, "graphs*.txt")):
        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()
        valid = []
        for line in lines:
            try:
                _, substrs = line.strip().split(maxsplit=1)
            except ValueError:
                continue
            substrs = substrs.split(",")
            if sum(len(s) == 1 for s in substrs) == 2 and all(len(s) <= 4 for s in substrs):
                valid.append(line)
        newname = fname.replace(".txt", "_cleaned.txt")
        with open(newname, "w", encoding="utf-8") as f:
            f.writelines(valid)
        print(f"{fname} -> {newname}: {len(lines)} -> {len(valid)} kept")



def is_knotoid_graph(g):
    seq = kp.degree_sequence(g)
    return len(seq) >= 2 and seq[0] == seq[1] == 1 and all(_ == 4 for _ in seq[2:])

print("v3")

clean_graph_files()

# laod all plantri graphs
plantri_graphs = {n: kp.load_diagrams(f"data/plantri/graphs{n}_cleaned.txt", notation="plantri") for n in range(2, 10)}
print("Graphs:", [len(g) for g in plantri_graphs.values()], "(all)")

# remove graphs with vertices with degree more than 4
for n, graphs in plantri_graphs.items():
    plantri_graphs[n] = [g for g in plantri_graphs[n] if max(kp.degree_sequence(g)) <= 4]

print("Graphs:", [len(g) for g in plantri_graphs.values()], "(degree <= 4 vertices)")

# remove graphs that do not have two vertices of degree one
for n, graphs in plantri_graphs.items():
    plantri_graphs[n] = [g for g in plantri_graphs[n] if sum(d == 1 for d in kp.degree_sequence(g)) == 2]

print("Graphs:", [len(g) for g in plantri_graphs.values()], "(two degree = 1 vertices)")

knotoid_graphs = {}

# parallellize arcs
for n, graphs in plantri_graphs.items():
    print(f"Processing graphs with {n} vertices...")
    s = {kp.canonical(g) for g in graphs}
    result = set()
    while s:
        g = s.pop()

        if is_knotoid_graph(g):
            result.add(g)
            continue

        for arc in g.arcs:
            ep1, ep2 = arc
            if g.degree(ep1.node) not in [2, 3] or g.degree(ep2.node) not in [2, 3]:
                continue

            g_ = kp.parallelize_arc(g, arc, inplace=False)
            g_ = kp.canonical(g_)
            s.add(g_)
            #s.add(kp.canonical(kp.flip(g_)))

    knotoid_graphs[n] = result

print("Graphs:", [len(g) for g in knotoid_graphs.values()], "(knotoid-like graphs)")

# check old graphs
#all_old_graphs = kp.load_diagrams("data/graphs_pdcodes.txt", "pd")
#old_graphs = {}
#for n in range(2, 11):
#    old_graphs[n] = [g for g in all_old_graphs if len(g) == n]

#print("Graphs:", [len(g) for g in old_graphs.values()], "(old)")



for n, graphs in knotoid_graphs.items():
    print(f"Saving {n} graphs... length = ")
    kp.save_diagrams(f"data/graphs/graphs{n}-knotoids.txt", graphs)

all_graphs = [_ for graphs in knotoid_graphs.values() for _ in graphs]
kp.save_diagrams(f"data/graphs/graphs-all-knotoids.txt", all_graphs)


"""
RUN 16.2.2026
Graphs: [1, 1, 1, 5, 32, 232, 1732, 13965] (all)
Graphs: [1, 1, 1, 5, 32, 232, 1732, 13965] (degree <= 4 vertices)
Graphs: [1, 1, 1, 5, 32, 232, 1732, 13965] (two degree = 1 vertices)
Graphs: [1, 0, 1, 4, 19, 71, 374, 2009] (knotoid-like graphs)

"""

"""
# 3.12.25
data/plantri\graphs10.txt -> data/plantri\graphs10_cleaned.txt: 12046072 -> 119796 kept
data/plantri\graphs10_cleaned.txt -> data/plantri\graphs10_cleaned_cleaned.txt: 119796 -> 119796 kept
data/plantri\graphs10_cleaned_cleaned.txt -> data/plantri\graphs10_cleaned_cleaned_cleaned.txt: 119796 -> 119796 kept
data/plantri\graphs10_cleaned_cleaned_cleaned.txt -> data/plantri\graphs10_cleaned_cleaned_cleaned_cleaned.txt: 119796 -> 119796 kept
data/plantri\graphs10_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs10_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 119796 -> 119796 kept
data/plantri\graphs10_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs10_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 119796 -> 119796 kept
data/plantri\graphs10_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs10_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 119796 -> 119796 kept
data/plantri\graphs2.txt -> data/plantri\graphs2_cleaned.txt: 1 -> 1 kept
data/plantri\graphs2_cleaned.txt -> data/plantri\graphs2_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs2_cleaned_cleaned.txt -> data/plantri\graphs2_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs2_cleaned_cleaned_cleaned.txt -> data/plantri\graphs2_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs2_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs2_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs2_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs2_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs2_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs2_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs3.txt -> data/plantri\graphs3_cleaned.txt: 2 -> 1 kept
data/plantri\graphs3_cleaned.txt -> data/plantri\graphs3_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs3_cleaned_cleaned.txt -> data/plantri\graphs3_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs3_cleaned_cleaned_cleaned.txt -> data/plantri\graphs3_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs3_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs3_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs3_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs3_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs3_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs3_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs4.txt -> data/plantri\graphs4_cleaned.txt: 6 -> 1 kept
data/plantri\graphs4_cleaned.txt -> data/plantri\graphs4_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs4_cleaned_cleaned.txt -> data/plantri\graphs4_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs4_cleaned_cleaned_cleaned.txt -> data/plantri\graphs4_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs4_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs4_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs4_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs4_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs4_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs4_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1 -> 1 kept
data/plantri\graphs5.txt -> data/plantri\graphs5_cleaned.txt: 25 -> 5 kept
data/plantri\graphs5_cleaned.txt -> data/plantri\graphs5_cleaned_cleaned.txt: 5 -> 5 kept
data/plantri\graphs5_cleaned_cleaned.txt -> data/plantri\graphs5_cleaned_cleaned_cleaned.txt: 5 -> 5 kept
data/plantri\graphs5_cleaned_cleaned_cleaned.txt -> data/plantri\graphs5_cleaned_cleaned_cleaned_cleaned.txt: 5 -> 5 kept
data/plantri\graphs5_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs5_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 5 -> 5 kept
data/plantri\graphs5_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs5_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 5 -> 5 kept
data/plantri\graphs5_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs5_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 5 -> 5 kept
data/plantri\graphs6.txt -> data/plantri\graphs6_cleaned.txt: 179 -> 32 kept
data/plantri\graphs6_cleaned.txt -> data/plantri\graphs6_cleaned_cleaned.txt: 32 -> 32 kept
data/plantri\graphs6_cleaned_cleaned.txt -> data/plantri\graphs6_cleaned_cleaned_cleaned.txt: 32 -> 32 kept
data/plantri\graphs6_cleaned_cleaned_cleaned.txt -> data/plantri\graphs6_cleaned_cleaned_cleaned_cleaned.txt: 32 -> 32 kept
data/plantri\graphs6_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs6_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 32 -> 32 kept
data/plantri\graphs6_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs6_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 32 -> 32 kept
data/plantri\graphs6_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs6_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 32 -> 32 kept
data/plantri\graphs7.txt -> data/plantri\graphs7_cleaned.txt: 2014 -> 232 kept
data/plantri\graphs7_cleaned.txt -> data/plantri\graphs7_cleaned_cleaned.txt: 232 -> 232 kept
data/plantri\graphs7_cleaned_cleaned.txt -> data/plantri\graphs7_cleaned_cleaned_cleaned.txt: 232 -> 232 kept
data/plantri\graphs7_cleaned_cleaned_cleaned.txt -> data/plantri\graphs7_cleaned_cleaned_cleaned_cleaned.txt: 232 -> 232 kept
data/plantri\graphs7_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs7_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 232 -> 232 kept
data/plantri\graphs7_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs7_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 232 -> 232 kept
data/plantri\graphs7_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs7_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 232 -> 232 kept
data/plantri\graphs8.txt -> data/plantri\graphs8_cleaned.txt: 31178 -> 1732 kept
data/plantri\graphs8_cleaned.txt -> data/plantri\graphs8_cleaned_cleaned.txt: 1732 -> 1732 kept
data/plantri\graphs8_cleaned_cleaned.txt -> data/plantri\graphs8_cleaned_cleaned_cleaned.txt: 1732 -> 1732 kept
data/plantri\graphs8_cleaned_cleaned_cleaned.txt -> data/plantri\graphs8_cleaned_cleaned_cleaned_cleaned.txt: 1732 -> 1732 kept
data/plantri\graphs8_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs8_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1732 -> 1732 kept
data/plantri\graphs8_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs8_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1732 -> 1732 kept
data/plantri\graphs8_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs8_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 1732 -> 1732 kept
data/plantri\graphs9.txt -> data/plantri\graphs9_cleaned.txt: 580555 -> 13965 kept
data/plantri\graphs9_cleaned.txt -> data/plantri\graphs9_cleaned_cleaned.txt: 13965 -> 13965 kept
data/plantri\graphs9_cleaned_cleaned.txt -> data/plantri\graphs9_cleaned_cleaned_cleaned.txt: 13965 -> 13965 kept
data/plantri\graphs9_cleaned_cleaned_cleaned.txt -> data/plantri\graphs9_cleaned_cleaned_cleaned_cleaned.txt: 13965 -> 13965 kept
data/plantri\graphs9_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs9_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 13965 -> 13965 kept
data/plantri\graphs9_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs9_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 13965 -> 13965 kept
data/plantri\graphs9_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt -> data/plantri\graphs9_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned_cleaned.txt: 13965 -> 13965 kept
Graphs: [1, 1, 1, 5, 32, 232, 1732, 13965, 119796] (all)
Graphs: [1, 1, 1, 5, 32, 232, 1732, 13965, 119796] (degree <= 4 vertices)
Graphs: [1, 1, 1, 5, 32, 232, 1732, 13965, 119796] (two degree = 1 vertices)
Processing graphs with 2 vertices...
Processing graphs with 3 vertices...
Processing graphs with 4 vertices...
Processing graphs with 5 vertices...
Processing graphs with 6 vertices...
Processing graphs with 7 vertices...
Processing graphs with 8 vertices...
Processing graphs with 9 vertices...
Processing graphs with 10 vertices...
Graphs: [1, 0, 1, 4, 19, 71, 374, 2009, 11949] (knotoid-like graphs)
Saving 2 graphs... length = 
Saving 3 graphs... length = 
Saving 4 graphs... length = 
Saving 5 graphs... length = 
Saving 6 graphs... length = 
Saving 7 graphs... length = 
Saving 8 graphs... length = 
Saving 9 graphs... length = 
Saving 10 graphs... length = 



"""