#!/usr/bin/env python3
import csv
from pathlib import Path

RESULTS_DIR = Path("results")
ALLOWED_CROSSINGS = [0, 1, 2, 3, 4, 5, 6, 7]
FILES = [RESULTS_DIR / f"knotoids-{k}.csv" for k in ALLOWED_CROSSINGS]


def read_all_files():
    data = {}
    for k, file in zip(ALLOWED_CROSSINGS, FILES):
        rows = []
        if not file.exists():
            data[k] = rows
            continue
        with file.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        data[k] = rows
    return data


def per_crossing_stats(data):
    """
    Relevant fields in the new CSV header:
      - kiral: "True" (kiral) or "False" (akiral)
      - rotatable: "True", "False", "unlikely", "unknown"
    """
    results = {}

    for k, rows in data.items():
        total = len(rows)

        kiral_yes = kiral_no = kiral_other = 0
        rot_yes = rot_no = rot_unlikely = rot_unknown = rot_other = 0

        for row in rows:
            kv = (row.get("kiral") or "").strip()
            if kv == "True":
                kiral_yes += 1
            elif kv == "False":
                kiral_no += 1
            else:
                kiral_other += 1

            rv = (row.get("rotatable") or "").strip().lower()
            if rv == "true":
                rot_yes += 1
            elif rv == "false":
                rot_no += 1
            elif rv == "unlikely":
                rot_unlikely += 1
            elif rv == "unknown":
                rot_unknown += 1
            else:
                rot_other += 1

        results[k] = {
            "total": total,
            "kiral_yes": kiral_yes,
            "kiral_no": kiral_no,
            "kiral_other": kiral_other,
            "rot_yes": rot_yes,
            "rot_no": rot_no,
            "rot_unlikely": rot_unlikely,
            "rot_unknown": rot_unknown,
            "rot_other": rot_other,
        }

    return results


def write_latex_table(stats, out_path=Path("table.txt")):
    # Totals across all crossings
    tot_total = 0
    tot_kiral_yes = tot_kiral_no = 0
    tot_rot_yes = tot_rot_no = tot_rot_unlikely = tot_rot_unknown = 0

    lines = []
    lines.append(r"\begin{tabular}{@{}lccccccc@{}}")
    lines.append(r"\toprule")
    lines.append(
        r"\textbf{Crossings} & \textbf{Total} & "
        r"\multicolumn{2}{c}{\textbf{Chiral}} & "
        r"\multicolumn{4}{c}{\textbf{Rotatable}} \\"
    )
    lines.append(r"\cmidrule(lr){3-4}\cmidrule(lr){5-8}")
    lines.append(
        r"& & \textbf{Yes} & \textbf{No} & "
        r"\textbf{Yes} & \textbf{No} & \textbf{Unlikely} & \textbf{Unknown} \\"
    )
    lines.append(r"\midrule")

    for k in ALLOWED_CROSSINGS:
        s = stats.get(k, {})
        total = int(s.get("total", 0))
        kiral_yes = int(s.get("kiral_yes", 0))
        kiral_no = int(s.get("kiral_no", 0))
        rot_yes = int(s.get("rot_yes", 0))
        rot_no = int(s.get("rot_no", 0))
        rot_unlikely = int(s.get("rot_unlikely", 0))
        rot_unknown = int(s.get("rot_unknown", 0))

        tot_total += total
        tot_kiral_yes += kiral_yes
        tot_kiral_no += kiral_no
        tot_rot_yes += rot_yes
        tot_rot_no += rot_no
        tot_rot_unlikely += rot_unlikely
        tot_rot_unknown += rot_unknown

        lines.append(
            f"{k} & {total} & {kiral_yes} & {kiral_no} & "
            f"{rot_yes} & {rot_no} & {rot_unlikely} & {rot_unknown} \\\\"
        )

    lines.append(r"\midrule")
    lines.append(
        r"\textbf{Total} & " + rf"\textbf{{{tot_total}}} & "
        + rf"\textbf{{{tot_kiral_yes}}} & \textbf{{{tot_kiral_no}}} & "
        + rf"\textbf{{{tot_rot_yes}}} & \textbf{{{tot_rot_no}}} & "
        + rf"\textbf{{{tot_rot_unlikely}}} & \textbf{{{tot_rot_unknown}}} \\"
    )
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append("")  # trailing newline

    out_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    data = read_all_files()
    stats = per_crossing_stats(data)

    print("=== Per-crossing statistics ===")
    for k in ALLOWED_CROSSINGS:
        s = stats.get(k, {})
        print(f"Crossings {k}: total={s.get('total', 0)}")
        print(f"  Chiral (kiral): Yes={s.get('kiral_yes', 0)}, No={s.get('kiral_no', 0)}, Other={s.get('kiral_other', 0)}")
        print(
            "  Rotatable: "
            f"Yes={s.get('rot_yes', 0)}, "
            f"No={s.get('rot_no', 0)}, "
            f"Unlikely={s.get('rot_unlikely', 0)}, "
            f"Unknown={s.get('rot_unknown', 0)}, "
            f"Other={s.get('rot_other', 0)}"
        )

    write_latex_table(stats, out_path=Path("table.txt"))
    print("\nWrote LaTeX table to table.txt")


    # FIGURE OUT POLY STRENGTH
    import knotpy as kp
    knotoids = kp.load_invariant_table(Path("data") / "11-knotoids-table.csv")


    print("Poly uniqueness")

    for f in ["kbsm", "affine", "arrow", "mock", "yamada"]:
        unique = 0
        non_unique = 0

        vals = [v[f] for v in knotoids.values()]
        for i in vals:
            c = vals.count(i)
            if c == 1:
                unique += 1
            elif c > 1:
                non_unique += 1
            else:
                raise ValueError("!!!")


        print(f"{f} unique: {unique} non-unique: {non_unique}")


    print("")


    def kbsm2(k):
        kp.settings.allowed_moves = "r1,r2,r3"
        return kp.kauffman_bracket_skein_module(k, normalize=True)[0][0]


    def yamada2(k):
        kp.settings.allowed_moves = "r1,r2,r3"
        ck = kp.closure(k, True, True)
        kp.settings.allowed_moves = "r1,r2,r3,r4,r5"
        y = kp.yamada(ck)
        kp.settings.allowed_moves = "r1,r2,r3"
        return y


    def arrow2(k):
        kp.settings.allowed_moves = "r1,r2,r3"
        return kp.arrow_polynomial(k)


    def mock2(k):
        kp.settings.allowed_moves = "r1,r2,r3"
        return kp.mock_alexander_polynomial(k)


    def affine2(k):
        kp.settings.allowed_moves = "r1,r2,r3"
        return kp.affine_index_polynomial(k)



    print("Poly uniqueness with mirror")



    for f in ["kbsm", "affine", "arrow", "mock", "yamada"]:
        unique = 0
        non_unique = 0


        vals = [v["diagram"] for v in knotoids.values()]

        if f == "kbsm":
            inv = [{kbsm2(_), kbsm2(kp.mirror(_, inplace=False))} for _ in vals]
        elif f == "affine":
            inv = [{affine2(_), affine2(kp.mirror(_, inplace=False))} for _ in vals]
        elif f == "arrow":
            inv = [{arrow2(_), arrow2(kp.mirror(_, inplace=False))} for _ in vals]
        elif f == "mock":
            inv = [{mock2(_), mock2(kp.mirror(_, inplace=False))} for _ in vals]
        elif f == "yamada":
            inv = [{knotoids[_.name]["yamada"], kp.yamada_mirror(knotoids[_.name]["yamada"], normalize=True)} for _ in vals]
        else:
            raise ValueError("!!!")

        for i in inv:
            c = inv.count(i)
            if c == 1:
                unique += 1
            elif c > 1:
                non_unique += 1
            else:
                raise ValueError("!!!")



        print(f"{f} unique: {unique} non-unique: {non_unique}")


    print("Rotatable:")
    print(" ".join([k for k in knotoids if knotoids[k]["rotatable"] == "True"]))


    print("Achiral:")
    print(" ".join([k for k in knotoids if knotoids[k]["kiral"] == "False"]))

    print("Fully Achiral:")
    print(" ".join([k for k in knotoids if knotoids[k]["kiral"] == "False" and knotoids[k]["rotatable"] == "True"]))
