---
tag: 36CBME
kind: definition
slug: gdt-ts
name: GDT-TS
aliases:
- Global distance test total score
- GDT_TS
area: biology/structure-prediction
level: advanced
summary: The mean of the percentages of residues that some superposition puts within 1, 2, 4 and 8 Å of the native, each percentage maximized on its own; CASP's main model score.
prereqs: [rmsd, optimal-superposition]
see_also: [tm-score, structure-alignment, kabsch-algorithm, quaternion-superposition, protein-structure-prediction, alphafold]
sources:
  - paper: doi:10.1093/nar/gkg571
    title: Adam Zemla, LGA, a method for finding 3D similarities in protein structures, Nucleic Acids Research 31(13), 2003, 3370-3374
    locator: the GDT (global distance test) measure, the GDT_TS score as the mean over the cutoffs 1, 2, 4 and 8 Å, and the iterative superposition procedure of LGA
  - paper: doi:10.1002/prot.20264
    title: Yang Zhang and Jeffrey Skolnick, Scoring function for automated assessment of protein structure template quality, Proteins 57(4), 2004, 702-710
    locator: the comparison of the TM-score with GDT and MaxSub
---

GDT-TS (global distance test, total score) measures how close a model of a protein is to the native structure, given a residue correspondence. For each cutoff $c$ of 1, 2, 4 and 8 Å it finds the largest share of residues that one superposition puts within $c$ of their native positions, and it reports the mean of the four shares, in percent from 0 to 100. Each share has its own best superposition. Zemla defined it with the LGA program in 2003, and it has been the main score for model accuracy in the CASP experiments. A score is a percentage; a higher value is better.

## Definition

**Model.** Each structure is its $C_\alpha$ trace, one point per residue, in Å. A correspondence pairs model residue $x_i$ with native residue $y_i$ for $i = 1, \ldots, N$, usually by residue number, and $L$ is the number of residues of the native structure.

**Percent under a cutoff.** For $c > 0$,

$$P_c = \frac{100}{L}\ \max_{R \in SO(3),\ t \in \mathbb{R}^3}\ \bigl|\{\, i : |R x_i + t - y_i| \le c \,\}\bigr| .$$

**GDT-TS.**

$$\mathrm{GDT\text{-}TS} = \frac{P_1 + P_2 + P_4 + P_8}{4}.$$

Since a larger cutoff can only hold more residues, $P_1 \le P_2 \le P_4 \le P_8$. The score is 100 exactly when one rigid motion puts all $L$ residues within 1 Å.

**GDT-HA.** The high-accuracy form uses the cutoffs 0.5, 1, 2 and 4 Å, and it separates good models from very good ones.

**Computing it.** The maximum in $P_c$ is not a least-squares problem, so [optimal superposition](/optimal-superposition/) does not solve it directly. LGA uses an iterative heuristic, and the implementation here follows the same outline: take contiguous fragments of the model as seeds; fit each seed by least RMSD; then repeat: keep the residues within $c$ and fit them again, until the set does not change. Each fit updates the best count for every cutoff, which keeps $P_1 \le P_2 \le P_4 \le P_8$. The result is a lower bound of each $P_c$. With $O(L \log L)$ seeds and a fixed cap on the rounds, the worst case time is $O(L^2 \log L)$.

An exact maximum is possible in principle in polynomial time, because a rigid motion has six parameters and the motions that put residue $i$ within $c$ form a region bounded by algebraic surfaces of bounded degree, so the arrangement of the $L$ regions has polynomial size. Such exact methods are much slower than the heuristic, and the tools in use do not run them.

## Examples and non-examples

**A hinge.** The target is an ideal $\alpha$-helix of 40 residues ($C_\alpha$ radius 2.3 Å, $100°$ and 1.5 Å per residue), and the model is the same helix with residues 31 to 40 turned by $40°$ about an axis through residue 30.

| cutoff $c$ | residues at the least-RMSD fit of all 40 | best count found by the search | $P_c$ |
|---|---|---|---|
| 1 Å | 10 | 31 | 77.5 |
| 2 Å | 26 | 34 | 85.0 |
| 4 Å | 37 | 38 | 95.0 |
| 8 Å | 40 | 40 | 100.0 |

So $\mathrm{GDT\text{-}TS} = (77.5 + 85 + 95 + 100)/4 = 89.375$. For the 1 Å cutoff, the fit of the whole chain is a poor choice: it moves every residue a bit, and only 10 stay within 1 Å. A fit on the 30 exact residues keeps those 30 within 1 Å, and the search finds a fit with 31. The GDT-HA of the same model is 83.125.

**The same model.** A model equal to the native, up to a rigid motion, has GDT-TS 100.

**A partial model.** A model that has only 20 of the 40 native residues, all exact, has $P_c = 50$ for each cutoff and GDT-TS 50, because the count is divided by the native length $L$.

**Not a GDT-TS.** The four counts at one shared superposition, such as the least-RMSD fit, give a lower number, here $(10 + 26 + 37 + 40)/160 \cdot 100 = 70.6$. That is a lower bound, not the score.

## Related definitions

- **[RMSD](/rmsd/).** One superposition and a mean of squares. One bad region can dominate it. GDT-TS ignores the residues outside each cutoff.
- **[TM-score](/tm-score/).** A smooth weight $1/(1 + (d/d_0)^2)$ with a length-dependent scale replaces the four fixed cutoffs, and the value is in $(0, 1]$.
- **LGA.** The LGA program of Zemla (2003) computes GDT and also a sequence-independent structure alignment, so it can compare structures without a given correspondence; see [structure alignment](/structure-alignment/).
- **MaxSub.** An earlier measure that finds the largest subset of residues within a single cutoff of 3.5 Å.

## References
