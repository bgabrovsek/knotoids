"""
Draws unresolved knotoids

"""
from pathlib import Path
from common import *
from collections import Counter
from knotpy.tables.diagram_reader import load_diagrams
from knotpy.tables.invariant_reader import load_invariant_table
import knotpy as kp
from tqdm import tqdm

kp.settings.allowed_moves = "r1,r2,r3,flype,flip"

input = Path("data/7-knotoids-groups-up-to-flip.txt")  # save PD codes of knotoids
data = kp.load_diagram_sets(input)


kp.export_pdf_groups(data, Path("plots") / "7-knotoids-groups.pdf", ignore_errors=True, arc_width=2.0)


