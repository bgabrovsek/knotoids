
from pathlib import Path
from common import *
import glob

from knotpy.tables.diagram_reader import load_diagrams
from knotpy.tables.parallel_writer import save_invariants_parallel
import knotpy as kp

PARALLEL = True

kp.settings.allowed_moves = "r1,r2,r3"
print("v4")

DATA_DIR = Path("data")
BASENAME = "3-knotoids-invariants-part"

def kbsm_2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.kauffman_bracket_skein_module(k, normalize=True)[0][0]

def yamada_closure_2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.yamada(kp.closure(k, True, True))

def arrow_2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.arrow_polynomial(k)
    return arrow_2(k)

def mock_2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.mock_alexander_polynomial(k)

def affine_2(k):
    kp.settings.allowed_moves = "r1,r2,r3"
    return kp.affine_index_polynomial(k)


def read_already_computed_parts():
    data = {}
    n = 0
    while True:
        n += 1
        path = DATA_DIR / f"{BASENAME}-{n}.csv"
        if not path.exists():
            break
        print("Reading", path)
        data.update(kp.load_invariant_table(path))
    return data, n


if __name__ == "__main__":

    kp.settings.allowed_moves = "r1,r2,r3"
    input_diagrams = DATA_DIR / Path("2-knotoids-simplified.txt")  # save PD codes of knotoids
    output_all_results = DATA_DIR / Path("3-knotoids-invariants-all.csv")  # save PD codes of knotoids

    # read already pre-computed invariants (in case the process halted)
    #output_new_partial_results = DATA_DIR / f"{BASENAME}-{n}.csv"
    #existing_data, n = read_already_computed_parts()

    # keys_to_remove = []
    # for k, v in existing_data.items():
    #     if all(not v[inv] for inv in ["kbsm", "affine", "arrow", "mock", "yamada"]):
    #         keys_to_remove.append(k)
    #
    # for k in keys_to_remove:
    #     del existing_data[k]

    input_knotoids = kp.load_diagrams(input_diagrams)

    # print("Input knotoids:", len(input_knotoids))
    # print("Already computed:", len(existing_data))

    count_crossings = defaultdict(int)
    for k in input_knotoids:
        count_crossings[len(k) - 2] += 1
        k.name = f"{len(k)-2}_{count_crossings[len(k) - 2]}"

        # if k.name in existing_data and k != existing_data[k.name]["diagram"]:
        #     print("Previously computed table does not match current table")

    knotoids = input_knotoids#[k for k in input_knotoids if k.name not in existing_data]
    print("Loaded", len(knotoids), "knotoids")

    # remove data we do not need
    input_knotoids = None
    existing_data = None

    invariants = {
        "kbsm": kbsm_2,
        "affine": affine_2,
        "arrow": arrow_2,
        "mock": mock_2,
        "yamada": yamada_closure_2,
    }

    if PARALLEL:
        errors = save_invariants_parallel(output_all_results, knotoids, invariants, workers=28, scratch_dir=DATA_DIR / "scratch")

        if any(errors.values()):
            print("Some invariants failed:")
            for diag, errs in errors.items():
                for err in errs:
                    print(f"{diag}: {err}")

    else:
        results = {}
        for i, k in enumerate(knotoids):

            results[k.name] = {
                "name": k.name,
                "knotpy notation": kp.to_knotpy_notation(k),
                "kbsm": kbsm_2(k),
                "affine": affine_2(k),
                "arrow": arrow_2(k),
                "mock": mock_2(k),
                "yamada": yamada_closure_2(k),
            }
            print(f"{i}/{len(knotoids)}", k.name, results[k.name]["yamada"])
        kp.save_invariant_table(output_all_results, results)


    # check results

    input_knotoids = kp.load_diagrams(input_diagrams)
    outputed_knotoids = kp.load_invariant_table(output_all_results)

    if len(input_knotoids) == len(outputed_knotoids):
        print("All results computed successfully!")
        print("Saved as", output_all_results)
    else:
        print("Still missing some results.")
        print("Missing:", len(input_knotoids) - len(outputed_knotoids), "knotoids")

