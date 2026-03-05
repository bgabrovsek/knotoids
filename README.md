# Knotoids

This repository contains the code used for the computations in the paper

**A table of knotoids in $S^3$ up to seven crossings**  
Boštjan Gabrovšek, Paolo Cavicchioli

## Final results

The complete table of knotoids produced by the computations in this repository is available here:

➡ **https://github.com/bgabrovsek/knotoids/blob/main/knotoids.pdf**

The PDF contains the final classification of knotoids in \(S^3\) up to seven crossings together with their invariants.

## Overview

The code in this repository performs the following steps:

1. Generation of planar graphs using **plantri**
2. Construction of knotoid diagrams from the graphs
3. Reduction using sequences of **Reidemeister moves**
4. Detection of equivalent knotoids
5. Computation of invariants, including:
   - Kauffman bracket polynomial
   - Mock Alexander polynomial
   - Arrow polynomial
   - Affine index polynomial
   - Yamada polynomial of the double closure

The output of these computations produces the tables reported in the paper and in the PDF above.
