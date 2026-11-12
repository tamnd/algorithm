---
tag: 3YNAR9
kind: concept
slug: contact-map
name: Contact map
aliases:
- Residue contact map
area: biology/structure-prediction
level: intro
summary: A symmetric 0/1 matrix over the residues of a known structure, with a 1 where two residues are closer than a cutoff, usually C-beta atoms within 8 Å.
prereqs: [euclidean-distance]
see_also: [contact-map-prediction, structure-alignment, dali, protein-secondary-structure, uniform-grid, multidimensional-scaling, protein-structure-prediction, rmsd]
sources:
  - paper: doi:10.1006/jmbi.1998.1645
    title: Kevin W. Plaxco, Kim T. Simons and David Baker, Contact order, transition state placement and the refolding rates of single domain proteins, Journal of Molecular Biology 277(4), 1998, 985-994
    locator: the definition of the relative contact order and its correlation with folding rates
  - paper: doi:10.1016/S1359-0278(97)00041-2
    title: Michele Vendruscolo, Edo Kussell and Eytan Domany, Recovery of protein structure from contact maps, Folding and Design 2(5), 1997, 295-306
    locator: the reconstruction of three-dimensional structures from their contact maps
  - paper: doi:10.1006/jmbi.1993.1489
    title: Liisa Holm and Chris Sander, Protein structure comparison by alignment of distance matrices, Journal of Molecular Biology 233(1), 1993, 123-138
    locator: the use of residue distance matrices and their contact patterns to compare structures
  - paper: doi:10.1109/SFFCS.1999.814624
    title: Deborah Goldman, Sorin Istrail and Christos H. Papadimitriou, Algorithmic aspects of protein structure similarity, 40th Annual Symposium on Foundations of Computer Science (FOCS), 1999, 512-521
    locator: the contact map overlap problem and the proof that it is NP-hard
---

A contact map of a protein structure is a square matrix over its residues, with a 1 at $(i, j)$ when residues $i$ and $j$ are close in space and a 0 otherwise. Close usually means that the $C_\beta$ atoms ($C_\alpha$ for glycine) are less than 8 Å apart. The map is symmetric, it is the same for each rotation and translation of the structure, and it shows the secondary structure and the fold as patterns that a person or a program can read. This page is about the map of a known structure. [Contact map prediction](/contact-map-prediction/) estimates the map from the sequence alone.

## In plain words

A protein is a long chain that folds into a compact shape. Number the links of the chain from one end to the other. Now make a table with one row and one column for each link, and put a mark where two links touch, or nearly touch, in the folded shape.

Links that are next to each other in the chain always touch, so the marks along the middle of the table carry little news. The marks far from the middle are the interesting ones: they show that two parts of the chain, far apart along the chain, come together in space. A helix gives a thick band near the middle. Two strands that lie side by side give a line of marks across the table. The table does not change when the protein moves or turns, and it often holds enough to rebuild the shape.

## The idea

**Definition.** Let a structure have $L$ residues, with one representative point $p_i \in \mathbb{R}^3$ for residue $i$, in Å. For a cutoff $d_c$, the contact map is

$$C_{ij} = \begin{cases} 1 & \text{if } |p_i - p_j| < d_c \text{ and } i \ne j, \\ 0 & \text{otherwise.} \end{cases}$$

The underlying distance matrix $D_{ij} = |p_i - p_j|$ holds more: from it, classical [multidimensional scaling](/multidimensional-scaling/) recovers the points up to a rigid motion and a reflection. The contact map keeps one bit of each distance.

**Choices.** The representative point is one choice: $C_\alpha$ atoms, $C_\beta$ atoms with $C_\alpha$ for glycine, or the shortest distance between any two heavy atoms of the two residues. The cutoff is another: 8 Å for $C_\beta$ is the convention of the CASP assessments of contact prediction, and heavy-atom maps use smaller cutoffs, such as 6 Å in the contact order work of Plaxco, Simons and Baker. A minimum sequence separation $|i - j| \ge s$ removes the trivial contacts of chain neighbors. The CASP assessments group contacts by separation into short (6 to 11), medium (12 to 23) and long range (24 or more).

**Patterns.** In an $\alpha$-helix, residue $i$ is near $i + 3$ and $i + 4$, which gives a thick band along the diagonal. Two antiparallel $\beta$-strands give a line of contacts perpendicular to the diagonal, and two parallel strands give a line parallel to it, away from the diagonal. The [secondary structure](/protein-secondary-structure/) can be read off these patterns.

**Contact order.** The relative contact order of Plaxco, Simons and Baker (1998) is

$$\mathrm{CO} = \frac{1}{L \cdot N_c} \sum_{(i, j)\ \text{in contact}} |i - j|,$$

where $N_c$ is the number of contacts. It is the mean sequence separation of the contacts, divided by the length. A protein with many long-range contacts has a high contact order, and Plaxco, Simons and Baker found that such single-domain proteins fold more slowly.

**Computing the map.** The direct way tests all $\binom{L}{2}$ pairs, $\Theta(L^2)$ time. A cell list does better: put each point in a [uniform grid](/uniform-grid/) of cubes of side $d_c$, and compare each point only with the points in its own cube and the 26 neighbors. Atoms cannot overlap, so a ball of radius $d_c$ holds a bounded number of residues, and the cell list takes $O(L)$ time for protein structures. In the worst case, with all points in one cube, it takes $\Theta(L^2)$ time, which is also the size of the output then. The implementation uses a cell list and its tests check it against the direct test of all pairs.

## Examples

**A toy hairpin.** Take eight $C_\alpha$-like points, two strands of four residues with 3.8 Å steps along $x$ and 4.8 Å between the strands: residues 0 to 3 at $(3.8 i, 0, 0)$, and residues 4 to 7 at $(3.8 (7 - i), 4.8, 0)$, so the chain turns back on itself. With the cutoff 8 Å and the minimum separation 3, the contacts are

| $i$ | partners $j > i$ | separations |
|---|---|---|
| 0 | 6, 7 | 6, 7 |
| 1 | 5, 6, 7 | 4, 5, 6 |
| 2 | 5, 6 | 3, 4 |

Residue 0 faces residue 7 at 4.8 Å, 1 faces 6, and 2 faces 5. These pairs, $(0, 7)$, $(1, 6)$, $(2, 5)$, form the line perpendicular to the diagonal that marks two antiparallel strands. There are $N_c = 7$ contacts with separations summing to 35, so $\mathrm{CO} = 35/(8 \cdot 7) = 0.625$. With the minimum separation 1, the map has 20 contacts, because each chain neighbor at 3.8 Å and each $i, i + 2$ pair at 7.6 Å also count.

**Mirror images.** A structure and its mirror image have the same distance matrix and the same contact map. A map can never tell the two hands apart; the handedness must come from other knowledge, such as the right-handed twist of an $\alpha$-helix.

**Not a contact.** Two points exactly 8 Å apart are not in contact under the rule "less than 8 Å". Codes differ on this edge, so state the rule.

## Where it is used

- **Structure comparison.** [DALI](/dali/) aligns two structures by comparing their distance matrices, and the contact map overlap problem asks for the alignment that shares the most contacts. Goldman, Istrail and Papadimitriou (1999) proved that contact map overlap is NP-hard; see [structure alignment](/structure-alignment/).
- **Structure prediction.** Predicted contacts constrain the fold in [protein structure prediction](/protein-structure-prediction/). Vendruscolo, Kussell and Domany (1997) showed that a native contact map usually holds enough to rebuild the structure.
- **Evaluation.** Predicted maps are scored against the map of the native structure, for example by the precision of the top $L/5$ long-range contacts.
- **Folding kinetics.** The contact order predicts folding rates of small single-domain proteins.
- **Model checking.** The fraction of native contacts kept in a model, often called $Q$, measures how close a model or a simulation frame is to the native fold.

## References
