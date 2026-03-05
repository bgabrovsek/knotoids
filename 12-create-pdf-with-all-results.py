#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from pathlib import Path
import re

RESULTS_DIR = Path("results")
DIAGRAMS_DIR = Path("diagrams")
OUTPUT_TEX = Path("full-table.tex")
FIGURES_PDF = Path("knotoids.pdf")  # in repo root



def tex_escape(s):
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in s)

# Convert Python-style exponentiation to LaTeX: **k  ->  ^{k}
# Handles: **(expr), **{expr}, **-3, **10, **\alpha, **n
_POW_PAREN = re.compile(r"\*\*\s*\(([^()]*)\)")
_POW_BRACE = re.compile(r"\*\*\s*\{([^{}]*)\}")
_POW_SIMPLE = re.compile(r"\*\*\s*([+-]?(?:\d+(?:\.\d*)?)|\\[A-Za-z]+|\w+)")

def _normalize_powers(s: str) -> str:
    while True:
        s2 = _POW_PAREN.sub(r"^{\1}", s)
        s2 = _POW_BRACE.sub(r"^{\1}", s2)
        s3 = _POW_SIMPLE.sub(r"^{\1}", s2)
        if s3 == s:
            return s3
        s = s3

def as_math(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return ""
    s = _normalize_powers(s)
    # If already in math mode, leave delimiters as-is
    if (s.startswith("$") and s.endswith("$")) or s.startswith(r"\(") or s.endswith(r"\)") or s.startswith(r"\["):
        return s.replace("*", "")
    return f"${s}$".replace("*", "")

def read_csv_rows(csv_path: Path):
    rows = []
    if not csv_path.exists():
        return rows
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def _norm_bool_label(val: str, true_label: str, false_label: str, unknown_label: str) -> str:
    s = (val or "").strip().lower()
    if s in ("true", "1", "yes", "y", "t"):
        return true_label
    if s in ("false", "0", "no", "n", "f"):
        return false_label
    if not s or s == "unknown":
        return unknown_label
    return unknown_label

def _norm_rotatable(val: str) -> str:
    s = (val or "").strip().lower()
    if s in ("true", "1", "yes", "y", "t"):
        return "rotatable"
    if s in ("unlikely", "unknown"):
        return r"non-rotatable$^{*}$"
    if not s:
        return "rotatability unknown"
    return "rotatability unknown"

def invariants_block(row):

    name = tex_escape(str(row.get("name", "")).strip())

    import knotpy as kp

    em = tex_escape(str(row.get("em", "")).strip())
    em = em.upper()
    pd = tex_escape(str(row.get("pd", "")).strip())



    # NEW CSV columns:
    # chirality is in "kiral" as "True"/"False"
    chirality = _norm_bool_label(
        row.get("kiral", ""),
        true_label="chiral",
        false_label="achiral",
        unknown_label="chirality unknown",
    )

    # rotatability is in "rotatable" as "True"/"unlikely"/"unknown"
    rotatability = _norm_rotatable(row.get("rotatable", ""))

    # duplicate is in "mutant" as "False" or a name
    mutant_val = (row.get("mutant", "") or "").strip()
    mutant_low = mutant_val.lower()
    duplicate_line = ""
    if mutant_val and mutant_low not in ("false", "0", "no", "n", "f"):
        duplicate_line = f"Possible duplicate [{tex_escape(mutant_val)}]"

    #duplicate_val = (row.get("duplicate", "") or "").strip()
    #duplicate_line = f"Possible duplicate [{tex_escape(duplicate_val)}]" if duplicate_val else ""

    kbsm = as_math(str(row.get("kbsm", "")).strip())
    yamada = as_math(str(row.get("yamada", "")).strip())
    arrow = as_math(str(row.get("arrow", "")).strip())
    mock = as_math(str(row.get("mock", "")).strip())
    affine = as_math(str(row.get("affine", "")).strip())



    pd = pd.replace("X", "").replace("V", "")

    # Keep your name formatting behavior
    name = name.replace("\\_", "_{") + "}"
    name = "K" + name
    header_bits = [chirality, rotatability]
    if duplicate_line:
        header_bits.append(duplicate_line)

    lines = [
        rf"\textbf{{Name:}} \large{{$\mathbf{{{name}}}$}} ({', '.join(header_bits)})",
        rf"\textbf{{PD:}} {{\scriptsize\texttt{{{pd}}}}}" if name.startswith("K7") or name.startswith("K6") else rf"\textbf{{EM:}} {{\small\texttt{{{pd}}}}}",
        rf"\textbf{{EM:}} {{\scriptsize\texttt{{{em}}}}}" if name.startswith("K7")  else rf"\textbf{{EM:}} {{\small\texttt{{{em}}}}}",
        rf"\textbf{{Kauffman bracket:}} {{\scriptsize {kbsm}}}" if kbsm else r"\textbf{kbsm:}",
        rf"\textbf{{Arrow:}} {{\scriptsize {arrow.replace('L', 'L_')}}}" if arrow else r"\textbf{arrow:}",
        rf"\textbf{{Mock:}} {{\scriptsize {mock}}}" if mock else r"\textbf{mock:}",
        rf"\textbf{{Affine:}} {{\scriptsize {affine}}}" if affine else r"\textbf{affine:}",
        rf"\textbf{{Yamada:}} {{\scriptsize {yamada}}}" if yamada else r"\textbf{yamada:}",
    ]
    return r" \\ ".join(lines)

def entry_minipages(row):
    def forward_slashes(p: str) -> str:
        return p.replace("\\", "/")

    # CSV column "page" is 1-based
    page_raw = (row.get("page", "") or "").strip()
    try:
        page = int(page_raw) if page_raw else 1
    except ValueError:
        page = 1  # fallback if malformed

    img_pdf = forward_slashes(str(FIGURES_PDF))

    left = rf"""\begin{{minipage}}[t]{{0.25\textwidth}}
\vspace{{0pt}}% top-align the minipage
\centering
\includegraphics[page={page},width=\linewidth]{{{img_pdf}}}
\end{{minipage}}"""

    right = rf"""\begin{{minipage}}[t]{{0.73\textwidth}}
\vspace{{0pt}}% top-align the minipage
\raggedright\small
{invariants_block(row)}
\end{{minipage}}"""

    return left + "\n\\hfill\n" + right

def build_section(k, rows):
    if not rows:
        return ""
    lines = [rf"\section{{Number of crossings: {k}}}", ""]
    for idx, row in enumerate(rows):
        lines.append(r"\noindent " + entry_minipages(row))
        if idx != len(rows) - 1:
            lines += [
                r"",
                r"\vspace{0.6\baselineskip}",
                r"\noindent\rule{\textwidth}{0.4pt}",
                r"\vspace{0.9\baselineskip}",
            ]
        else:
            lines.append(r"")
    return "\n".join(lines)

def main():
    preamble = r"""\documentclass[11pt,a4paper]{article}
\usepackage[a4paper, margin=1cm]{geometry}
\usepackage{graphicx}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\title{Classified Knotoids}
\date{}
\begin{document}
\maketitle
"""
    sections = []
    for k in range(8):
        csv_path = RESULTS_DIR / f"knotoids-{k}.csv"
        rows = read_csv_rows(csv_path)
        print(k,"rows", len(rows))
        if rows:
            sections.append(build_section(k, rows))

    ending = r"\end{document}" + "\n"
    OUTPUT_TEX.write_text(preamble + "\n\n".join(sections) + "\n" + ending, encoding="utf-8")
    print(f"Wrote LaTeX to {OUTPUT_TEX}")

if __name__ == "__main__":
    main()