---
tag: ZSVBRN
kind: problem
slug: rna-pseudoknot-prediction
name: RNA pseudoknot prediction
aliases:
- Pseudoknot prediction
- Pseudoknotted structure prediction
- RNA folding with pseudoknots
area: biology/structure-prediction
level: advanced
summary: Predict RNA structures that include crossing base pairs, which standard folding excludes.
prereqs: [pseudoknot, zuker-algorithm]
see_also: [pseudoknot-np-hardness, rna-secondary-structure-prediction, mccaskill-algorithm, nearest-neighbor-model, maximum-weight-matching, interval-dp, sankoff-rna-algorithm, covariance-model]
sources:
  - paper: doi:10.1006/jmbi.1998.2436
    title: Elena Rivas and Sean R. Eddy, A dynamic programming algorithm for RNA structure prediction including pseudoknots, Journal of Molecular Biology 285(5), 1999, pages 2053 to 2068
    locator: the gap matrices, the class of structures, and the O(n^6) time and O(n^4) space bounds
  - paper: doi:10.1016/S0166-218X(00)00186-4
    title: Tatsuya Akutsu, Dynamic programming algorithms for RNA secondary structure prediction with pseudoknots, Discrete Applied Mathematics 104(1-3), 2000, pages 45 to 62
    locator: the simple pseudoknots, the O(n^4) time algorithm for them, and the NP-hardness of planar structures
  - paper: doi:10.1002/jcc.10296
    title: Robert M. Dirks and Niles A. Pierce, A partition function algorithm for nucleic acid secondary structure including pseudoknots, Journal of Computational Chemistry 24(13), 2003, pages 1664 to 1677
    locator: the partition function over a class of pseudoknots in O(n^5) time
  - paper: doi:10.1186/1471-2105-5-104
    title: Jens Reeder and Robert Giegerich, Design, implementation and evaluation of a practical pseudoknot folding algorithm based on thermodynamics, BMC Bioinformatics 5, 2004, article 104
    locator: the canonical simple recursive pseudoknots and the O(n^4) time algorithm pknotsRG
  - paper: doi:10.1089/106652700750050862
    title: Rune B. Lyngsø and Christian N. S. Pedersen, RNA pseudoknot prediction in energy-based models, Journal of Computational Biology 7(3-4), 2000, pages 409 to 427
    locator: NP-completeness with arbitrary pseudoknots in the nearest neighbor pseudoknot model
  - paper: doi:10.1093/bioinformatics/14.8.691
    title: Jack E. Tabaska, Robert B. Cary, Harold N. Gabow and Gary D. Stormo, An RNA folding method capable of identifying pseudoknots and base triples, Bioinformatics 14(8), 1998, pages 691 to 699
    locator: the maximum weighted matching method, which allows any crossing
  - paper: doi:10.1089/106652703322756186
    title: Samuel Ieong, Ming-Yang Kao, Tak-Wah Lam, Wing-Kin Sung and Siu-Ming Yiu, Predicting RNA secondary structures with arbitrary pseudoknots by maximizing the number of stacking pairs, Journal of Computational Biology 10(6), 2003, pages 981 to 995
    locator: the 1/2 and 1/3 approximation algorithms for stacking pairs
---

RNA pseudoknot prediction is the problem of computing the base pairs of an RNA when two pairs may cross. The standard folding algorithms, such as the [Zuker algorithm](/zuker-algorithm/), work only for nested [secondary structures](/rna-secondary-structure/), because each pair splits the sequence into an inside and an outside part. A [pseudoknot](/pseudoknot/) breaks this split. With arbitrary crossings and an energy that rewards stacks, the problem is NP-hard ([pseudoknot NP-hardness](/pseudoknot-np-hardness/)), so the exact algorithms fix a class of structures: $O(n^6)$ time for the class of Rivas and Eddy (1999), $O(n^5)$ for that of Dirks and Pierce (2003), and $O(n^4)$ for the simple pseudoknots of Akutsu (2000) and the canonical class of Reeder and Giegerich (2004).

## In plain words

Usually we assume that the folds of an RNA nest like brackets: if one pair encloses a stretch, the letters in that stretch pair only with each other. This makes the problem easy to cut into small parts. Real RNAs sometimes break the rule: letters in the loop of a hairpin pair with letters outside it. Such a fold is called a pseudoknot.

Once pairs may cross, a stretch is no longer closed, and a part can depend on letters far away. If any crossing is allowed and the score rewards long runs of pairs, no fast exact method is known. So programs allow only some shapes of crossings, which cover the common cases, and pay with more time for each shape they add.

## Definition

**Input.** A sequence $s = s_1 \cdots s_n$ over $\{A, C, G, U\}$, a set $\mathcal{B}$ of allowed pairs (usually AU, GC and GU), a hairpin minimum $\theta$ (usually 3), a class $\mathcal{C}$ of structures, and an energy $E(P)$ for each $P \in \mathcal{C}$.

**Structures.** A structure is a set $P$ of allowed pairs with at least $\theta$ bases inside each pair and no shared bases. Pairs may cross. The class $\mathcal{C}$ says which crossings are allowed.

**Output.** A structure $P^* \in \mathcal{C}$ of minimum energy, or, for the ensemble version, the partition function $Z = \sum_{P \in \mathcal{C}} e^{-E(P)/RT}$ and the pair probabilities.

**Cost model.** Time and space on the [word RAM](/word-ram/), as functions of the length $n$. Each energy term is a table lookup in $O(1)$ time.

## Variants

- **All structures, pair weights only.** $\mathcal{C}$ is every structure and $E(P) = -\sum w(i, j)$. This is a [maximum weight matching](/maximum-weight-matching/) in the graph of allowed pairs and is polynomial. Tabaska and others (1998) used it to find pseudoknots and base triples.
- **All structures, stacking energies.** $\mathcal{C}$ is every structure and stacks of neighbor pairs get a bonus. NP-hard; see [pseudoknot NP-hardness](/pseudoknot-np-hardness/).
- **Simple pseudoknots** (Akutsu 2000). Crossings of the H-type kind inside a nested frame: in an interval, pairs from two or three sets that cross in a regular way. Exact in $O(n^4)$ time for a pair-based score.
- **The gap matrix class** (Rivas and Eddy 1999). The structures that their recurrences generate, with tables of an interval with one gap, $(i, j, k, l)$. It contains the H-type pseudoknots, the kissing hairpins and some deeper crossings.
- **The Dirks and Pierce class** (2003). A class that allows the partition function to be computed without counting a structure twice; it contains the H-type pseudoknots and pseudoknots nested in them.
- **Canonical simple recursive pseudoknots** (Reeder and Giegerich 2004). H-type pseudoknots in which the two helices have a canonical form, with any nested structure in their loops and pseudoknots in the loops in turn.
- **Ensemble and probabilities.** The partition function over the class, as in the [McCaskill algorithm](/mccaskill-algorithm/) for nested structures. Dirks and Pierce gave the first such algorithm with pseudoknots.
- **Comparative prediction.** Crossing pairs are often found by covariation in an alignment of many sequences of one family; see [simultaneous alignment and folding](/simultaneous-alignment-and-folding/) and the [covariance model](/covariance-model/).

## Examples

- **An H-type pseudoknot.** For $s = $ GGGAUUUAACCCAAAAA ($n = 17$) with AU, GC and GU pairs and $\theta = 3$, the best nested structure has 4 pairs, for example (((.(...))))....., with the pairs $(1, 12)$, $(2, 11)$, $(3, 10)$ and $(5, 9)$. The structure (((.[[[..)))..]]] has 6 pairs: the GC helix $\{(1, 12), (2, 11), (3, 10)\}$ and the UA helix $\{(5, 17), (6, 16), (7, 15)\}$, which cross. Six pairs is the most possible, because the sequence has only three U and three C bases. A nested algorithm cannot find it.
- **A frameshift or a telomerase pseudoknot.** Many viral frameshift signals and the core of the telomerase RNA are H-type pseudoknots. They are in the class of each of the exact algorithms below.
- **Kissing hairpins.** Two hairpins whose loops pair with each other. They are in the Rivas and Eddy class, but not in the simple pseudoknot class of Akutsu or the class of Dirks and Pierce. Later versions of the canonical method of Reeder and Giegerich add them.

## Known algorithms

| method | class | output | time |
|---|---|---|---|
| maximum weight matching (Tabaska and others 1998) | all structures, pair weights | optimum | polynomial |
| Rivas and Eddy (1999), pknots | gap matrix class | minimum energy | $O(n^6)$ |
| Akutsu (2000) | simple pseudoknots | optimum of a pair score | $O(n^4)$ |
| Dirks and Pierce (2003) | their class | partition function | $O(n^5)$ |
| Reeder and Giegerich (2004), pknotsRG | canonical simple recursive | minimum energy | $O(n^4)$ |

All the bounds are worst case, with $n$ the length of the sequence. The Rivas and Eddy algorithm uses $O(n^4)$ space. The exact class methods extend the [interval dynamic program](/interval-dp/) of nested folding with tables for an interval with one or more gaps: a table indexed by $(i, j, k, l)$ describes the positions $i$ to $k$ and $l$ to $j$, with a gap $k + 1$ to $l - 1$ that is filled later. This gives the $O(n^4)$ space and the higher powers of $n$ in the time.

- **Heuristics.** Programs add helices one by one, or search with stochastic methods, or solve an integer program over pair probabilities. They handle wider classes on longer sequences but give no guarantee of an optimum.
- **Approximation.** For the largest number of stacking pairs, Ieong, Kao, Lam, Sung and Yiu (2003) give a $1/2$-approximation for planar structures in $O(n^3)$ time and a $1/3$-approximation for all structures in $O(n)$ time.

## Bounds

- **Lower bounds.** For arbitrary pseudoknots and an energy that depends on neighbor pairs, the decision problem is NP-complete (Lyngsø and Pedersen 2000), so no polynomial exact algorithm exists unless P = NP. Optimal planar structures are also NP-hard (Akutsu 2000). See [pseudoknot NP-hardness](/pseudoknot-np-hardness/).
- **Upper bounds.** The time grows with the class: $O(n^3)$ with no crossings, $O(n^4)$ for simple and canonical H-type classes, $O(n^5)$ and $O(n^6)$ for wider classes. In practice the $O(n^6)$ time and $O(n^4)$ space of pknots limit it to sequences of about a hundred bases.
- **Energy parameters.** Few melting experiments exist for pseudoknots, so their loop terms are fits with fewer data than the terms of the [nearest-neighbor model](/nearest-neighbor-model/). Errors in these terms limit the accuracy more than the class does.

## Reductions

- **From nested folding.** If the class has no crossing structures, the problem is [RNA secondary structure prediction](/rna-secondary-structure-prediction/). Each class algorithm contains a nested folding algorithm as the part with no gaps.
- **To matching.** With pair weights only and any crossing allowed, the problem is maximum weight matching.
- **From 3SAT.** With stacking energies and any crossing allowed, there is a polynomial reduction from a bounded form of 3SAT; see [pseudoknot NP-hardness](/pseudoknot-np-hardness/).
- **To grammars.** The class methods correspond to grammars stronger than context-free grammars, such as multiple context-free grammars, whose parsing takes higher powers of $n$.

## Applications

- Viral RNAs, where H-type pseudoknots cause ribosomal frameshifts and help start translation.
- The telomerase RNA, the RNase P RNA, the transfer-messenger RNA and many riboswitches, whose cores are pseudoknots.
- Ribosomal RNAs, whose known structures contain pseudoknots that comparative analysis found.
- Design of RNAs with pseudoknots, where a design must be checked by a folding algorithm that can see them.

## References
