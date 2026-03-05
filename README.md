# Knotoids

This repository contains the code used for the computations in the paper

> **A table of knotoids in $S^3$ up to seven crossings**  
> Boštjan Gabrovšek, Paolo Cavicchioli

The code was used to generate, classify, and analyse knotoid diagrams with up to seven crossings.

## Overview

The project performs the following steps:

1. **Generation of planar graphs** using `plantri`.
2. **Construction of knotoid diagrams** from the generated graphs.
3. **Normalization and reduction** using sequences of Reidemeister moves.
4. **Detection of equivalence classes** of knotoids.
5. **Computation of invariants** including:
   - Kauffman bracket polynomial
   - Mock Alexander polynomial
   - Arrow polynomial
   - Affine index polynomial

The final output is the table of knotoids presented in the paper.

## Dependencies

The code relies on the following tools:

- Python ≥ 3.10
- [KnotPy](https://github.com/bgabrovsek/knotpy)
- [plantri](https://users.cecs.anu.edu.au/~bdm/plantri/)

Additional Python packages may be required depending on the scripts.

## Installation

Clone the repository:

```bash
git clone https://github.com/bgabrovsek/knotoids.git
cd knotoids
