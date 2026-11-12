---
tag: STBB8G
kind: problem
slug: structure-alignment
name: Protein structure alignment
aliases:
- Structural alignment
- Protein structure comparison
area: biology/structure-prediction
level: core
summary: Given two 3D protein structures, find a one-to-one matching of their residues, and often a superposition, that makes them most alike under a chosen score; NP-hard for some scores.
prereqs: [optimal-superposition, contact-map, needleman-wunsch]
see_also: [dali, combinatorial-extension, tm-score, gdt-ts, kabsch-algorithm, protein-threading, global-alignment, hungarian-algorithm]
sources:
  - paper: doi:10.1109/SFFCS.1999.814624
    title: Deborah Goldman, Sorin Istrail and Christos H. Papadimitriou, Algorithmic aspects of protein structure similarity, 40th Annual Symposium on Foundations of Computer Science (FOCS), 1999, 512-521
    locator: the contact map overlap problem, the proof that it is NP-hard, and the polynomial cases
  - paper: doi:10.1093/protein/7.9.1059
    title: Richard H. Lathrop, The protein threading problem with sequence amino acid interaction preferences is NP-complete, Protein Engineering 7(9), 1994, 1059-1068
    locator: the reduction that shows threading with pairwise interactions and variable gaps is NP-complete
  - paper: doi:10.1073/pnas.0404383101
    title: Rachel Kolodny and Nathan Linial, Approximate protein structural alignment in polynomial time, PNAS 101(33), 2004, 12201-12206
    locator: the polynomial-time approximation for alignment scores defined through a superposition, by search over a grid of rigid motions and dynamic programming
  - paper: doi:10.1145/369133.369199
    title: Giuseppe Lancia, Robert Carr, Brian Walenz and Sorin Istrail, 101 optimal PDB structure alignments, a branch-and-cut algorithm for the maximum contact map overlap problem, RECOMB 2001, 193-202
    locator: the integer programming formulation of contact map overlap and its exact solution on real proteins
  - paper: doi:10.1006/jmbi.1993.1489
    title: Liisa Holm and Chris Sander, Protein structure comparison by alignment of distance matrices, Journal of Molecular Biology 233(1), 1993, 123-138
    locator: alignment by intramolecular distances without a superposition (DALI)
  - paper: doi:10.1093/protein/11.9.739
    title: Ilya N. Shindyalov and Philip E. Bourne, Protein structure alignment by incremental combinatorial extension (CE) of the optimal path, Protein Engineering 11(9), 1998, 739-747
    locator: alignment by chaining aligned fragment pairs (CE)
  - paper: doi:10.1093/nar/gki524
    title: Yang Zhang and Jeffrey Skolnick, TM-align, a protein structure alignment algorithm based on the TM-score, Nucleic Acids Research 33(7), 2005, 2302-2309
    locator: the heuristic that alternates dynamic programming with superposition to maximize the TM-score
  - paper: doi:10.1093/bioinformatics/btg1086
    title: Yuzhen Ye and Adam Godzik, Flexible structure alignment by chaining aligned fragment pairs allowing twists, Bioinformatics 19(Suppl 2), 2003, ii246-ii255
    locator: flexible alignment with hinges between rigid fragment chains (FATCAT)
---

Protein structure alignment takes two protein structures, given as 3D coordinates, and asks which residues of one correspond to which residues of the other, so that the matched parts are as alike as possible. Unlike sequence alignment, it compares shapes, so it finds relations between proteins whose sequences have diverged beyond recognition. Unlike [optimal superposition](/optimal-superposition/), the correspondence is not given: it is the main output. There is no single objective. Each method fixes its own score, and for several natural scores the exact problem is [NP-hard](/np-hard/), so the methods in use, such as [DALI](/dali/), [CE](/combinatorial-extension/) and TM-align, are heuristics.

## In plain words

You have two folded protein chains, and you suspect that they have the same overall shape, even though their sequences look different. You want to pair up the links of the two chains so that paired links sit in the same place once the two shapes are laid on top of each other.

Two questions are tied together. If you knew the pairing, finding the best way to lay one shape on the other would be easy. If you knew how to lay one shape on the other, finding a good pairing would also be easy: walk along both chains and pair links that sit close together. But you know neither at the start. Each method breaks this circle in its own way: some compare the inner distances of each shape, which needs no laying over; others guess small matching pieces and grow them.

## Definition

**Model.** A structure is its $C_\alpha$ trace, $A = (a_1, \ldots, a_n)$ and $B = (b_1, \ldots, b_m)$ with $a_i, b_j \in \mathbb{R}^3$, in Å. Arithmetic is in the [real RAM](/real-ram/).

**Alignment.** An alignment is a set of pairs $M = \{(i_1, j_1), \ldots, (i_k, j_k)\}$ that is one-to-one. A sequential alignment also keeps the chain order: $i_1 < \cdots < i_k$ and $j_1 < \cdots < j_k$. This is the same kind of object as a [global alignment](/global-alignment/) of two sequences, with the unmatched residues as gaps.

**Problem.** Given $A$, $B$ and a score $S$, find a sequential alignment $M$ that maximizes $S(M)$. The usual scores fall into two families.

- **Scores with a superposition.** $S(M) = \max_{R, t} \sum_{(i, j) \in M} f(|R a_i + t - b_j|)$ for a function $f$ that falls with the distance, such as $f(d) = 1/(1 + (d/d_0)^2)$ for the [TM-score](/tm-score/), or $f(d) = [d \le c]$ for a count within a cutoff. A related form maximizes $|M|$ subject to the least [RMSD](/rmsd/) of $M$ being at most a bound.
- **Scores without a superposition.** $S(M) = \sum_{(i, j), (i', j') \in M} \phi(|a_i - a_{i'}|, |b_j - b_{j'}|)$ compares the intramolecular distances of matched pairs, as in [DALI](/dali/). The special case $\phi = 1$ when both pairs are in contact, and 0 otherwise, is the contact map overlap (CMO) problem: find the alignment that shares the most [contacts](/contact-map/).

The output is $M$, and for the first family also the superposition $(R, t)$.

## Variants

- **Non-sequential.** Drop the order condition. This finds circular permutations and swapped domains, at the cost of a larger search space.
- **Flexible.** Allow the alignment to use different rigid motions for different segments, joined at hinges. FATCAT (Ye and Godzik 2003) chains rigid fragment pairs and pays for each twist.
- **Multiple.** Align $K \ge 3$ structures at once, for a structural core common to a family.
- **Database search.** Compare one query structure with every structure in a database and rank the hits by a significance score, such as the Z-score of DALI or CE.
- **[Threading](/protein-threading/).** Align a sequence of unknown structure onto a known structure. Lathrop (1994) proved that threading with pairwise residue interactions and variable gaps is NP-complete.

## Examples

Let $A$ be four $C_\alpha$ atoms on a line, 3.8 Å apart: $(0,0,0), (3.8,0,0), (7.6,0,0), (11.4,0,0)$. Let $B$ be the same with one extra residue in a bulge: $(0,0,0), (3.8,0,0), (5.7,3,0), (7.6,0,0), (11.4,0,0)$.

| alignment $M$ | $|M|$ | least RMSD |
|---|---|---|
| $(1,1), (2,2), (3,3), (4,4)$, by position | 4 | 2.00 Å |
| $(1,1), (2,2), (3,3)$ | 3 | 0.96 Å |
| $(1,1), (2,2), (3,4), (4,5)$, with a gap in $A$ | 4 | 0 Å |

Pairing by position matches $a_3$ with the bulge and pulls the fit out of line. Dropping pairs lowers the RMSD but leaves part of the chain out. The right alignment puts a gap against the bulge and fits perfectly. The example also shows why an RMSD alone is not a score for alignment: the empty alignment and any one pair have RMSD 0. A score must reward the length and penalize the deviation, which each of the scores above does in its own way.

## Known algorithms

| method | score | search | status |
|---|---|---|---|
| [DALI](/dali/) (Holm and Sander 1993) | elastic similarity of distance matrices | hexapeptide contact patterns, then Monte Carlo | heuristic |
| [CE](/combinatorial-extension/) (Shindyalov and Bourne 1998) | distance differences of aligned fragment pairs, then RMSD | combinatorial extension of a path of fragment pairs | heuristic |
| TM-align (Zhang and Skolnick 2005) | TM-score | seeds, then alternating dynamic programming and superposition | heuristic |
| LGA (Zemla 2003) | residues within cutoffs, as in [GDT-TS](/gdt-ts/) | iterative superposition of subsets | heuristic |
| FATCAT (Ye and Godzik 2003) | fragment pairs with twists | dynamic programming over fragment chains | heuristic, flexible |
| Kolodny and Linial (2004) | scores defined through a superposition | grid of rigid motions, dynamic programming for each | polynomial-time approximation |
| Lancia, Carr, Walenz and Istrail (2001) | contact map overlap | integer programming, branch and cut | exact, exponential worst case |

## Bounds

- **Contact map overlap is NP-hard.** Goldman, Istrail and Papadimitriou (1999) proved this, even for the sequential case, and gave polynomial algorithms for restricted classes of contact maps.
- **Threading is NP-complete.** Lathrop (1994) proved this for the threading problem with pairwise interaction preferences and variable-length gaps.
- **Superposition-based scores admit approximation.** Kolodny and Linial (2004) showed that for a broad class of scores defined through a superposition, a solution within any fixed accuracy of the optimum can be found in polynomial time: the rigid motions are searched on a fine grid, and for each motion the best sequential alignment is a dynamic program. The polynomial has a high degree, so the method is not used for routine searches.
- **The fixed-motion step is easy.** For a fixed superposition, the best sequential alignment under a sum of per-pair scores is a [Needleman-Wunsch](/needleman-wunsch/) dynamic program in $O(nm)$ time, and the best non-sequential one is an assignment problem, solved by the [Hungarian algorithm](/hungarian-algorithm/) in $O(n^2 m)$ time for $n \le m$.

## Reductions

- **Fixed alignment to superposition.** Given $M$, the best rigid motion for least RMSD is the [Kabsch algorithm](/kabsch-algorithm/) or the [quaternion method](/quaternion-superposition/) on the matched pairs.
- **Fixed superposition to sequence alignment.** Given $(R, t)$, set the score of the pair $(i, j)$ to $f(|R a_i + t - b_j|)$ and solve a [global alignment](/global-alignment/) with gaps. Alternating the two steps is the core of TM-align and of the final step of CE; each round cannot lower the score, but the result can be a local optimum.
- **Fragment pairs to cliques.** Methods that start from pairs of matching fragments or secondary structure elements form a graph whose edges join pairs that fit together, and a good alignment is a large clique of this graph; finding a [maximum clique](/maximum-clique/) is itself NP-hard.

## Applications

- **Function and evolution.** Two proteins with the same fold may share an ancestor even when their sequences show no relation. Structure alignment finds such remote homologs.
- **Classification.** Fold classifications such as SCOP and CATH group domains by structure similarity, and database search with DALI or CE finds the neighbors of a new structure.
- **Model assessment.** A model is aligned to the native structure to compute scores such as [GDT-TS](/gdt-ts/) and the [TM-score](/tm-score/) when the residue numbering is not shared.
- **Templates for prediction.** [Protein structure prediction](/protein-structure-prediction/) by homology modeling starts from templates found by sequence or structure similarity.

## References
