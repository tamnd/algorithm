---
tag: NQBJJN
kind: definition
slug: tm-score
name: TM-score
aliases:
- Template modeling score
area: biology/structure-prediction
level: advanced
summary: A score in (0,1] for two protein structures, the best mean of 1/(1+(d/d0)^2) over matched residues with a length-dependent d0; about 0.5 or more means the same fold.
prereqs: [rmsd, optimal-superposition]
see_also: [gdt-ts, structure-alignment, kabsch-algorithm, quaternion-superposition, combinatorial-extension, dali, protein-structure-prediction, alphafold]
sources:
  - paper: doi:10.1002/prot.20264
    title: Yang Zhang and Jeffrey Skolnick, Scoring function for automated assessment of protein structure template quality, Proteins 57(4), 2004, 702-710
    locator: the definition of the TM-score and of the length-dependent scale d0
  - paper: doi:10.1093/nar/gki524
    title: Yang Zhang and Jeffrey Skolnick, TM-align, a protein structure alignment algorithm based on the TM-score, Nucleic Acids Research 33(7), 2005, 2302-2309
    locator: the structure alignment that maximizes the TM-score over alignments and superpositions
  - paper: doi:10.1093/bioinformatics/btq066
    title: Jinrui Xu and Yang Zhang, How significant is a protein structure similarity with TM-score = 0.5?, Bioinformatics 26(7), 2010, 889-895
    locator: the statistics of the TM-score of unrelated pairs and the threshold of 0.5 for the same fold
---

The TM-score (template modeling score) measures how similar two protein structures are, given a residue correspondence. It is a number in $(0, 1]$: each matched residue adds a term between 0 and 1 that is large when its distance after superposition is small compared with a scale $d_0$, and the score takes the best superposition. The scale $d_0$ grows with the protein length, so a TM-score has the same meaning for small and large proteins, unlike the [RMSD](/rmsd/). A value of 1 means a perfect match, and a value of about 0.5 or more usually means the two structures have the same fold. Zhang and Skolnick defined it in 2004.

## Definition

**Model.** Each structure is its $C_\alpha$ trace, one point per residue, in Å. A correspondence pairs residue $x_i$ of the model with residue $y_i$ of the target for $i = 1, \ldots, N$, and $L$ is the length of the target, the normalization length.

**Scale.** For $L > 15$, let

$$d_0(L) = 1.24\, \sqrt[3]{L - 15} - 1.8 \quad \text{Å}.$$

This formula is 0 at $L \approx 18.06$ and negative below it. Programs therefore take $d_0 = \max(d_0(L), 0.5)$ Å, and $d_0 = 0.5$ Å for short chains. For $L = 40$, $d_0 = 1.826$ Å; for $L = 100$, $3.652$ Å; for $L = 300$, $6.360$ Å.

**TM-score.** With $d_i = |R x_i + t - y_i|$,

$$\mathrm{TM} = \max_{R \in SO(3),\ t \in \mathbb{R}^3}\ \frac{1}{L} \sum_{i=1}^{N} \frac{1}{1 + (d_i / d_0)^2}.$$

Each term is in $(0, 1]$, and $N \le L$, so $0 < \mathrm{TM} \le 1$. The value is 1 exactly when $N = L$ and some rigid motion puts every $x_i$ on $y_i$. A residue far away adds almost nothing, so a badly placed loop cannot spoil the score of a good core, which is the main contrast with RMSD.

**Computing it.** The maximum over $(R, t)$ has no closed form, because the terms are not quadratic in the distances. The TM-score program uses a heuristic search, which in outline is: take contiguous fragments of length $L$, $L/2$, $L/4$, down to about 4 residues as seeds; fit each seed by [optimal superposition](/optimal-superposition/); then repeat a few times: keep the residues closer than a search cutoff and fit again. The best superposition seen gives the score. The result is a lower bound of the true maximum, and in practice it is close. The implementation follows this outline. With $F = O(L \log L)$ seeds and a fixed cap on the rounds, its worst case time is $O(L^2 \log L)$.

**Over alignments.** When the correspondence is not given, TM-align (Zhang and Skolnick 2005) searches over alignments and superpositions together to maximize the TM-score. This is a heuristic for a [structure alignment](/structure-alignment/) problem.

## Examples and non-examples

**A hinge.** Take an ideal $\alpha$-helix of 40 residues ($C_\alpha$ radius 2.3 Å, $100°$ and 1.5 Å per residue) as the target, and as the model the same helix with residues 31 to 40 turned by $40°$ about an axis through residue 30. So the first 30 residues are exact and the last 10 are off.

| measure | value |
|---|---|
| $d_0(40)$ | 1.826 Å |
| RMSD after the least-RMSD fit of all 40 residues | 2.224 Å |
| TM-score at that same fit | 0.565 |
| TM-score after the search | 0.793 |
| residues within 1 Å at the best TM fit | 30 |

The least-RMSD fit spreads the error over all residues, so no part fits well. The TM-score search finds the fit of the 30 exact residues, which then contribute $30/40 = 0.75$, and the 10 turned residues add $0.043$.

**Identical structures.** A structure compared with itself has TM-score 1, and its $L$ residues contribute 1 each.

**The normalization length matters.** The same 12 matched and perfect residues give TM-score 1 when $L = 12$ and $0.5$ when they are normalized by a target of $L = 24$. The score is not symmetric when the two chains have different lengths: TM-align reports two values, one normalized by each chain.

**Not a TM-score.** The mean of $1/(1 + (d_i/d_0)^2)$ at the least-RMSD superposition (0.565 above) is only a lower bound. A TM-score with a $d_0$ for a length other than the target length is a different number, and tools state which length they use.

## Related definitions

- **[RMSD](/rmsd/).** The mean of squared distances. It is dominated by the worst residues and grows with the length for unrelated pairs.
- **[GDT-TS](/gdt-ts/).** The mean of the fractions of residues within 1, 2, 4 and 8 Å, each fraction maximized over superpositions. Both scores reward a well-fitted core; GDT-TS has fixed cutoffs, and the TM-score has a smooth weight with a length-dependent scale.
- **Fold significance.** Xu and Zhang (2010) studied the TM-scores of unrelated pairs and found that a TM-score above about 0.5 usually means the same fold, in the sense of the SCOP and CATH classifications.
- **TM-align.** The TM-score is also the objective of [structure alignment](/structure-alignment/) by TM-align. Other aligners, such as [DALI](/dali/) and [CE](/combinatorial-extension/), optimize their own scores, and their alignments can be rated by the TM-score afterwards.
- **pTM.** Structure prediction programs such as [AlphaFold](/alphafold/) report a predicted TM-score, an estimate of the TM-score of the model against the unknown true structure.

## References
